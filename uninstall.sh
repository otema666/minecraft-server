#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Detener el servidor de Minecraft (si está en ejecución)
echo -e "${GREEN}Stopping Minecraft server...${NC}"
pkill -f paper-1.21.1-128.jar || echo -e "${GREEN}No running Minecraft server found.${NC}"

# Eliminar el directorio de Minecraft
echo -e "${GREEN}Removing Minecraft directory...${NC}"
rm -rf /home/otema/minecraft

# Desinstalar Java
echo -e "${GREEN}Uninstalling default JRE...${NC}"
sudo apt remove --purge -y default-jre

# Limpiar paquetes no utilizados
echo -e "${GREEN}Removing unused packages...${NC}"
sudo apt autoremove -y

echo -e "${GREEN}Minecraft and Java have been uninstalled.${NC}"
