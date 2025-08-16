bl_info = {
	"name": "Update Me",
	"description": "Red Assets Library",
	"author": "Redmoon",
	"version": (1, 0, 2),
	"blender": (4, 0, 0),
	"location": "View 3D > Tool Shelf > Demo Updater",
	"warning": "",
	"wiki_url": "https://github.com/redmoon0/Red-Library",
	"tracker_url": "https://github.com/redmoon0/Red-Library/issues",
	"category": "System"
}
import bpy
from . import updater

owner = "redmoon0"
repo = "Addon_Updator"
class OBJECT_OT_my_button(bpy.types.Operator):
    bl_idname = "object.my_button"
    bl_label = "Update"
    bl_description = "Calls my custom function"

    def execute(self, context):
        updater.get_data_and_run(bl_info=bl_info, module=__name__, owner=owner, repo=repo)
        return {'FINISHED'}


class OBJECT_PT_update(bpy.types.Panel):
    bl_label = "Updating Addon"
    bl_idname = "OBJECT_PT_update"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Update'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.my_button", icon="TRASH")

def run_updater():
    updater.get_data_and_run(bl_info=bl_info, module=__name__, owner=owner, repo=repo)

classes = [OBJECT_OT_my_button, OBJECT_PT_update]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.app.timers.register(run_updater, first_interval=1.0)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
