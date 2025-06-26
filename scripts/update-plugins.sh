#!/usr/bin/env bash
set -euo pipefail

# 0) Verificar que el servidor no esté en ejecución
if pgrep -f "java.*-Xmx.*-jar paper\.jar nogui" &>/dev/null; then
  echo "ERROR: El servidor está en ejecución. Deténlo antes de actualizar plugins."
  exit 1
fi

# 1) Comprobar dependencias mínimas
for cmd in unzip jq curl; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ERROR: Falta '$cmd'. Instálalo con: sudo apt install $cmd"
    exit 1
  fi
done

PLUGINS_DIR="plugins"
BACKUP_DIR="plugin-backups/$(date +%F_%H%M)"
API_BASE="https://api.spiget.org/v2"

echo "$(pwd)"
mkdir -p "$BACKUP_DIR"
echo "=== Comprobando plugins en $PLUGINS_DIR ==="

for jar in "$PLUGINS_DIR"/*.jar; do
  [[ -f "$jar" ]] || { echo "No hay plugins en $PLUGINS_DIR"; break; }

  # Extraer name y version del plugin.yml
  name=$(unzip -p "$jar" plugin.yml \
           | awk -F': ' '/^[[:space:]]*name:/ {print $2; exit}')
  local_ver=$(unzip -p "$jar" plugin.yml \
                   | awk -F': ' '/^[[:space:]]*version:/ {print $2; exit}')

  if [[ -z "$name" || -z "$local_ver" ]]; then
    echo "SKIP: No pude extraer name/version de $jar"
    continue
  fi

  echo -e "\nPlugin: $name (v$local_ver)"

  # 2) Busqueda y filtrado por testedVersions 1.21.x
  query=$(printf '%s' "$name" | jq -sRr @uri)
  search_url="${API_BASE}/search/resources/${query}?field=name"
  raw=$(curl -sSf "$search_url") || {
    echo "  × ERROR: fallo al buscar $name"; continue
  }

  # Extraer únicamente el ID del recurso que:
  #  - name exacto
  #  - testedVersions incluye algo que empieza por "1.21"
  remote_id=$(jq -r --arg nm "$name" '
    .[]
    | select(.name == $nm)
    | select(any(.testedVersions[]; startswith("1.21")))
    | .id
    | tostring
    ' <<<"$raw")

  if [[ -z "$remote_id" ]]; then
    echo "  → No hay versión compatible con 1.21.x o no existe el plugin en Spiget."
    continue
  fi
  echo "  → ID en Spiget: $remote_id"

  # 3) Obtener la última versión publicada (p.ej. "2.3.1", etc.)
  latest_json=$(curl -sSf "${API_BASE}/resources/${remote_id}/versions/latest")
  remote_ver=$(jq -r '.name' <<<"$latest_json")
  echo "  → Última versión en Spiget: v$remote_ver"

  # 4) Comparar con la local y actualizar si hace falta
  if [[ "$remote_ver" == "$local_ver" ]]; then
    echo "  ✓ Ya estás en la última versión."
    continue
  fi

  echo "  → Actualizando $name: v$local_ver → v$remote_ver"
  # Backup
  cp "$jar" "$BACKUP_DIR/"

  # Descargar nuevo JAR
  dl_url="${API_BASE}/resources/${remote_id}/download"
  tmpfile=$(mktemp)
  curl -sSL "$dl_url" -o "$tmpfile"

  # Reemplazar
  mv "$tmpfile" "$jar"
  echo "  ✓ $jar actualizado. Backup en $BACKUP_DIR/$(basename "$jar")"
done

echo -e "\n=== Actualización de plugins completada ==="
