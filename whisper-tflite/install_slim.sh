#!/bin/bash
set -e
echo "Installing Whisper-TFlite ..."
echo "NOTE: This script will skip the 'fat' tensorflow packages and install only tflite_runtime."
sudo apt update
sudo apt install -y --no-install-recommends python3-pip python3-dev python3-setuptools python3-wheel python3-venv
sudo apt install -y --no-install-recommends ffmpeg
if [ -d "venv/" ]; then
	echo "Activating Python virtual env."
	source venv/bin/activate
else
	echo "Creating and activating Python virtual env."
	python3 -m venv venv && source venv/bin/activate
fi
echo "Installing packages ..."
pip3 install --upgrade pip
pip3 install git+https://github.com/openai/whisper.git
if [ -n "$(uname -m | grep aarch64)" ]; then
	echo "Installing 'tflite_runtime' built with Bazel for aarch64 ..."
	pip3 install https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/tflite_runtime-2.13.0-cp39-cp39-linux_aarch64.whl
	echo "If you get errors with this 'tflite_runtime' try 'pip3 uninstall tensorflow tflite tensorflow_io'"
else
	echo "Using default 'tflite_runtime' ..."
	pip3 install tflite_runtime
fi
echo "Downloading models ..."
mkdir -p models
cd models
if [ ! -f "whisper-tiny.en.tflite" ]; then
	wget https://github.com/usefulsensors/openai-whisper/raw/main/models/whisper-tiny.en.tflite
	#wget https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/whisper-tiny.en.tflite
fi
if [ ! -f "whisper-tiny.tflite" ]; then
	wget https://github.com/usefulsensors/openai-whisper/raw/main/models/whisper-tiny.tflite
fi
echo "DONE"
