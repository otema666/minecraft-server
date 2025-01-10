#!/bin/bash
screen -S minecraft -d -m java -Xmx2048M -jar paper-1.21.1-128.jar nogui

echo "[+] Server started"
echo "[-] Para ver la consola del servidor, ejecuta el comando 'screen -r minecraft'"