import bpy
import os
import tempfile

def uninstall_current_and_install_new(addon_module, download_url, repo):
    # Create a temporary Python file
    text = bpy.data.texts.new("temp.py")
    text.write(f"""
import bpy
import tempfile
import os
import zipfile
import requests
import addon_utils
               
# Disable if active
if {repr(addon_module)} in bpy.context.preferences.addons:
    addon_utils.disable({repr(addon_module)}, default_set=True)

# Get addon file path
module = addon_utils.addons_fake_modules.get({repr(addon_module)})
if module and hasattr(module, '__file__'):
    addon_path = os.path.dirname(module.__file__)
    print(f"Removing files at: {{addon_path}}")

    # Delete folder or single file
    if os.path.exists(addon_path):
        import shutil
        shutil.rmtree(addon_path, ignore_errors=True)

# Reload scripts so Blender forgets it
bpy.ops.script.reload()

owner = "redmoon0"
repo = "Addon_Updator"

print({repr(download_url)})
url = {repr(download_url)}
response = requests.get(url, timeout=10)
response.raise_for_status()

download_url = response.json().get("zipball_url")

temp_dir = tempfile.mkdtemp()
zip_path = os.path.join(temp_dir, repo + ".zip")

print("⬇️ Downloading update...")
r = requests.get(download_url, stream=True, timeout=30)
r.raise_for_status()
with open(zip_path, "wb") as f:
    for chunk in r.iter_content(chunk_size=8192):
        f.write(chunk)
bpy.ops.preferences.addon_install(filepath=zip_path, overwrite=True)
if os.path.exists(zip_path):
    os.remove(zip_path)
    print("Zip_Removed")
if os.path.exists(temp_dir):
    os.rmdir(temp_dir)
""")


    bpy.app.timers.register(
            lambda: exec(text.as_string()),
            first_interval=0.5
        )



    
    return {'FINISHED'}
