#!/usr/bin/env python3

import os
import yaml
import re
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

def print_status(message, color=Fore.CYAN):
    """Prints a status message with color."""
    print(color + message + Style.RESET_ALL)

def print_success(message):
    """Prints a success message."""
    print(Fore.GREEN + "-> " + message + Style.RESET_ALL)

def print_error(message):
    """Prints an error message."""
    print(Fore.RED + "ERROR: " + message + Style.RESET_ALL)

def print_warning(message):
    """Prints a warning message."""
    print(Fore.YELLOW + "ADVERTENCIA: " + message + Style.RESET_ALL)

def rcon_passw():
    rpath = "../rcon_password.txt"
    if os.path.exists(rpath):
        with open(rpath, "r") as f:
            return f.read().strip()
    else:
        return "default_password"

def get_user_input(prompt, default=None):
    """Gets user input with an optional default value."""
    while True:
        user_input = input(Fore.YELLOW + prompt + Style.RESET_ALL).strip()
        if user_input:
            return user_input
        elif default is not None:
            return default
        else:
            print_warning("Este campo no puede estar vacío. Por favor, introduce un valor.")

def convert_tabs_to_spaces(file_path, spaces_per_tab=2):
    """
    Reads a file, replaces tabs with spaces, and rewrites it.
    This helps prevent YAML syntax errors caused by tabs.
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        new_content = content.replace('\t', ' ' * spaces_per_tab)

        if new_content != content:
            with open(file_path, 'w') as f:
                f.write(new_content)
            print_success(f"Tabulaciones convertidas a espacios en {file_path}.")
        else:
            print_success(f"No se encontraron tabulaciones en {file_path}.")

    except FileNotFoundError:
        print_warning(f"No se encontró el archivo {file_path} para limpiar tabulaciones.")
    except Exception as e:
        print_error(f"al limpiar tabulaciones en {file_path}: {e}")

def configure_seed(file_path, seed_data):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        with open(file_path, 'w') as f:
            for line in lines:
                if line.startswith("level-seed="):
                    f.write(f"level-seed={seed_data['seed']}\n")
                else:
                    f.write(line)
                
        print_success(f"{file_path} optimizado.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}.")
    except Exception as e:
        print_error(f"al optimizar {file_path}: {e}")

def get_seed_data():
    seeds = [
        {
            "id": "1",
            "nombre": "Cráter Anillo Glaciar",
            "descripcion": "Cráter circular con paredes cubiertas de nieve y hielo. Un paisaje espectacular con vistas impresionantes.",
            "imagen": "https://www.gameskinny.com/wp-content/uploads/2025/01/Minecraft-top-1-21-seeds-Deep-Dark-mountain.jpg",
            "seed": "4826836514737034883",
            "coordenadas": [290, 95, -205],
            "tipo": "❄️  Ártico/Montañas",
            "dificultad": "Media"
        },
        {
            "id": "2",
            "nombre": "Isla de Champiñones",
            "descripcion": "Las Islas de Champiñones son un bioma muy seguro en Minecraft, ya que los mobs hostiles no aparecen de forma natural en sus bloques de Micelio. Ideal para vivir una vida tranquila.",
            "imagen": "https://www.gameskinny.com/wp-content/uploads/2024/12/Minecraft-Best-1-21-seeds-Mushroom-sanctuary.jpg",
            "seed": "-4321675196973609001",
            "coordenadas": [319, 73, -289],
            "tipo": "🍄 Isla/Océano",
            "dificultad": "Fácil"
        },
        {
            "id": "3",
            "nombre": "Lago del Cañón Rojo",
            "descripcion": "Cañón de tonos rojizos con un gran lago azul en su centro, rodeado por paredes de tierra. Perfecto para construcciones.",
            "imagen": "https://www.pcgamesn.com/wp-content/sites/pcgamesn/2024/08/minecraft-seeds-badlands-lake-550x309.jpg",
            "seed": "7598363429859286340",
            "coordenadas": [-123, 118, 24],
            "tipo": "🏜️ Badlands/Mesa",
            "dificultad": "Media"
        }
    ]

    # Header visual mejorado
    print_status("\n" + "="*80, Fore.CYAN)
    print_status("🌱 SELECTOR DE SEMILLAS MINECRAFT 🌱", Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print_status("="*80, Fore.CYAN)
    print_status("Selecciona una semilla para tu mundo:", Fore.YELLOW)
    print_status("="*80 + "\n", Fore.CYAN)

    # Mostrar semillas con mejor formato
    for i, seed in enumerate(seeds):
        # Separador entre semillas
        if i > 0:
            print(Fore.LIGHTBLACK_EX + "─" * 80)
        
        # Número y nombre destacado
        print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}[{seed['id']}] {Fore.LIGHTGREEN_EX + Style.BRIGHT}{seed['nombre']}")
        
        # Tipo y dificultad en línea
        print(f"{Fore.MAGENTA}   🌍 Bioma: {Fore.WHITE}{seed['tipo']} {Fore.MAGENTA}| ⚡ Dificultad: {Fore.WHITE}{seed['dificultad']}")
        
        # Descripción formateada
        print(f"{Fore.YELLOW}   📋 {Fore.WHITE}{seed['descripcion']}")
        
        # Coordenadas destacadas
        coords_str = f"X: {seed['coordenadas'][0]}, Y: {seed['coordenadas'][1]}, Z: {seed['coordenadas'][2]}"
        print(f"{Fore.LIGHTBLUE_EX}   📍 Coordenadas: {Fore.WHITE}{coords_str}")
        
        # Seed ID
        print(f"{Fore.LIGHTBLACK_EX}   🔢 Seed: {seed['seed']}")
        
        print()  # Línea en blanco

    # Separador final
    print_status("="*80, Fore.CYAN)

    while True:
        try:
            print_status("🎯 Selección:", Fore.LIGHTMAGENTA_EX)
            seleccion = input(f"{Fore.YELLOW}➤ Ingresa el número de la semilla deseada (1-{len(seeds)}): {Style.RESET_ALL}")
            seleccion_int = int(seleccion)
            
            # Buscar la semilla seleccionada
            seed_seleccionada = None
            for seed in seeds:
                if int(seed['id']) == seleccion_int:
                    seed_seleccionada = seed
                    break

            if seed_seleccionada:
                # Confirmación visual mejorada
                print_status("\n" + "="*60, Fore.GREEN)
                print_success(f"✅ ¡Semilla seleccionada!")
                print(f"{Fore.LIGHTGREEN_EX}🌱 Mundo: {Fore.WHITE + Style.BRIGHT}{seed_seleccionada['nombre']}")
                print(f"{Fore.LIGHTBLUE_EX}🔢 Seed: {Fore.WHITE}{seed_seleccionada['seed']}")
                print(f"{Fore.LIGHTCYAN_EX}📍 Spawn: {Fore.WHITE}X:{seed_seleccionada['coordenadas'][0]} Y:{seed_seleccionada['coordenadas'][1]} Z:{seed_seleccionada['coordenadas'][2]}")
                print(f"{Fore.MAGENTA}🌍 Tipo: {Fore.WHITE}{seed_seleccionada['tipo']}")
                print_status("="*60 + "\n", Fore.GREEN)
                return seed_seleccionada
            else:
                print_error(f"❌ Número de semilla no válido. Por favor, ingresa un número entre 1 y {len(seeds)}.")
                print()
        except ValueError:
            print_error("❌ Entrada no válida. Por favor, ingresa solo números.")
            print()


def optimize_server_properties(file_path, max_players, RCON_PASSWORD, selected_seed=None):
    """Optimizes the server.properties file."""
    print_status(f"\nOptimizando {file_path}...")
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        with open(file_path, 'w') as f:
            for line in lines:
                if line.startswith("max-players="):
                    f.write(f"max-players={max_players}\n")
                elif line.startswith("view-distance="):
                    f.write("view-distance=11\n")
                elif line.startswith("simulation-distance="):
                    f.write("simulation-distance=7\n")
                elif line.startswith("entity-broadcast-range-percentage="):
                    f.write("entity-broadcast-range-percentage=50\n")
                elif line.startswith("spawn-protection="):
                    f.write("spawn-protection=16\n")
                elif line.startswith("spawn-animals="):
                    f.write("spawn-animals=true\n")
                elif line.startswith("spawn-npcs="):
                    f.write("spawn-npcs=true\n")
                elif line.startswith("online-mode="):
                    f.write("online-mode=false\n")
                elif line.startswith("save-user-cache-on-stop-only="):
                    f.write("save-user-cache-on-stop-only=true\n")
                elif line.startswith("enforce-secure-profile="):
                    f.write("enforce-secure-profile=false\n")
                elif line.startswith("enable-rcon="):
                    f.write(f"enable-rcon=true\n")
                elif line.startswith("rcon.password="):
                    f.write(f"rcon.password={RCON_PASSWORD}\n")
                elif line.startswith("level-seed="):
                    if selected_seed:
                        f.write(f"level-seed={selected_seed['seed']}\n")
                    else:
                        f.write("level-seed=\n")
                else:
                    f.write(line)

        print_success(f"{file_path} optimizado.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}.")
    except Exception as e:
        print_error(f"al optimizar {file_path}: {e}")

def optimize_spigot_yml(file_path):
    """Optimizes the spigot.yml file using PyYAML, preserving existing keys."""
    print_status(f"\nOptimizando {file_path}...")
    convert_tabs_to_spaces(file_path) # Clean tabs before loading
    try:
        with open(file_path, 'r') as f:
            spigot_config = yaml.safe_load(f)

        # Ensure the base structure exists
        if 'world-settings' not in spigot_config:
            spigot_config['world-settings'] = {}
        if 'default' not in spigot_config['world-settings']:
            spigot_config['world-settings']['default'] = {}

        default_settings = spigot_config['world-settings']['default']

        # --- Modify/add simple keys directly in default ---
        default_settings['mob-spawn-range'] = 4
        default_settings['nerf-spawner-mobs'] = True
        default_settings['tick-inactive-villagers'] = False
        default_settings['mob-spawner-tick-rate'] = 2
        default_settings['arrow-despawn-rate'] = 300
        default_settings['item-despawn-rate'] = 4000

        # --- Modify or create complex blocks, preserving sub-keys ---

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

        # Save changes
        with open(file_path, 'w') as f:
            yaml.dump(spigot_config, f, default_flow_style=False, indent=2, sort_keys=False)
        print_success(f"{file_path} optimizado.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}. Asegúrate de que el script se ejecuta en el directorio raíz del servidor.")
    except yaml.YAMLError as e:
        print_error(f"de sintaxis YAML en {file_path}: {e}")
    except Exception as e:
        print_error(f"al optimizar {file_path}: {e}")

def update_minimotd_conf(file_path, max_players):
    """Updates the MiniMOTD configuration."""
    print_status(f"Actualizando {file_path}...")
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Update max-players
        content = re.sub(r"^\s*max-players=.*", f"max-players={max_players}", content, flags=re.MULTILINE)

        # Replace the entire motds block
        new_motds_block = """motds=[
    {
      icon=random
      line1="<blue>Hello <bold><red>¡Bienvenid@s!"
      line2="<italic><gradient:green:yellow>Diviértete"
    }
]"""
        # Find the 'motds=[' block and its closing ']'
        content = re.sub(r"motds=\[\n.*?\]", new_motds_block, content, flags=re.DOTALL)

        with open(file_path, 'w') as f:
            f.write(content)
        print_success(f"{file_path} actualizado.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}.")
    except Exception as e:
        print_error(f"al actualizar {file_path}: {e}")

def optimize_bluemap_maps_conf(file_path):
    """Optimizes the plugins/BlueMap/maps/world.conf file with desired settings."""
    print_status(f"\nOptimizando {file_path} (usando regex)...")
    convert_tabs_to_spaces(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Enable 3D views and high-res, disable flat view
        content = re.sub(r"^\s*enable-perspective-view:.*", "enable-perspective-view: true", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*enable-free-flight-view:.*", "enable-free-flight-view: true", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*enable-hires:.*", "enable-hires: true", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*player-render-limit:\s*.*", "player-render-limit: 1", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*enable-flat-view:.*", "enable-flat-view: false", content, flags=re.MULTILINE)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"{file_path} optimizado.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}.")
    except Exception as e:
        print_error(f"Error al optimizar {file_path}: {e}")

def optimize_bluemap_core_conf(file_path):
    """Optimizes the plugins/BlueMap/core.conf file using regex."""
    print_status(f"\nOptimizando {file_path} (usando regex)...")
    convert_tabs_to_spaces(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Core settings
        content = re.sub(r"^\s*accept-download:.*", "accept-download: true", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*render-thread-count:.*", "render-thread-count: 4", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*scan-for-mod-resources:.*", "scan-for-mod-resources: false", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*metrics:.*", "metrics: false", content, flags=re.MULTILINE)
        content = re.sub(r"^\s*log:\s*\{.*?\}", "log: {}", content, flags=re.MULTILINE | re.DOTALL)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print_success(f"{file_path} optimizado.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}.")
    except Exception as e:
        print_error(f"Error al optimizar {file_path}: {e}")

def optimize_bluemap_plugin_conf(file_path):
    print_status(f"\nOptimizando plugin config: {file_path}")
    convert_tabs_to_spaces(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        output = []
        for line in lines:
            if line.startswith("live-player-markers:"):
                output.append("live-player-markers: true\n")
            elif line.startswith("hidden-game-modes:"):
                output.append('hidden-game-modes: ["spectator"]\n')
            elif line.startswith("hide-vanished:"):
                output.append("hide-vanished: true\n")
            elif line.startswith("hide-invisible:"):
                output.append("hide-invisible: true\n")
            elif line.startswith("hide-sneaking:"):
                output.append("hide-sneaking: true\n")
            elif line.startswith("hide-below-sky-light:"):
                output.append("hide-below-sky-light: 0\n")
            elif line.startswith("hide-below-block-light:"):
                output.append("hide-below-block-light: 0\n")
            elif line.startswith("hide-different-world:"):
                output.append("hide-different-world: true\n")
            elif line.startswith("write-markers-interval:"):
                output.append("write-markers-interval: 0\n")
            elif line.startswith("write-players-interval:"):
                output.append("write-players-interval: 0\n")
            elif line.startswith("skin-download:"):
                output.append("skin-download: false\n")
            elif line.startswith("player-render-limit:"):
                output.append("player-render-limit: 1\n")
            elif line.startswith("full-update-interval:"):
                output.append("full-update-interval: 2880\n")
            else:
                output.append(line)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(output)
        print_success(f"Plugin config optimized: {file_path}")
    except Exception as e:
        print_error(f"Error optimizing plugin config {file_path}: {e}")

def optimize_bluemap_webserver_conf(file_path):
    """Optimizes the plugins/BlueMap/webserver.conf file by removing the log block."""
    print_status(f"\nOptimizando {file_path} (desactivando logs)...")
    convert_tabs_to_spaces(file_path) # Ensure no tabs before reading

    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Regex to target the entire 'log:' block and replace it with an empty block.
        # This is the safest way to "disable" logging completely without causing YAML errors.
        #content = re.sub(r"^\s*log:.*?(?=\n\S|\Z)", "log: {}", content, flags=re.MULTILINE | re.DOTALL)
        content = re.sub(r"^\s*log:\s*\{.*?\}", "log: {}", content, flags=re.MULTILINE | re.DOTALL)


        with open(file_path, 'w') as f:
            f.write(content)
        print_success(f"Logs de webserver deshabilitados en {file_path}.")
    except FileNotFoundError:
        print_error(f"No se encontró el archivo {file_path}.")
    except Exception as e:
        print_error(f"al optimizar {file_path}: {e}")

def configure_tab_plugin(config_path, groups_path):
    # --- Configurar config.yml ---
    print_status(f"\nOptimizando '{config_path}'...")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
    except FileNotFoundError:
        print_error(f"Error: El archivo '{config_path}' no se encontró.")
        return
    except yaml.YAMLError as e:
        print_error(f"Error al parsear '{config_path}': {e}")
        return

    cfg['header-footer'] = {
        'enabled': True,
        'header': [],
        'footer': ["&7Memoria usada: %memory-used% MB / %memory-max% MB"],
        'disable-condition': '%world%=disabledworld'
    }

    if "playerlist-objective" not in cfg:
        cfg["playerlist-objective"] = {}
    cfg["playerlist-objective"]["enabled"] = False
    cfg["playerlist-objective"]["value"] = "%ping%"
    cfg["playerlist-objective"]["fancy-value"] = "&7Ping: %ping%"
    cfg["playerlist-objective"]["disable-condition"] = "%world%=disabledworld"

    if "belowname-objective" not in cfg:
        cfg["belowname-objective"] = {}
    cfg["belowname-objective"]["enabled"] = False
    cfg["belowname-objective"]["value"] = "%health%"
    cfg["belowname-objective"]["title"] = "&cHealth"
    cfg["belowname-objective"]["fancy-value"] = "&c%health%"
    cfg["belowname-objective"]["fancy-value-default"] = "NPC"
    cfg["belowname-objective"]["disable-condition"] = "%world%=disabledworld"

    if "layout" not in cfg:
        cfg["layout"] = {}
    cfg["layout"]["enabled"] = False
    cfg["layout"]["direction"] = "COLUMNS"
    cfg["layout"]["default-skin"] = "mineskin:383747683"
    cfg["layout"]["enable-remaining-players-text"] = True
    cfg["layout"]["remaining-players-text"] = "... and %s more"
    cfg["layout"]["empty-slot-ping-value"] = 1000
    if "layouts" not in cfg["layout"]:
        cfg["layout"]["layouts"] = {}
    if "default" not in cfg["layout"]["layouts"]:
        cfg["layout"]["layouts"]["default"] = {}
    if "fixed-slots" not in cfg["layout"]["layouts"]["default"]:
        cfg["layout"]["layouts"]["default"]["fixed-slots"] = []
    if "groups" not in cfg["layout"]["layouts"]["default"]:
        cfg["layout"]["layouts"]["default"]["groups"] = {}

    if "scoreboard-teams" in cfg:
        cfg["scoreboard-teams"]["enabled"] = False
    else:
        cfg["scoreboard-teams"] = {"enabled": False}

    if "placeholders" in cfg:
        cfg["placeholders"]["register-tab-expansion"] = True
        if "date-format" not in cfg["placeholders"]:
            cfg["placeholders"]["date-format"] = "dd.MM.yyyy"
        if "time-format" not in cfg["placeholders"]:
            cfg["placeholders"]["time-format"] = "[HH:mm:ss / h:mm a]"
        if "time-offset" not in cfg["placeholders"]:
            cfg["placeholders"]["time-offset"] = 0
    else:
        cfg["placeholders"] = {
            "register-tab-expansion": True,
            "date-format": "dd.MM.yyyy",
            "time-format": "[HH:mm:ss / h:mm a]",
            "time-offset": 0
        }

    new_refresh_intervals = {
        "default-refresh-interval": 500,
        "%healthbar_getbar%": 200,
        "%ping%": 1000
    }
    cfg["placeholderapi-refresh-intervals"] = new_refresh_intervals

    # Guardar los cambios en config.yml
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(cfg, f, sort_keys=False, allow_unicode=True, indent=2)
        print_success(f"'{config_path}' ha sido actualizado exitosamente.")
    except IOError as e:
        print_error(f"Error de E/S al escribir en '{config_path}': {e}")
        return

    # --- Configurar groups.yml ---
    try:
        with open(groups_path, 'r', encoding='utf-8') as f:
            groups_data = yaml.safe_load(f)
    except FileNotFoundError:
        print_error(f"Error: El archivo '{groups_path}' no se encontró.")
        return
    except yaml.YAMLError as e:
        print_error(f"Error al parsear '{groups_path}': {e}")
        return

    if "_DEFAULT_" in groups_data:
        groups_data["_DEFAULT_"].update({
            "tabprefix": "",
            "customtabname": "&f%player% %healthbar_getbar%",
            "tabsuffix": " &3%ping%ms"
        })
    else:
        print_error("Advertencia: La sección '_DEFAULT_' no se encontró en groups.yml. No se pudo actualizar.")

    try:
        with open(groups_path, 'w', encoding='utf-8') as f:
            yaml.dump(groups_data, f, sort_keys=False, allow_unicode=True, indent=2)
        print_success(f"'{groups_path}' ha sido actualizado exitosamente.")
    except IOError as e:
        print_error(f"Error de E/S al escribir en '{groups_path}': {e}")
        return

    print()
    os.system('echo "==============================================================================" | lolcat')
    print(f"""{Fore.RED}{Style.BRIGHT}\t\t\t¡¡¡IMPORTANTE!!!{Style.RESET_ALL}\n
    {Fore.YELLOW}Debes ejecutar {Fore.BLUE}'papi ecloud download HealthBar'{Fore.YELLOW} al iniciar el servidor si todavía no lo has hecho.
    Seguidamente ejecuta:
    {Fore.BLUE}'papi reload'{Fore.YELLOW} y {Fore.BLUE}'tab reload'{Fore.YELLOW}.
    """)
    os.system('echo "==============================================================================" | lolcat')


def main():
    """Main function to run the optimization process."""
    os.system('clear')
    
    # Header visual mejorado para el inicio
    print()
    print_status("=" * 80, Fore.LIGHTCYAN_EX)
    print_status("🚀 CONFIGURADOR DE SERVIDOR MINECRAFT 🚀", Fore.LIGHTMAGENTA_EX + Style.BRIGHT)
    print_status("=" * 80, Fore.LIGHTCYAN_EX)
    print_status("🔧 Iniciando proceso de optimización automática...", Fore.YELLOW)
    print_status("=" * 80, Fore.LIGHTCYAN_EX)

    # File paths
    PROPS_FILE = "server.properties"
    SPIGOT_FILE = "spigot.yml"
    MOTD_CONF = "plugins/MiniMOTD/main.conf"
    BLUEMAP_PLUGIN_CONF = "plugins/BlueMap/plugin.conf"
    BLUEMAP_CORE_CONF = "plugins/BlueMap/core.conf"
    BLUEMAP_WEBSERVER_CONF = "plugins/BlueMap/webserver.conf"
    BLUEMAP_WORLD_CONF = "plugins/BlueMap/maps/world.conf"
    TAB_CONF = "plugins/TAB/config.yml"
    TAB_GROUPS_CONF = "plugins/TAB/groups.yml"

    print_status("\n🔍 Verificando archivos requeridos...", Fore.LIGHTYELLOW_EX)
    required_files = [PROPS_FILE, SPIGOT_FILE, MOTD_CONF, BLUEMAP_PLUGIN_CONF, BLUEMAP_CORE_CONF, BLUEMAP_WEBSERVER_CONF, BLUEMAP_WORLD_CONF, TAB_CONF, TAB_GROUPS_CONF]
    missing_files = [f for f in required_files if not os.path.exists(f)]

    if missing_files:
        print_error("❌ Faltan archivos requeridos para la optimización:")
        for f in missing_files:
            print_error(f"  📄 {f}")
        print_error("⚠️  Asegúrate de que el script se ejecuta en el directorio raíz del servidor o que las rutas son correctas.")
        exit(1)
    print_success("✅ Todos los archivos requeridos encontrados.")

    # Sección de configuración de usuario
    print_status("\n📋 CONFIGURACIÓN INICIAL", Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print_status("─" * 50, Fore.LIGHTGREEN_EX)
    
    max_players_input = get_user_input("👥 Introduce el valor de max-players (por defecto: 3): ", default="3")
    RCON_PASSWORD = get_user_input("🔐 Introduce la contraseña de RCON: ", default=rcon_passw())
    o = get_user_input("🌱 ¿Deseas usar una semilla personalizada? (y/n): ", default="n").strip().lower()
    selected_seed = None
    if o == 'y':
        selected_seed = get_seed_data()

    try:
        max_players = int(max_players_input)
        if max_players <= 0:
            raise ValueError
    except ValueError:
        print_warning("El valor de max-players debe ser un número entero positivo. Usando 3 por defecto.")
        max_players = 3

    optimize_server_properties(PROPS_FILE, max_players, RCON_PASSWORD, selected_seed)
    optimize_spigot_yml(SPIGOT_FILE)
    update_minimotd_conf(MOTD_CONF, max_players)
    optimize_bluemap_plugin_conf(BLUEMAP_PLUGIN_CONF)
    optimize_bluemap_core_conf(BLUEMAP_CORE_CONF)
    optimize_bluemap_webserver_conf(BLUEMAP_WEBSERVER_CONF)
    optimize_bluemap_maps_conf(BLUEMAP_WORLD_CONF)

    configure_tab_plugin(TAB_CONF, TAB_GROUPS_CONF)

    # Mensaje de finalización mejorado
    print_status("\n" + "=" * 80, Fore.LIGHTGREEN_EX)
    print_status("🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE! 🎉", Fore.LIGHTGREEN_EX + Style.BRIGHT)
    print_status("=" * 80, Fore.LIGHTGREEN_EX)
    print_success("✅ Servidor optimizado para rendimiento y jugabilidad")
    print_success("✅ Configuraciones aplicadas correctamente")
    print_success("✅ ¡Tu servidor está listo para funcionar!")
    print_status("=" * 80 + "\n", Fore.LIGHTGREEN_EX)

if __name__ == "__main__":
    main()