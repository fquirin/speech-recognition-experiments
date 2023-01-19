#!/bin/bash
echo "Installing Sherpa-ncnn ..."
sudo apt update
sudo apt install -y --no-install-recommends git build-essential
echo "Cloning code ..."
git clone https://github.com/k2-fsa/sherpa-ncnn
echo "Running build process ..."
cd sherpa-ncnn
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j3
cd ..
echo "Downloading models ..."
mkdir -p models
cd models
if [ ! -d "sherpa-ncnn-conv-emformer-transducer-small-2023-01-09/" ]; then
	wget https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/sherpa-ncnn-conv-emformer-transducer-small-2023-01-09.zip
	unzip sherpa-ncnn-conv-emformer-transducer-small-2023-01-09.zip -d sherpa-ncnn-conv-emformer-transducer-small-2023-01-09
fi
echo "DONE"
