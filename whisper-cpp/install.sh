#!/bin/bash
echo "Installing Whisper.Cpp ..."
sudo apt update
sudo apt install -y --no-install-recommends git build-essential
if [ -n "$1" ] && [ "$1" == "BLAS" ]; then
	echo 'Checking OpenBLAS package'
	sudo apt install -y --no-install-recommends libopenblas-dev
else
	echo 'NOTE: You can use the argument "BLAS" to build with OpenBLAS support.'
	echo ''
fi
#only for stream:
#sudo apt install -y --no-install-recommends libsdl2-dev
echo "Cloning and model download ..."
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
mkdir -p models
if [ ! -f "models/ggml-tiny.bin" ]; then
	bash ./models/download-ggml-model.sh tiny
fi
if [ ! -f "models/ggml-base.bin" ]; then
	bash ./models/download-ggml-model.sh base
fi
echo "Running build process ..."
if [ -n "$1" ] && [ "$1" == "BLAS" ]; then
	make clean
	WHISPER_OPENBLAS=1 make && make bench
else
	make clean && make && make bench
fi
echo "DONE"
