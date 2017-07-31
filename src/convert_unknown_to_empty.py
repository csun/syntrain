# NOTE - this is a short, hacky script intended to change some labels around
# without regenerating all images. You should not need to run this.
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
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if pixels[i,j] > constants.EMPTY_LABEL:
                pixels[i,j] = constants.EMPTY_LABEL


mat_file = h5py.File(sys.argv[1], 'r')

MODEL_DIR = 'model/nyu_data'
TRAIN_DIR = 'train'
TEST_DIR = 'test'
MOUNT_POINT = '/SegNet/nyu_data'
IMAGE_COUNT = len(mat_file['images'])
SPLIT = math.ceil(IMAGE_COUNT * 0.8)

for i in range(IMAGE_COUNT):
    print(i)

    out_dir = TRAIN_DIR
    if i > SPLIT:
        out_dir = TEST_DIR

    label_filename = '{:05d}_label.png'.format(i)

    img = Image.open('{}/{}/{}'.format(MODEL_DIR, out_dir, label_filename))
    limit_labels(img)
    img.save('{}/{}/{}'.format(MODEL_DIR, out_dir, label_filename))


mat_file.close()
