#!/usr/bin/env bash

if [ -z "$1" ]; then
	/SegNet/caffe-segnet-cudnn5/build/tools/caffe train -gpu 0 -solver /SegNet/models/combined_solver.prototxt
else
	/SegNet/caffe-segnet-cudnn5/build/tools/caffe train -gpu 0 -solver /SegNet/models/combined_solver.prototxt -snapshot $1
fi
