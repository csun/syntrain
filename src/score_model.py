#!/usr/bin/env python
import numpy as np
import os
import sys
import argparse
import glob
import time

import caffe


def main(argv):
    pycaffe_dir = # TODO compute this from constants.py and set convert_nyu... to use

    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "output_file",
        help="Output npy filename."
    )
    # Optional arguments.
    parser.add_argument(
        "--model_def",
        default=os.path.join(pycaffe_dir,
                "../models/bvlc_reference_caffenet/deploy.prototxt"),
        help="Model definition file."
    )
    parser.add_argument(
        "--pretrained_model",
        default=os.path.join(pycaffe_dir,
                "../models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel"),
        help="Trained model weights file."
    )
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation."
    )
    # TODO do we need this?
    parser.add_argument(
        "--channel_swap",
        default='2,1,0',
        help="Order to permute input channels. The default converts " +
             "RGB -> BGR since BGR is the Caffe default by way of OpenCV."
    )
    args = parser.parse_args()

    image_dims = # TODO set this to constants.IMAGE_SIZE

    # TODO keep this configurable
    if args.gpu:
        caffe.set_mode_gpu()
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    classifier = caffe.Classifier(args.model_def, args.pretrained_model,
            image_dims=image_dims, input_scale=args.input_scale, raw_scale=args.raw_scale)

    inputs = # TODO Using test.txt, create a list of loaded input images
    print("Classifying %d inputs." % len(inputs))

    # Classify.
    start = time.time()
    predictions = classifier.predict(inputs, False)
    print("Done in %.2f s." % (time.time() - start))

    # TODO load all target images
    # TODO subtract targets from predictions and count num of zeroes for global accuracy
    # TODO compute class accuracy similarly?
    # TODO read paper to make sure that this is how those are actually computed.


if __name__ == '__main__':
    main(sys.argv)
