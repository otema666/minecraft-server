#!/usr/bin/env bash
set -euo pipefail

# Colores
GREEN='\e[1;32m'
ORANGE='\e[1;34m'
YELLOW='\e[1;33m'
RED='\e[1;31m'
NC='\e[0m'

SERVER_JAR="paper.jar"
SERVER_PATTERN="java.*-Xmx.*-jar paper\.jar nogui"
SCRIPTS_DIR="scripts"

show_menu() {
    clear
    figlet -f slant "        MENU" | lolcat

    # Detectar estado
    if [[ -f "$SERVER_JAR" ]]; then
        installed=true
    else
        installed=false
    fi
    if pgrep -f "$SERVER_PATTERN" &>/dev/null; then
        running=true
    else
        running=false
    fi

    # Construir arrays vacíos
    MENU_LABELS=()
    MENU_CMDS=()
    MENU_COLORS=()

    if ! $installed; then
        # No instalado: solo instalar
        MENU_LABELS+=("1. Instalar servidor (install.sh)")
        MENU_CMDS+=("./$SCRIPTS_DIR/install.sh")
        MENU_COLORS+=("$ORANGE")
    else
        if $running; then
            # Instalado y corriendo: solo abrir consola
            MENU_LABELS+=("1. Abrir consola (screen -r minecraft)")
            MENU_CMDS+=("screen -r minecraft")
            MENU_COLORS+=("$GREEN")
        else
            # Instalado pero no corriendo: menú completo
            MENU_LABELS+=("1. Iniciar servidor (start.sh)")
            MENU_CMDS+=("./$SCRIPTS_DIR/start.sh")
            MENU_COLORS+=("$GREEN")

            MENU_LABELS+=("2. Configurar servidor (configure-server.py)")
            MENU_CMDS+=("./$SCRIPTS_DIR/configure-server.py")
            MENU_COLORS+=("$ORANGE")

            MENU_LABELS+=("3. Configurar plugins (plugin-manager.sh)")
            MENU_CMDS+=("./$SCRIPTS_DIR/plugin-manager.sh")
            MENU_COLORS+=("$ORANGE")

            MENU_LABELS+=("4. Desinstalar servidor (uninstall.sh)")
            MENU_CMDS+=("./$SCRIPTS_DIR/uninstall.sh")
            MENU_COLORS+=("$ORANGE")

            MENU_LABELS+=("5. Actualizar PaperMC (update-paper.sh)")
            MENU_CMDS+=("./$SCRIPTS_DIR/update-paper.sh")
            MENU_COLORS+=("$YELLOW")

            MENU_LABELS+=("6. Actualizar plugins (update-plugins.sh)")
            MENU_CMDS+=("./$SCRIPTS_DIR/update-plugins.sh")
            MENU_COLORS+=("$YELLOW")
        fi
    fi

    # Siempre añadimos Salir al final
    MENU_LABELS+=("0. Salir")
    MENU_CMDS+=("exit")
    MENU_COLORS+=("$RED")

    # Imprimir marco
    local width=60
    local inner=$((width - 4))
    local border
    border=$(printf '=%.0s' $(seq 1 $width))
    echo "$border"
    local title="MENÚ DE SERVIDOR MC"
    local pad=$(( (inner - ${#title}) / 2 ))
    printf "| %*s%s%*s |\n" "$pad" "" "$title" $((inner - pad - ${#title})) ""
    echo "$border"

    # Imprimir opciones con color
    for i in "${!MENU_LABELS[@]}"; do
        color=${MENU_COLORS[i]}
        label=${MENU_LABELS[i]}
        printf "| ${color}%-${inner}s${NC} |\n" "$label"
    done

    echo "$border"
    echo
}

while true; do
    show_menu
    read -rp "Seleccione opción [0-${#MENU_LABELS[@]}]: " opt
    echo
    if [[ "$opt" == "0" ]]; then
        echo -e "${RED}Saliendo...${NC}"
        exit 0
    elif [[ "$opt" =~ ^[1-9][0-9]*$ ]] && (( opt >=1 && opt < ${#MENU_CMDS[@]} )); then
        cmd=${MENU_CMDS[opt-1]}
        eval "$cmd"
    else
        echo -e "${RED}Opción inválida.${NC}"
    fi
    echo -e "\nPresione Enter para continuar..."
    read -r
done
