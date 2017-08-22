import math
import bpy

# TODO make shell script that runs something like the following except
# renders all frames.
#    blender --background /hdd/syn_scene_assets/scenes/nodes_sample.blend --render-frame 1
import constants


OUTPUT_PATH = '//render/'
IMAGE_PREFIX = 'image_'
LABEL_PREFIX = 'label_'
LABEL_PROP_NAME = 'label'


# === RENDER SETTINGS ===
scene = bpy.context.scene

(scene.render.resolution_x, scene.render.resolution_y) = constants.IMAGE_SIZE
scene.render.filepath = OUTPUT_PATH + IMAGE_PREFIX
scene.render.image_settings.color_mode = 'RGB'
scene.use_nodes = True

if len(scene.render.layers) != 1:
    print('Warning - more than one render layer in scene. Output may be wrong.')
scene.render.layers.active.use_pass_object_index = True


# === COMPOSITING NODES ===
tree = scene.node_tree
links = tree.links

input_node = tree.nodes.new(type='CompositorNodeRLayers')
input_node.location = (0, 0)
input_node.scene = scene

indexob_output = None
for output in input_node.outputs:
    if output.name == 'IndexOB':
        indexob_output = output
        break

divide_node = tree.nodes.new(type='CompositorNodeMath')
divide_node.operation = 'DIVIDE'
divide_node.location = (200, 0)
# inputs scaled from 0 to 1, but we want to specify in terms of 0 to 255
links.new(indexob_output, divide_node.inputs[0])
divide_node.inputs[1].default_value = 255

output_node = tree.nodes.new(type='CompositorNodeOutputFile')
output_node.location = (400, 0)
output_node.base_path = OUTPUT_PATH
output_node.format.color_mode = 'RGB'
output_node.file_slots[0].path = IMAGE_PREFIX

output_node.file_slots.new(LABEL_PREFIX)
output_node.file_slots[1].use_node_format = False
output_node.file_slots[1].path = LABEL_PREFIX
output_node.file_slots[1].format.color_mode = 'BW'

links.new(input_node.outputs[0], output_node.inputs[0])
links.new(divide_node.outputs[0], output_node.inputs[1])


# === SET PASS INDEX ===
for obj in bpy.data.objects:
    label = obj[LABEL_PROP_NAME] if (LABEL_PROP_NAME in obj) else None

    if label in constants.LABEL_NAME_TO_INDEX:
        obj.pass_index = constants.LABEL_NAME_TO_INDEX[label]
        continue
    elif label is not None:
        print('Invalid label "{}" for object "{}"'.format(label, obj.name))

    obj.pass_index = constants.EMPTY_LABEL
