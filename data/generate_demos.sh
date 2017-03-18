#!/bin/sh

sudo singularity create hello-world.img
sudo singularity bootstrap hello-world.img helloworld.def
sudo singularity create hello-name.img
sudo singularity bootstrap hello-name.img helloname.def
