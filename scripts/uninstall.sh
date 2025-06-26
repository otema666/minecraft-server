#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Detener el servidor de Minecraft (si está en ejecución)
echo -e "${GREEN}Stopping Minecraft server...${NC}"
pkill -f "paper-.*\.jar" || echo -e "${GREEN}No running Minecraft server found.${NC}"

# Desinstalar Java
echo -e "${GREEN}Uninstalling default JRE...${NC}"
sudo apt remove --purge -y default-jre

# Limpiar paquetes no utilizados
echo -e "${GREEN}Removing unused packages...${NC}"
sudo apt autoremove -y

echo -e "${GREEN}Minecraft and Java have been uninstalled.${NC}"

# Eliminar el directorio de Minecraft
echo -e "${GREEN}Por favor, elimine el directorio de Minecraft manualmente.${NC}"
