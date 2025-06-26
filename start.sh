#!/usr/bin/env bash
set -euo pipefail

# Verificar si el archivo paper.jar existe
if [[ ! -f paper.jar ]]; then
    echo "[-] Error: El servidor no está instalado. Asegúrate de ejecutar install.sh."
    exit 1
fi

# Valores de RAM
RECOMMENDED_RAM="1024M"

# Menú de selección
echo "¿Cuánta RAM quieres asignar al servidor?"
echo " 1)  512M"
echo " 2) ${RECOMMENDED_RAM} (recomendada)"
echo " 3) 2048M"
echo " 4) Personalizada"
read -rp "Elige una opción [1-4]: " opt

# Si el usuario pulsa ENTER sin escribir nada, usamos la recomendada
if [[ -z "$opt" ]]; then
  opt=2
fi

case "$opt" in
  1) XMX="512M"       ;;
  2) XMX="$RECOMMENDED_RAM" ;;
  3) XMX="2048M"      ;;
  4)
    read -rp "Introduce la cantidad de RAM (ej. 512M, 1G, 1536M): " custom
    if [[ ! "$custom" =~ ^[0-9]+[MG]$ ]]; then
      echo "[-] Valor no válido. Usa formatos como '512M' o '1G'."
      exit 1
    fi
    XMX="$custom"
    ;;
  *)
    echo "[-] Opción inválida. Se usará la recomendada (${RECOMMENDED_RAM})."
    XMX="$RECOMMENDED_RAM"
    ;;
esac

echo "[+] Asignando -Xmx${XMX} al servidor"

# Iniciar el servidor en una nueva sesión de screen
screen -S minecraft -d -m java -Xmx${XMX} -jar paper.jar nogui

echo "[+] Servidor iniciado en la sesión de screen 'minecraft'"
echo "[-] Para ver la consola: screen -r minecraft"
