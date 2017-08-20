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

chain_outputs = []
for i in range(len(constants.LABEL_NAMES) + 1):
    y_location = -200 * i

    mask_node = tree.nodes.new(type='CompositorNodeIDMask')
    mask_node.index = i
    mask_node.location = (200, y_location)
    links.new(indexob_output, mask_node.inputs[0])

    multiply_node = tree.nodes.new(type='CompositorNodeMath')
    multiply_node.operation = 'MULTIPLY'
    multiply_node.location = (400, y_location)
    # inputs scaled from 0 to 1, but we want to specify in terms of 0 to 255
    multiply_node.inputs[0].default_value = math.ceil(i / 0.255) / 1000
    links.new(mask_node.outputs[0], multiply_node.inputs[1])

    chain_outputs.append(multiply_node.outputs[0])

adders = []
adders.append(tree.nodes.new(type='CompositorNodeMath'))
adders[0].operation = 'ADD'
adders[0].location = (600, 0)
links.new(chain_outputs[0], adders[0].inputs[0])
links.new(chain_outputs[1], adders[0].inputs[1])

for i in range(2, len(chain_outputs)):
    adders.append(tree.nodes.new(type='CompositorNodeMath'))
    adders[-1].operation = 'ADD'
    adders[-1].location = (600, -200 * (i - 1))
    links.new(adders[-2].outputs[0], adders[-1].inputs[0])
    links.new(chain_outputs[i], adders[-1].inputs[1])

output_node = tree.nodes.new(type='CompositorNodeOutputFile')
output_node.location = (800, 0)
output_node.base_path = OUTPUT_PATH
output_node.format.color_mode = 'RGB'
output_node.file_slots[0].path = IMAGE_PREFIX

output_node.file_slots.new(LABEL_PREFIX)
output_node.file_slots[1].use_node_format = False
output_node.file_slots[1].path = LABEL_PREFIX
output_node.file_slots[1].format.color_mode = 'BW'

links.new(input_node.outputs[0], output_node.inputs[0])
links.new(adders[-1].outputs[0], output_node.inputs[1])


# === SET PASS INDEX ===
for obj in bpy.data.objects:
    label = obj[LABEL_PROP_NAME] if (LABEL_PROP_NAME in obj) else None

    if label in constants.LABEL_NAME_TO_INDEX:
        obj.pass_index = constants.LABEL_NAME_TO_INDEX[label]
        continue
    elif label is not None:
        print('Invalid label "{}" for object "{}"'.format(label, obj.name))

    obj.pass_index = constants.EMPTY_LABEL
