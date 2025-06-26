#!/bin/bash

# Directorios
PLUGINS_DIR="plugins"
DEACTIVATED_DIR="deactivated_plugins"

# Crear el directorio de desactivados si no existe
mkdir -p "$DEACTIVATED_DIR"

# Función para mostrar la lista de plugins
mostrar_plugins() {
    clear
    echo -e "\n\033[1;34m=== Plugins Activos ===\033[0m"
    local active_found=false
    for plugin in "$PLUGINS_DIR"/*.jar; do
        if [[ -f "$plugin" ]]; then
            echo -e "\e[32m$(basename "$plugin")\e[0m"
            active_found=true
        fi
    done
    if ! $active_found; then
        echo -e "\e[31mNo hay plugins activos.\e[0m"
    fi

    echo -e "\n\033[1;31m=== Plugins Desactivados ===\033[0m"
    local deactivated_found=false
    for plugin in "$DEACTIVATED_DIR"/*.jar; do
        if [[ -f "$plugin" ]]; then
            echo -e "\e[31m$(basename "$plugin")\e[0m"
            deactivated_found=true
        fi
    done
    if ! $deactivated_found; then
        echo -e "\e[32mNo hay plugins desactivados.\e[0m"
    fi
}

# Función para desactivar un plugin
desactivar_plugin() {
    local plugin_name="$1"
    local plugin_path="$PLUGINS_DIR/$plugin_name"

    if [[ -f "$plugin_path" ]]; then
        mv "$plugin_path" "$DEACTIVATED_DIR/"
        echo -e "\nPlugin '\e[32m$plugin_name\e[0m' desactivado."
    else
        echo -e "\nPlugin '\e[31m$plugin_name\e[0m' no encontrado."
    fi
}

# Menú principal
while true; do
    mostrar_plugins
    echo -e "\n\033[1;34mOpciones:\033[0m"
    echo "1. Desactivar un plugin"
    echo "2. Salir"
    echo
    read -p "Selecciona una opción: " opcion

    case $opcion in
        1)
            read -p "Introduce el nombre del plugin a desactivar (sin .jar): " plugin_name
            desactivar_plugin "$plugin_name.jar"
            read -p "Presiona Enter para continuar..."
            ;;
        2)
            echo "Saliendo..."
            exit 0
            ;;
        *)
            echo -e "\n\033[31mOpción no válida. Intenta de nuevo.\033[0m"
            read -p "Presiona Enter para continuar..."
            ;;
    esac
done
