import math
import sys

import h5py
import numpy as np
from PIL import Image

import constants


if len(sys.argv) != 2:
    print('Please provide the path to the nyu dataset .mat file')
    sys.exit(1)


def limit_labels(img):
    def limit_element(element):
        if element not in constants.ORIGINAL_LABEL_MAP:
            return constants.EMPTY_LABEL
        else:
            return constants.ORIGINAL_LABEL_MAP[element]

    return np.matrix([[limit_element(e) for e in row] for row in img], dtype=np.uint8)


mat_file = h5py.File(sys.argv[1], 'r')

MODEL_DIR = 'model/nyu_data'
TRAIN_DIR = 'train'
TEST_DIR = 'test'
MOUNT_POINT = '/SegNet/nyu_data'
IMAGE_COUNT = len(mat_file['images'])
SPLIT = math.ceil(IMAGE_COUNT * 0.8)

train_file = open(MODEL_DIR + '/train.txt', 'w+')
test_file = open(MODEL_DIR + '/test.txt', 'w+')

for i in range(IMAGE_COUNT):
    print(i)
    # Max depth in dataset is 10m - use to normalize values to [0...255]
    normalized_depth = (mat_file['depths'][i] * 25.5).astype(np.uint8)
    stacked = np.concatenate(
            (mat_file['images'][i], np.expand_dims(normalized_depth, 0)), 0)
    labels = limit_labels(mat_file['labels'][i])

    out_dir = TRAIN_DIR
    record_file = train_file
    if i > SPLIT:
        out_dir = TEST_DIR
        record_file = test_file

    img_filename = '{:05d}.png'.format(i)
    label_filename = '{:05d}_label.png'.format(i)

    # The dataset comes with the axes in reverse order - swap these
    # so PIL renders image correctly
    img = Image.fromarray(np.swapaxes(stacked, 0, 2))
    # Note that we use NEAREST when downsampling instead of any other fancy
    # methods to ensure that we maintain perfect correspondence between labels
    # and original pixels.
    img.thumbnail(constants.IMAGE_SIZE, Image.NEAREST)
    img.save('{}/{}/{}'.format(MODEL_DIR, out_dir, img_filename))

    img = Image.fromarray(np.swapaxes(labels, 0, 1))
    img.thumbnail(constants.IMAGE_SIZE, Image.NEAREST)
    img.save('{}/{}/{}'.format(MODEL_DIR, out_dir, label_filename))

    record = '{0}/{1}/{2} {0}/{1}/{3}'.format(MOUNT_POINT, out_dir, img_filename, label_filename)
    print(record, file=record_file)


mat_file.close()
train_file.close()
test_file.close()
