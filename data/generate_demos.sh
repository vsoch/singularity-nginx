#!/bin/sh

sudo singularity create hello-world.img
sudo singularity bootstrap hello-world.img helloworld.def
