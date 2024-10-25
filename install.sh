#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

# Actualizar el sistema
echo -e "${GREEN}[+] Updating package list...${NC}"
sudo apt update

# Actualizar paquetes instalados
echo -e "${GREEN}[+] Upgrading installed packages...${NC}"
sudo apt upgrade -y

# Instalar OpenJDK 21
echo -e "${GREEN}[+] Installing OpenJDK 21...${NC}"
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:openjdk-r/ppa -y
sudo apt update
sudo apt install -y openjdk-21-jdk

# Configurar Java predeterminado (opcional)
#sudo update-alternatives --config java

# Descargar el archivo JAR de PaperMC
echo -e "${GREEN}[+] Downloading PaperMC server jar...${NC}"
wget https://api.papermc.io/v2/projects/paper/versions/1.21.1/builds/128/downloads/paper-1.21.1-128.jar -O paper.jar

# Aceptar el EULA
echo "eula=true" > eula.txt

echo -e "${GREEN}[+] Installation complete!${NC}"
