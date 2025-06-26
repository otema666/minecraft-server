#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'
RED='\033[0;31m'

# Actualizar el sistema
echo -e "${GREEN}[+] Updating package list...${NC}"
sudo apt update

# Actualizar paquetes instalados
echo -e "${GREEN}[+] Upgrading installed packages...${NC}"
sudo apt upgrade -y

# Instalar OpenJDK 21 solo si no está instalado
if dpkg -s openjdk-21-jdk &>/dev/null; then
  echo -e "${GREEN}[+] OpenJDK 21 is already installed, skipping.${NC}"
else
  echo -e "${GREEN}[+] Installing OpenJDK 21...${NC}"
  sudo apt install -y software-properties-common
  sudo add-apt-repository ppa:openjdk-r/ppa -y
  sudo apt update
  sudo apt install -y openjdk-21-jdk
fi


# Configurar Java predeterminado (opcional)
#sudo update-alternatives --config java

# Descargar el archivo JAR de PaperMC (última build de la versión)
echo -e "${GREEN}[+] Downloading latest PaperMC server jar...${NC}"
VERSION="1.21.1"
API_URL="https://api.papermc.io/v2/projects/paper/versions/${VERSION}/builds"

# 1) Descargamos el JSON de builds
JSON=$(wget -qO- "$API_URL")

# 2) Extraemos el nombre del último JAR (p.ej. paper-1.21.1-128.jar)
JAR_NAME=$(echo "$JSON" \
  | grep -Po '"name":"\Kpaper-'${VERSION}'-[0-9]+\.jar' \
  | tail -n1)

# 3) Obtenemos el número de build
BUILD_NUM=$(echo "$JAR_NAME" \
  | sed -E "s/paper-${VERSION}-([0-9]+)\.jar/\1/")

# Validación rápida
if [[ -z "$JAR_NAME" || -z "$BUILD_NUM" ]]; then
  echo -e "${RED}[!] Error: no se pudo determinar el JAR o el build.${NC}"
  exit 1
fi

# 4) Construimos la URL y descargamos
DOWNLOAD_URL="https://api.papermc.io/v2/projects/paper/versions/${VERSION}/builds/${BUILD_NUM}/downloads/${JAR_NAME}"
wget -qO paper.jar "$DOWNLOAD_URL"

echo -e "${GREEN}[+] Downloaded ${JAR_NAME}${NC}"

# Aceptar el EULA
echo "eula=true" > eula.txt

echo -e "${GREEN}[+] Installation complete!${NC}"
