import requests
import zipfile
import os
import bpy
import tempfile
from . import uninstall_script as uninstall

def get_data_and_run(bl_info, module, owner, repo): 
    version_tuple = bl_info.get('version', (0,0,0))
    current_version = f"v{version_tuple[0]}.{version_tuple[1]}.{version_tuple[2]}"

    print("🛠 RigACar Checking For Updates...")

    try:
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # network error handling
    except requests.RequestException as e:
        print(f"⚠️ Failed to fetch latest release info: {e}")
        return

    latest_version = get_latest_version(response)
    if not latest_version:
        print("⚠️ Could not determine latest version.")
        return

    try:
        update_available = compare_versions(current_version, latest_version)
    except Exception as e:
        print(f"⚠️ Version comparison failed: {e}")
        return

    if update_available:
        print(f"🔔 Update available! Latest version: {latest_version}")
        uninstall.uninstall_current_and_install_new(addon_module=module, download_url=url, repo=repo)


    else:
        print("✅ Addon is up-to-date.")


def get_latest_version(response):
    try:
        if response.status_code == 200:
            release = response.json()
            return release.get("tag_name")
        else:
            print(f"⚠️ GitHub API returned error code {response.status_code}")
    except Exception as e:
        print(f"⚠️ Failed to parse latest version: {e}")
    return None


def compare_versions(current_version, latest_version):
    try:
        current_version = current_version.lstrip('v')
        latest_version = latest_version.lstrip('v')
        current_tuple = tuple(map(int, current_version.split(".")))
        latest_tuple = tuple(map(int, latest_version.split(".")))
        return current_tuple < latest_tuple
    except Exception as e:
        print(f"⚠️ Error comparing versions: {e}")
        return False
