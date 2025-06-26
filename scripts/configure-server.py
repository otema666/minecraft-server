#!/usr/bin/env python3

import os
import yaml
import re

def get_user_input(prompt, default=None):
    """Obtiene una entrada de usuario con un valor por defecto opcional."""
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        elif default is not None:
            return default
        else:
            print("Este campo no puede estar vacío. Por favor, introduce un valor.")

def optimize_server_properties(file_path, max_players):
    """Optimiza el archivo server.properties."""
    print(f"Optimizando {file_path}...")
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        with open(file_path, 'w') as f:
            for line in lines:
                # Usamos regex para reemplazar las líneas deseadas
                if line.startswith("max-players="):
                    f.write(f"max-players={max_players}\n")
                elif line.startswith("view-distance="):
                    f.write("view-distance=7\n")
                elif line.startswith("simulation-distance="):
                    f.write("simulation-distance=5\n")
                elif line.startswith("entity-broadcast-range-percentage="):
                    f.write("entity-broadcast-range-percentage=50\n")
                elif line.startswith("spawn-protection="):
                    f.write("spawn-protection=0\n")
                elif line.startswith("spawn-animals="):
                    f.write("spawn-animals=false\n")
                elif line.startswith("spawn-npcs="):
                    f.write("spawn-npcs=false\n")
                elif line.startswith("online-mode="):
                    f.write("online-mode=true\n")
                else:
                    f.write(line)
        print(f"-> {file_path} optimizado.")
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {file_path}.")
    except Exception as e:
        print(f"ERROR al optimizar {file_path}: {e}")

def optimize_spigot_yml(file_path):
    """Optimiza el archivo spigot.yml usando PyYAML, preservando las claves existentes."""
    print(f"Optimizando {file_path}...")
    try:
        with open(file_path, 'r') as f:
            spigot_config = yaml.safe_load(f)

        # Asegurarse de que la estructura base exista
        if 'world-settings' not in spigot_config:
            spigot_config['world-settings'] = {}
        if 'default' not in spigot_config['world-settings']:
            spigot_config['world-settings']['default'] = {}

        default_settings = spigot_config['world-settings']['default']

        # --- Modificar/añadir claves simples directamente en default ---
        # Estas claves existían directamente bajo 'default'
        default_settings['mob-spawn-range'] = 4
        default_settings['nerf-spawner-mobs'] = True
        default_settings['tick-inactive-villagers'] = False # Esta se movió de EAR a aquí
        default_settings['mob-spawner-tick-rate'] = 2
        default_settings['arrow-despawn-rate'] = 300
        default_settings['item-despawn-rate'] = 4000

        # --- Modificar o crear bloques complejos, preservando sub-claves ---

        # entity-activation-range
        if 'entity-activation-range' not in default_settings:
            default_settings['entity-activation-range'] = {}
        ear_settings = default_settings['entity-activation-range']
        ear_settings['animals'] = 24
        ear_settings['monsters'] = 24
        ear_settings['raiders'] = 48
        ear_settings['misc'] = 8
        ear_settings['water'] = 8
        ear_settings['villagers'] = 24
        ear_settings['flying-monsters'] = 24
        # El resto de sub-claves (wake-up-inactive, villagers-work-immunity, ignore-spectators)
        # se conservarán si ya existen, ya que solo estamos modificando las claves principales.
        # Si no existen, no se añadirán a menos que se definan aquí explícitamente.

        # entity-tracking-range
        if 'entity-tracking-range' not in default_settings:
            default_settings['entity-tracking-range'] = {}
        etr_settings = default_settings['entity-tracking-range']
        etr_settings['players'] = 96
        etr_settings['animals'] = 48
        etr_settings['monsters'] = 48
        etr_settings['misc'] = 32
        etr_settings['display'] = 64
        etr_settings['other'] = 32

        # merge-radius
        if 'merge-radius' not in default_settings:
            default_settings['merge-radius'] = {}
        merge_settings = default_settings['merge-radius']
        merge_settings['item'] = 2.0
        merge_settings['exp'] = 2.0

        # Guardar los cambios
        with open(file_path, 'w') as f:
            # default_flow_style=False para usar el estilo de bloque (más legible)
            # sort_keys=False para intentar mantener el orden original de las claves
            # indent=2 para una indentación consistente
            yaml.dump(spigot_config, f, default_flow_style=False, indent=2, sort_keys=False)
        print(f"-> {file_path} optimizado.")
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {file_path}. Asegúrate de que el script se ejecuta en el directorio raíz del servidor.")
    except yaml.YAMLError as e:
        print(f"ERROR de sintaxis YAML en {file_path}: {e}")
    except Exception as e:
        print(f"ERROR al optimizar {file_path}: {e}")

def update_minimotd_conf(file_path, max_players):
    """Actualiza la configuración de MiniMOTD."""
    print(f"Actualizando {file_path}...")
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Actualizar max-players
        content = re.sub(r"^\s*max-players=.*", f"max-players={max_players}", content, flags=re.MULTILINE)

        # Reemplazar el bloque motds completo
        new_motds_block = """motds=[
    {
      icon=random
      line1="<blue>Hello <bold><red>¡Bienvenid@s!"
      line2="<italic><gradient:green:yellow>Diviértete"
    }
]"""
        # Encuentra el bloque 'motds=[' y el ']' de cierre
        content = re.sub(r"motds=\[\n.*?\]", new_motds_block, content, flags=re.DOTALL)

        with open(file_path, 'w') as f:
            f.write(content)
        print(f"-> {file_path} actualizado.")
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {file_path}.")
    except Exception as e:
        print(f"ERROR al actualizar {file_path}: {e}")

def update_bluemap_conf(file_path):
    """Actualiza la configuración de BlueMap."""
    print(f"Actualizando {file_path}...")
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        with open(file_path, 'w') as f:
            for line in lines:
                if "accept-download:" in line:
                    f.write("accept-download: true\n")
                else:
                    f.write(line)
        print(f"-> {file_path} (accept-download=true).")
    except FileNotFoundError:
        print(f"ERROR: No se encontró el archivo {file_path}.")
    except Exception as e:
        print(f"ERROR al actualizar {file_path}: {e}")

def main():
    """Función principal para ejecutar el proceso de optimización."""
    # Rutas de los archivos
    PROPS_FILE = "server.properties"
    SPIGOT_FILE = "spigot.yml"
    MOTD_CONF = "plugins/MiniMOTD/main.conf"
    BLUEMAP_CONF = "plugins/BlueMap/core.conf"

    # 0) Comprobación de archivos
    required_files = [PROPS_FILE, SPIGOT_FILE, MOTD_CONF, BLUEMAP_CONF]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print("ERROR: Faltan archivos requeridos para la optimización:")
        for f in missing_files:
            print(f"  - {f}")
        print("Asegúrate de que el script se ejecuta en el directorio raíz del servidor o que las rutas son correctas.")
        exit(1)

    # 1) Solicitar max-players
    max_players_input = get_user_input("Introduce el valor de max-players: ", default="3")
    try:
        max_players = int(max_players_input)
        if max_players <= 0:
            raise ValueError
    except ValueError:
        print("El valor de max-players debe ser un número entero positivo. Usando 3 por defecto.")
        max_players = 20

    # 2) Optimizar server.properties
    optimize_server_properties(PROPS_FILE, max_players)

    # 3) Optimizar spigot.yml
    optimize_spigot_yml(SPIGOT_FILE)

    # 4) Actualizar MiniMOTD
    update_minimotd_conf(MOTD_CONF, max_players)

    # 5) Actualizar BlueMap
    update_bluemap_conf(BLUEMAP_CONF)

    print("\n🎉 ¡Configuración completada y optimizada para rendimiento y jugabilidad!")

if __name__ == "__main__":
    main()