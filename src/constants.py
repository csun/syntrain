LOCAL_MODEL_DIR = 'model'
MOUNTED_MODEL_DIR = '/SegNet'
TRAIN_DIR = 'train'
TEST_DIR = 'test'

EMPTY_LABEL = 16
ORIGINAL_LABEL_MAP = {0: EMPTY_LABEL, 21: 0, 11: 1, 64: 2, 3: 3, 5: 4, 19: 5, 59: 6,
    28: 7, 119: 8, 4: 9, 144: 10, 7: 11, 157: 12, 83: 13, 36: 14, 24: 15}

LABEL_NAMES = ['wall', 'floor', 'picture', 'cabinet', 'chair', 'table',
    'window', 'door', 'pillow', 'ceiling', 'lamp', 'counter', 'bed', 'sofa',
    'desk', 'sink']
LABEL_NAME_TO_INDEX = {name: index for (index, name) in enumerate(LABEL_NAMES)}


IMAGE_SIZE = (480, 360)
