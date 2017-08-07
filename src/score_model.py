#!/usr/bin/env python
import os
import sys
import argparse
import glob
import time

import numpy as np
from PIL import Image

import caffe

def score_prediction(target, prediction):
    non_empty_mask = (target != constants.EMPTY_LABEL)
    non_empty_count = np.count_nonzero(non_empty_mask)
    # Because we will never predict an empty label, automatically forces all
    # target empty pixels to be false (desired behavior)
    correct_mask = (prediction - target == 0)

    global_accuracy_total += np.count_nonzero(correct_mask) / non_empty_count

    for i in range(len(label_accuracy_totals)):
        target_positives = (target == i)
        predicted_negatives = np.logical_and((prediction != i), non_empty_mask)

        true_positives = np.count_nonzero(
                np.logical_and(target_positives, correct_mask))
        true_negatives = np.count_nonzero(
                np.logical_and(predicted_negatives, np.logical_not(target_positives)))
        label_accuracy_totals[i] += (true_positives + true_negatives) / non_empty_count


def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "model_def",
        help="Model definition file (prototxt).")
    parser.add_argument(
        "pretrained_model",
        help="Trained model weights file (caffemodel).")

    # Optional arguments.
    parser.add_argument(
        "--gpu",
        action='store_true',
        help="Switch for gpu computation.")
    args = parser.parse_args()

    if args.gpu:
        caffe.set_mode_gpu()
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    net = caffe.Net(args.model_def, args.pretrained_model, caffe.TEST)

    global_accuracy_total = 0
    label_accuracy_totals = [0] * len(constants.LABEL_NAMES)
    # TODO figure out how to just iterate until end
    for i in range(1):
        net.forward()

        predicted = net.blobs['prob'].data
        output = np.squeeze(predicted[0,:,:,:])
        # TODO I think that this is what we want (the labels). Give it a better name..
        # TODO test these things one by one in cpu mode and just print shapes
        # at first to see if working.
        ind = np.argmax(output, axis=0)

        print(output.shape)

    # TODO need to use syntax from other script, not classifier.predict
    # (https://github.com/alexgkendall/SegNet-Tutorial/blob/master/Scripts/test_segmentation_camvid.py)
    # TODO need to write an X_inference.prototxt

    # TODO at end, print all class accuracies with their human-readable names
    # TODO print the avg. class accuracy
    # TODO print the global accuracy


if __name__ == '__main__':
    main(sys.argv)
