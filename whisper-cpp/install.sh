#!/bin/bash
echo "Installing Whisper.Cpp ..."
sudo apt update
sudo apt install -y --no-install-recommends git build-essential
#only for stream:
#sudo apt install -y --no-install-recommends libsdl2-dev
echo "Cloning and model download ..."
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
mkdir -p models
if [ ! -f "models/ggml-tiny.bin" ]; then
	bash ./models/download-ggml-model.sh tiny
fi
if [ ! -f "models/ggml-tiny.bin" ]; then
	bash ./models/download-ggml-model.sh base
fi
echo "Running build process ..."
make clean && make && make bench
echo "DONE"
