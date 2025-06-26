#!/usr/bin/env python3

# Requires: pip install requests pyyaml

import re
import zipfile
import shutil
import requests
import yaml
from pathlib import Path
from datetime import datetime

# --- Configuration ---
# Directory where your PaperMC plugins are located
PLUGINS_DIR = Path("plugins")

# Root directory for plugin backups. A subdirectory named with the current timestamp
# will be created inside this root for each run.
BACKUP_ROOT = Path("plugin_backups") / datetime.now().strftime("%Y-%m-%d_%H%M%S")

# Full Minecraft version string (e.g., "1.21.1")
MC_PREFIX_FULL = "1.21.1"
# Derived Minecraft series (e.g., "1.21") used for Hangar compatibility checks
MC_SERIES = ".".join(MC_PREFIX_FULL.split(".", 2)[:2])

# Hangar API base URL
HANGAR_API = "https://hangar.papermc.io/api/v1"
# Hangar CDN base URL for direct file downloads
HANGAR_CDN = "https://hangarcdn.papermc.io"

# Manual mapping of detected plugin names to Hangar (namespace, slug)
# Add your plugins here if the automatic detection isn't sufficient
# or if the name in the JAR doesn't match the Hangar slug.
# Example: "Chunky": ("pop4959", "Chunky") -> Plugin named "Chunky" by user "pop4959" with slug "Chunky"
PLUGIN_MAP = {
    "Chunky": ("pop4959", "Chunky"),
    "BlueMap": ("Blue", "BlueMap"),
    # Add more plugins here as needed:
    # "YourPluginName": ("HangarNamespace", "HangarSlug"),
}

# --- Functions ---

def get_latest_hangar_version(ns: str, slug: str, mc_series: str) -> dict | None:
    """
    Fetches the latest compatible 'Release' version data for a plugin from Hangar.

    Args:
        ns (str): The Hangar project namespace (user/organization name).
        slug (str): The Hangar project slug (URL-friendly name).
        mc_series (str): The Minecraft series (e.g., "1.21") to check compatibility against.

    Returns:
        dict | None: A dictionary containing the latest version data if found and compatible,
                     otherwise None.
    """
    slug_lower = slug.lower()
    url = f"{HANGAR_API}/projects/{ns}/{slug_lower}/versions/latest?channel=Release"
    try:
        response = requests.get(url)
        # If the project or version is not found, Hangar returns 404
        if response.status_code == 404:
            print(f"    No latest 'Release' version found on Hangar for {ns}/{slug_lower}.")
            return None
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        latest = response.json()

        # Check if the platform is PAPER
        if latest.get("platform") != "PAPER":
            print(f"    Incompatible platform for {ns}/{slug}: Expected 'PAPER', got '{latest.get('platform', 'N/A')}'.")
            return None

        # Check Minecraft version compatibility
        compatible = False
        for mc_version in latest.get("minecraftVersions", []):
            if mc_version.startswith(mc_series):
                compatible = True
                break
        if not compatible:
            print(f"    No compatible Minecraft version found for {ns}/{slug}. Required series: {mc_series}. Available: {', '.join(latest.get('minecraftVersions', []))}.")
            return None

        return latest
    except requests.exceptions.RequestException as e:
        print(f"  Error fetching latest Hangar version for {ns}/{slug}: {e}")
        return None
    except ValueError as e: # For JSON decoding errors
        print(f"  Error parsing Hangar API response for {ns}/{slug}: {e}")
        return None


def main():
    """
    Main function to automate PaperMC plugin updates.
    """
    # 1. Create backup directory
    try:
        BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
        print(f"Created backup directory: {BACKUP_ROOT}")
    except OSError as e:
        print(f"Error creating backup directory {BACKUP_ROOT}: {e}. Exiting.")
        return

    # 2. Process each JAR file in the plugins directory
    if not PLUGINS_DIR.exists():
        print(f"Plugins directory '{PLUGINS_DIR}' not found. Please ensure it exists.")
        return
    if not PLUGINS_DIR.is_dir():
        print(f"'{PLUGINS_DIR}' is not a directory. Please provide a valid plugins directory.")
        return

    plugin_jars = sorted(PLUGINS_DIR.glob("*.jar"))
    if not plugin_jars:
        print(f"No .jar files found in '{PLUGINS_DIR}'.")
        return

    for jar_path in plugin_jars:
        print(f"\n--- Processing: {jar_path.name} ---")
        plugin_name = None
        local_version = None
        current_jar_stem = jar_path.stem

        # Attempt to detect plugin name and version from filename
        # Regex: captures anything before the last dash as name, and everything after as version
        # Version regex: (\d+(?:\.[0-9A-Za-z\-]+)*) matches digits, then optionally non-digits, hyphens, and more digits/alphas.
        filename_match = re.match(r"^(.+)-(\d+(?:\.[0-9A-Za-z\-]+)*)$", current_jar_stem)
        if filename_match:
            plugin_name, local_version = filename_match.groups()
            print(f"  Detected from filename: Name='{plugin_name}', Version='{local_version}'")
        else:
            # If filename parsing fails, try reading plugin.yml inside the JAR
            try:
                with zipfile.ZipFile(jar_path, 'r') as jar_zip:
                    # Check if plugin.yml exists in the JAR
                    if 'plugin.yml' in jar_zip.namelist():
                        with jar_zip.open('plugin.yml') as yml_file:
                            plugin_info = yaml.safe_load(yml_file)
                            plugin_name = plugin_info.get('name')
                            local_version = plugin_info.get('version')
                        if plugin_name and local_version:
                            print(f"  Detected from plugin.yml: Name='{plugin_name}', Version='{local_version}'")
                        else:
                            print(f"  Warning: Could not find 'name' or 'version' in plugin.yml for {jar_path.name}. Skipping.")
                            continue
                    else:
                        print(f"  Warning: No plugin.yml found inside {jar_path.name}. Skipping.")
                        continue
            except (zipfile.BadZipFile, KeyError, yaml.YAMLError, FileNotFoundError) as e:
                # Catch errors related to zip file corruption, missing plugin.yml entries, or YAML parsing issues
                print(f"  Warning: Could not parse {jar_path.name} (Error: {e}). Skipping.")
                continue

        # Ensure we have a plugin name and version
        if not plugin_name or not local_version:
            print(f"  Warning: Could not determine plugin name or local version for {jar_path.name}. Skipping.")
            continue

        # 3. Check against PLUGIN_MAP for Hangar mapping
        if plugin_name not in PLUGIN_MAP:
            print(f"  Plugin '{plugin_name}' is not in PLUGIN_MAP. Please add `'{plugin_name}': ('HangarNamespace', 'HangarSlug'),` to PLUGIN_MAP to enable updates for this plugin. Skipping.")
            continue

        ns, slug = PLUGIN_MAP[plugin_name]
        print(f"  Mapped to Hangar: Namespace='{ns}', Slug='{slug}'")

        # 4. Fetch latest Hangar version
        print(f"  Fetching latest compatible Hangar version for {ns}/{slug} (MC Series: {MC_SERIES})...")
        latest_hangar_data = get_latest_hangar_version(ns, slug, MC_SERIES)

        if not latest_hangar_data:
            print(f"  No compatible release found on Hangar for {plugin_name}.")
            continue

        remote_ver = latest_hangar_data["name"]
        file_name = latest_hangar_data["fileName"]
        # Construct the download URL using CDN
        download_url = f"{HANGAR_CDN}/plugins/{ns}/{slug}/versions/{remote_ver}/PAPER/{file_name}"

        print(f"  Local version: {local_version}, Remote Hangar version: {remote_ver}")

        # 5. Compare versions and download if newer
        if remote_ver == local_version:
            print(f"  {plugin_name} is already up-to-date (version {local_version}).")
        else:
            print(f"  Update available for {plugin_name}: {local_version} -> {remote_ver}")
            backup_path = BACKUP_ROOT / jar_path.name
            print(f"  Backing up current plugin '{jar_path.name}' to '{backup_path}'...")
            try:
                shutil.copyfile(jar_path, backup_path)
                print("  Backup successful.")
            except IOError as e:
                print(f"  Error backing up {jar_path.name}: {e}. Skipping update for this plugin.")
                continue

            print(f"  Downloading new version from: {download_url}")
            try:
                # Use stream=True to handle large files efficiently
                response = requests.get(download_url, stream=True)
                response.raise_for_status()  # Raise HTTPError for bad status codes

                # Overwrite the original JAR file with the new one
                with open(jar_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"  Successfully downloaded and updated {jar_path.name} to version {remote_ver}.")
            except requests.exceptions.RequestException as e:
                print(f"  Error downloading new version for {plugin_name}: {e}. Attempting to restore backup.")
                try:
                    shutil.copyfile(backup_path, jar_path)
                    print("  Backup restored successfully.")
                except IOError as restore_e:
                    print(f"  CRITICAL ERROR: Failed to restore backup for {plugin_name} after download failure: {restore_e}")
            except IOError as e:
                print(f"  Error writing new JAR file for {plugin_name}: {e}. Attempting to restore backup.")
                try:
                    shutil.copyfile(backup_path, jar_path)
                    print("  Backup restored successfully.")
                except IOError as restore_e:
                    print(f"  CRITICAL ERROR: Failed to restore backup for {plugin_name} after write failure: {restore_e}")

# --- Main Guard ---
if __name__ == "__main__":
    main()
