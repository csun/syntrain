#!/usr/bin/env bash

sudo nvidia-docker run -ti --volume=$(pwd):/SegNet -u $(id -u):$(id -g) caffe:gpu bash
sudo docker container prune
