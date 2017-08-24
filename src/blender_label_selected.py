import bpy
import constants

bl_info = {'name': 'Label Selected (syntrain)', 'category': 'Object'}

class LabelSelected(bpy.types.Operator):
    bl_idname = 'object.label_selected'        # unique identifier for buttons and menu items to reference.
    bl_label = 'Add label to all selected items'         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    label = bpy.props.EnumProperty(
                name='Label',
                items=[(label, label, '') for label in constants.LABEL_NAMES])

    def execute(self, context):        # execute() is called by blender when running the operator.
        for obj in bpy.context.selected_objects:
            obj['label'] = self.label

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

def register():
    bpy.utils.register_class(LabelSelected)

def unregister():
    bpy.utils.unregister_class(LabelSelected)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == '__main__':
    register()
