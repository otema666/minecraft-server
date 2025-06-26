#!/usr/bin/env bash
set -euo pipefail

# Rutas
PROPS_FILE="server.properties"
SPIGOT_FILE="spigot.yml"
MOTD_CONF="plugins/MiniMOTD/main.conf"
BLUEMAP_CONF="plugins/BlueMap/core.conf"

# 0) Comprobación de archivos y yq
missing=()
for f in "$PROPS_FILE" "$SPIGOT_FILE" "$MOTD_CONF" "$BLUEMAP_CONF"; do
  [[ ! -f "$f" ]] && missing+=("$f")
done
if (( ${#missing[@]} )); then
  echo "ERROR: faltan archivos:"
  for f in "${missing[@]}"; do echo "  - $f"; done
  exit 1
fi

if ! command -v yq &> /dev/null; then
    echo "ERROR: 'yq' no está instalado. Por favor, instálalo para continuar."
    echo "Puedes encontrar instrucciones aquí: https://github.com/mikefarah/yq#install"
    exit 1
fi

# 1) max-players
read -p "Introduce el valor de max-players: " MAX_PLAYERS

# 2) server.properties optimizado
sed -i -E "
  s/^max-players=.*/max-players=${MAX_PLAYERS}/;
  s/^view-distance=.*/view-distance=7/;
  s/^simulation-distance=.*/simulation-distance=5/;
  s/^entity-broadcast-range-percentage=.*/entity-broadcast-range-percentage=50/;
  s/^spawn-protection=.*/spawn-protection=0/;
  s/^spawn-animals=.*/spawn-animals=false/;
  s/^spawn-npcs=.*/spawn-npcs=false/;
  s/^online-mode=.*/online-mode=true/;
" "$PROPS_FILE"
echo "-> $PROPS_FILE optimizado."

# 3) spigot.yml optimizado usando yq
echo "Optimizando $SPIGOT_FILE usando yq..."

# Define parámetros clave-valor para world-settings.default
declare -A SPIGOT_PARAMS=(
  ["mob-spawn-range"]="4"
  ["nerf-spawner-mobs"]="true"
  ["tick-inactive-villagers"]="false"
  ["mob-spawner-tick-rate"]="2"
  ["arrow-despawn-rate"]="300"
  ["item-despawn-rate"]="4000"
)

# Modifica o añade claves individuales dentro de world-settings.default
for key in "${!SPIGOT_PARAMS[@]}"; do
  yq -i ".world-settings.default.${key} = \"${SPIGOT_PARAMS[$key]}\"" "$SPIGOT_FILE"
done

# Define y reemplaza/añade bloques completos dentro de world-settings.default
yq -i '
  .world-settings.default."entity-activation-range" = {
    animals: 24,
    monsters: 24,
    raiders: 48,
    misc: 8,
    water: 8,
    villagers: 24,
    "flying-monsters": 24
  }
' "$SPIGOT_FILE"

yq -i '
  .world-settings.default."entity-tracking-range" = {
    players: 96,
    animals: 48,
    monsters: 48,
    misc: 32,
    display: 64,
    other: 32
  }
' "$SPIGOT_FILE"

yq -i '
  .world-settings.default."merge-radius" = {
    item: 2.0,
    exp: 2.0
  }
' "$SPIGOT_FILE"

echo "-> $SPIGOT_FILE optimizado."

# 4) MiniMOTD
sed -i "s/^\(\s*max-players=\).*/\1${MAX_PLAYERS}/" "$MOTD_CONF"
sed -i '/^motds=\[/,/^\]/c\
motds=[\
    {\
      icon=random\
      line1="<blue>Hello <bold><red>¡Bienvenid@s!"\
      line2="<italic><gradient:green:yellow>Diviértete"\
    }\
]' "$MOTD_CONF"
echo "-> $MOTD_CONF actualizado."

# 5) BlueMap
sed -i "s/^\s*accept-download:\s*false/accept-download: true/" "$BLUEMAP_CONF"
echo "-> $BLUEMAP_CONF (accept-download=true)."

echo ""
echo "🎉 ¡Configuración completada y optimizada para rendimiento y jugabilidad!"