#!/bin/bash
screen -S minecraft -d -m java -Xmx2048M -jar paper.jar nogui

echo "[+] Server started"
echo "[-] Para ver la consola del servidor, ejecuta el comando 'screen -r minecraft'"