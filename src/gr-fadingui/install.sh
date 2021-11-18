#!/bin/sh

mkdir -p build
cmake -DGR_PYTHON_DIR=/usr/lib/python3/dist-packages/ -GNinja -Bbuild
ninja -C build

# install to system
sudo ninja -C build install
