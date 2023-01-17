#!/bin/bash
sudo apt update
sudo apt install -y --no-install-recommends python3-pip python3-dev python3-setuptools python3-wheel python3-venv
sudo apt install -y --no-install-recommends ffmpeg
if [ -f "venv" ]; then
	source venv/bin/activate
else
	python3 -m venv venv && source venv/bin/activate
fi
pip3 install --upgrade pip
pip3 install git+https://github.com/openai/whisper.git
pip3 install tensorflow==2.11.0 tflite==2.10.0 tensorflow_io==0.27.0
#pip3 install tflite_runtime
mkdir -p models
cd models
if [ ! -f "whisper.tflite" ]; then
	wget https://github.com/usefulsensors/openai-whisper/raw/main/models/whisper.tflite
fi
echo "DONE"
