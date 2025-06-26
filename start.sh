#!/bin/bash

# Verificar si el archivo paper.jar existe
if [ ! -f paper.jar ]; then
    echo "[-] Error: El servidor no está instalado. Asegúrate de ejecutar install.sh."
    exit 1
fi

# Iniciar el servidor en una nueva sesión de screen
screen -S minecraft -d -m java -Xmx2048M -jar paper.jar nogui

echo "[+] Servidor iniciado"
echo "[-] Para ver la consola del servidor, ejecuta el comando 'screen -r minecraft'"
