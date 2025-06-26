#!/usr/bin/env bash
set -euo pipefail

# 0) Verificar que el servidor no esté en ejecución
if pgrep -f "java.*-Xmx.*-jar paper\.jar nogui" >/dev/null; then
  echo "ERROR: El servidor está en ejecución. Deténlo antes de actualizar."
  exit 1
fi

# Versión de Minecraft/Paper que quieres usar
PAPER_VERSION="1.21.1"

# Directorio base del servidor (ajusta si quieres otro)
SERVER_DIR="$(pwd)"

# Comprobamos que jq está instalado
if ! command -v jq &>/dev/null; then
  echo "ERROR: jq no está instalado. Instálalo (por ejemplo: sudo apt install jq) y vuelve a ejecutar."
  exit 1
fi

# URL de la API para listar builds
API_URL="https://api.papermc.io/v2/projects/paper/versions/${PAPER_VERSION}/builds"

echo "[$(date +'%F %T')] Obteniendo datos de builds de Paper ${PAPER_VERSION}..."
# Descarga el JSON completo, extrae el último build y el nombre del JAR
API_RESPONSE=$(curl -s "${API_URL}")
LATEST_BUILD=$(jq -r '.builds | last | .build' <<<"$API_RESPONSE")
JAR_NAME=$(jq -r '.builds | last | .downloads.application.name' <<<"$API_RESPONSE")

# Validaciones
if [[ -z "$LATEST_BUILD" || -z "$JAR_NAME" ]]; then
  echo "ERROR: no se pudo obtener el último build o el nombre del JAR (¿versión o API incorrecta?)."
  exit 1
fi

echo "[$(date +'%F %T')] Último build disponible: ${LATEST_BUILD}"
echo "[$(date +'%F %T')] Nombre de JAR a descargar: ${JAR_NAME}"

# Construimos la URL de descarga usando el nombre oficial
DOWNLOAD_URL="https://api.papermc.io/v2/projects/paper/versions/${PAPER_VERSION}/builds/${LATEST_BUILD}/downloads/${JAR_NAME}"

echo "[$(date +'%F %T')] Descargando Paper ${PAPER_VERSION}-${LATEST_BUILD}..."
curl -fL "${DOWNLOAD_URL}" -o "${SERVER_DIR}/paper.jar"

echo "[$(date +'%F %T')] ¡Listo! paper.jar ha sido actualizado al build ${LATEST_BUILD}."
echo "Ahora puedes arrancar el servidor con ./start.sh"
