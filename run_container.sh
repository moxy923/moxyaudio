#!/bin/bash

root_dir=$PWD

# run
docker run -i -v /dev/snd:/dev/snd -v $root_dir:/app --privileged audio