#!/usr/bin/env python
import os
import sys
import argparse
import glob
import time

import numpy as np
from PIL import Image

import caffe
import constants


def main(argv):
    parser = argparse.ArgumentParser()
    # Required arguments: input and output files.
    parser.add_argument(
        "dataset",
        help="Image names (txt).")
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
    parser.add_argument(
        "--save_dir",
        help="Where to store predictions (optional).")
    args = parser.parse_args()

    if args.gpu:
        caffe.set_mode_gpu()
        print("GPU mode")
    else:
        caffe.set_mode_cpu()
        print("CPU mode")

    # Make classifier.
    net = caffe.Net(args.model_def, args.pretrained_model, caffe.TEST)

    with open(args.dataset) as f:
        target_filenames = map(lambda l: l.split()[1], f.readlines())

    total_non_empty = 0
    global_accuracy_total = 0
    label_accuracy_totals = [0] * len(constants.LABEL_NAMES)
    # TODO figure out how to just iterate until end
    for target_file in target_filenames:
        print("Processing {}".format(target_file))

        net.forward()
        target = np.asarray(Image.open(target_file))

        probabilities = np.squeeze(net.blobs['prob'].data[0,:,:,:])
        prediction = np.argmax(probabilities, axis=0)

        non_empty_mask = (target != constants.EMPTY_LABEL)
        non_empty_count = np.count_nonzero(non_empty_mask)
        total_non_empty += non_empty_count
        # Because we will never predict an empty label, automatically forces all
        # target empty pixels to be false (desired behavior)
        correct_mask = (prediction - target == 0)
        global_accuracy_total += np.count_nonzero(correct_mask)

        for i in range(len(label_accuracy_totals)):
            target_positives = (target == i)
            predicted_negatives = np.logical_and((prediction != i), non_empty_mask)
    
            true_positives = np.count_nonzero(
                    np.logical_and(target_positives, correct_mask))
            true_negatives = np.count_nonzero(
                    np.logical_and(predicted_negatives, np.logical_not(target_positives)))
            label_accuracy_totals[i] += (true_positives + true_negatives)

        if args.save_dir:
            img = Image.fromarray(np.uint8(prediction))
            img.save("{}/{}".format(args.save_dir, target_file.split('/')[-1]))

    avg_class_accuracy_totals = 0
    print("====Class Accuracies:")
    for name, total in zip(constants.LABEL_NAMES, label_accuracy_totals):
        avg_acc = total / float(total_non_empty)
        avg_class_accuracy_totals += avg_acc
        print("{} - {}".format(name, avg_acc))

    print("====Average Class Accuracy: {}".format(
                avg_class_accuracy_totals / len(constants.LABEL_NAMES)))
    print("====Global Accuracy: {}".format(
                global_accuracy_total / float(total_non_empty)))


if __name__ == '__main__':
    main(sys.argv)
