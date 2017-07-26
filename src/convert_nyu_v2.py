import math
import sys

import h5py
import numpy as np
from PIL import Image


if len(sys.argv) != 2:
    print('Please provide the path to the nyu dataset .mat file')
    sys.exit(1)


mat_file = h5py.File(sys.argv[1], 'r')

MODEL_DIR = 'model/nyu_data'
TRAIN_DIR = MODEL_DIR + '/train'
TEST_DIR = MODEL_DIR + '/test'
MOUNT_POINT = '/SegNet'
IMAGE_COUNT = len(mat_file['images'])
SPLIT = math.ceil(IMAGE_COUNT * 0.8)

train_file = open(MODEL_DIR + '/train.txt', 'w+')
test_file = open(MODEL_DIR + '/test.txt', 'w+')

for i in range(IMAGE_COUNT):
    # Max depth in dataset is 10m - use to normalize values to [0...255]
    normalized_depth = (mat_file['depths'][i] * 25.5).astype(np.uint8)
    stacked = np.concatenate(
            (mat_file['images'][i], np.expand_dims(normalized_depth, 0)), 0)
    labels = mat_file['labels'][i].astype(np.uint8)

    out_dir = TRAIN_DIR
    record_file = train_file
    if i > SPLIT:
        out_dir = TEST_DIR
        record_file = test_file

    img_filename = '{}/{:05d}.png'.format(out_dir, i)
    label_filename = '{}/{:05d}_label.png'.format(out_dir, i)

    # The dataset comes with the axes in reverse order - swap these
    # so PIL renders image correctly
    img = Image.fromarray(np.swapaxes(stacked, 0, 2))
    img.save(img_filename)

    img = Image.fromarray(np.swapaxes(labels, 0, 1))
    img.save(label_filename)
    
    record = '{0}/{1} {0}/{2}'.format(MOUNT_POINT, img_filename, label_filename)
    print(record, file=record_file)


mat_file.close()
train_file.close()
test_file.close()
