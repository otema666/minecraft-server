#!/usr/bin/env bash
set -euo pipefail

# Rutas de los archivos que queremos modificar
PROPS_FILE="server.properties"
MOTD_CONF="plugins/MiniMOTD/main.conf"
BLUEMAP_CONF="plugins/BlueMap/core.conf"

# 0) Comprobación previa de archivos
missing=()
[[ ! -f "$PROPS_FILE" ]] && missing+=("$PROPS_FILE")
[[ ! -f "$MOTD_CONF"   ]] && missing+=("$MOTD_CONF")
[[ ! -f "$BLUEMAP_CONF" ]] && missing+=("$BLUEMAP_CONF")

if (( ${#missing[@]} )); then
  echo "ERROR: No se encontraron los siguientes archivos:"
  for f in "${missing[@]}"; do
    echo "  - $f"
  done
  echo ""
  echo "Asegúrate de ejecutar el servidor al menos una vez para generarlos,"
  echo "o de que las rutas sean correctas."
  exit 1
fi

# 1) Pedimos el número máximo de jugadores
read -p "Introduce el valor de max-players: " MAX_PLAYERS

# 2) Actualizamos server.properties
sed -i "s/^max-players=.*/max-players=${MAX_PLAYERS}/"            "$PROPS_FILE"
sed -i "s/^view-distance=.*/view-distance=15/"                   "$PROPS_FILE"
sed -i "s/^simulation-distance=.*/simulation-distance=13/"       "$PROPS_FILE"
sed -i "s/^online-mode=.*/online-mode=false/"                     "$PROPS_FILE"
echo "-> $PROPS_FILE actualizado."

# 3) Actualizamos plugins/MiniMOTD/main.conf

# 3a) Cambiamos player-count-settings.max-players
sed -i "s/^\(\s*max-players=\).*/\1${MAX_PLAYERS}/"               "$MOTD_CONF"

# 3b) Reemplazamos todo el bloque motds=[ ... ]
sed -i '/^motds=\[/,/^\]/c\
motds=[\
    {\
        # Set the icon to use with this MOTD\
        #  Either use '\''random'\'' to randomly choose an icon, or use the name\
        #  of a file in the icons folder (excluding the '\''.png'\'' extension)\
        #    ex: icon="myIconFile"\
        icon=random\
        line1="<blue>Hello <bold><red>nigga!"\
        line2="<italic><underlined><gradient:red:green>nigger"\
    }\
]'                                                               "$MOTD_CONF"
echo "-> $MOTD_CONF actualizado."

# 4) Actualizamos plugins/BlueMap/core.conf

# Cambiamos accept-download: false → true
sed -i "s/^\s*accept-download:\s*false/accept-download: true/"     "$BLUEMAP_CONF"
echo "-> $BLUEMAP_CONF actualizado (accept-download: true)."

echo ""
echo "¡Configuración completada!"
