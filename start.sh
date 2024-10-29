#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

if screen -list | grep -q "minecraft"; then
  echo -e "${RED}[-] El servidor de Minecraft ya está en ejecución!${NC}"
  exit 1
fi

echo -e "${GREEN}[+] Iniciando el servidor de Minecraft...${NC}\n"
clear
screen -S minecraft -d -m java -Xmx1024M -jar paper-1.21.1-128.jar nogui
echo -e "${GREEN}[+] Servidor en ejecución. Para ver la consola, use el comando 'screen -r minecraft'.${NC}\n"
cleanup() {
  echo -e "${GREEN}[+] Deteniendo el servidor de Minecraft...${NC}"
  screen -S minecraft -p 0 -X stuff "stop$(printf '\r')"
  sleep 5
  echo -e "${GREEN}[+] Server stopped. Exiting script.${NC}"
  exit 0
}

trap cleanup SIGINT

auto_save() {
echo -e "${GREEN}[+] Iniciando el guardado automático del mundo...${NC}"
  while screen -list | grep -q "minecraft"; do
    sleep 500
    echo -e "${GREEN}[+] Guardando mundo...${NC}"
    screen -S minecraft -p 0 -X stuff "say Mundo Guardado!$(printf '\r')"
    sleep 5
    screen -S minecraft -p 0 -X stuff "save-all$(printf '\r')"
  done
}

auto_save
