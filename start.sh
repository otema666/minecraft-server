#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Inicia el servidor de Minecraft
echo -e "${GREEN}[+] Starting Minecraft server...${NC}"
java -Xmx1024M -jar paper-1.21.1-128.jar nogui
