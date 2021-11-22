#!/bin/sh

set -o errexit

mkdir -p build
cmake -DGR_PYTHON_DIR=/usr/lib/python3/dist-packages/ -GNinja -Bbuild
ninja -C build

# run QA
export CTEST_OUTPUT_ON_FAILURE=1
ninja -C build test
cat build/Testing/Temporary/LastTest.log

# install to system
sudo ninja -C build install
