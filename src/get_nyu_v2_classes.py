import math
import sys

import h5py
import numpy as np


if len(sys.argv) != 2:
    print('Please provide the path to the nyu dataset .mat file')
    sys.exit(1)

mat_file = h5py.File(sys.argv[1], 'r')
TOTAL_CLASSES = len(mat_file['names'][0])
TOTAL_IMAGES = len(mat_file['labels'])
class_hist = [0] * TOTAL_CLASSES

def label_name(index):
    # File format really messes up strings
    obj = mat_file[mat_file['names'][0][index]]
    return ''.join(chr(i) for i in obj)

def count_image(index):
    img = mat_file['labels'][index]
    seen = np.unique(img)

    for label in seen:
        # NOTE the 'labels' array is 0 indexed, though the actual labels they
        # correspond to in the images are 1 indexed as 0 represents unlabeled.
        # To deal with this, we need to ignore 0 labels and subtract 1 from the
        # pixel value.
        if label != 0:
            class_hist[label - 1] += 1

for index in range(TOTAL_IMAGES):
    count_image(index)
names = map(label_name, range(TOTAL_CLASSES))

# NOTE again, add one to deal with the 1 indexing of labels
zipped = zip(names, class_hist, range(1,TOTAL_CLASSES + 1))
zipped = sorted(zipped, key=lambda x: x[1], reverse=True)

out_file = open('classes.csv', 'w+')
print('Name,Count,Index', file=out_file)
for item in zipped:
    print('{},{},{}'.format(*item), file=out_file)


out_file.close()
mat_file.close()
