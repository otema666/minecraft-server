#!/usr/bin/env bash
set -euo pipefail

# Colores ANSI
RED="\e[31m" GREEN="\e[32m" YELLOW="\e[33m"
CYAN="\e[36m" BOLD="\e[1m" RESET="\e[0m"

# Chequea paper.jar
if [[ ! -f paper.jar ]]; then
  echo -e "${RED}$(pwd)"
  echo -e "${RED}[-] Error:${RESET} No se encuentra ${BOLD}paper.jar${RESET}. Ejecuta ${BOLD}install.sh${RESET} primero."
  exit 1
fi

# Asignación de memoria segura
XMS="512M"
XMX="1024M"

echo -e "${CYAN}${BOLD}Iniciando servidor:${RESET}"
echo -e "  -Xms = ${YELLOW}${XMS}${RESET}"
echo -e "  -Xmx = ${YELLOW}${XMX}${RESET}"

# Flags Aikar para G1GC
GC_FLAGS=(
  -XX:+UseG1GC
  -XX:+ParallelRefProcEnabled
  -XX:MaxGCPauseMillis=200
  -XX:+UnlockExperimentalVMOptions
  -XX:+DisableExplicitGC
  -XX:+AlwaysPreTouch
  -XX:G1NewSizePercent=30
  -XX:G1MaxNewSizePercent=40
  -XX:G1HeapRegionSize=8M
  -XX:G1ReservePercent=20
  -XX:G1HeapWastePercent=5
  -XX:InitiatingHeapOccupancyPercent=15
  -XX:G1MixedGCLiveThresholdPercent=90
  -XX:SurvivorRatio=32
  -XX:+PerfDisableSharedMem
  -XX:MaxTenuringThreshold=1
  -Dusing.aikars.flags=true
  -Daikars.new.flags=true
)

echo -e "${GREEN}[+] Lanzando servidor en screen 'minecraft'${RESET}"

if ! screen -S minecraft -d -m java \
  -server \
  -Xms${XMS} -Xmx${XMX} \
  "${GC_FLAGS[@]}" \
  -jar paper.jar nogui; then
  echo -e "${RED}[-] Error:${RESET} Falló al iniciar el servidor en screen. Verifica que screen esté instalado y funcionando."
  exit 1
fi

echo -e "${GREEN}[+] Servidor iniciado.${RESET}"
echo -e "${CYAN}[-] Para ver la consola: ${BOLD}screen -r minecraft${RESET}"
screen -r minecraft
