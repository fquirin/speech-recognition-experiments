#!/bin/bash
set -e
echo "Installing NVIDIA NeMo ASR ..."
sudo apt update
sudo apt install -y --no-install-recommends python3-pip python3-dev python3-setuptools python3-wheel python3-venv
sudo apt install -y --no-install-recommends libsndfile1 ffmpeg
sudo apt install -y --no-install-recommends build-essential cmake
if [ -d "venv/" ]; then
	echo "Activating Python virtual env."
	source venv/bin/activate
else
	echo "Creating and activating Python virtual env."
	python3 -m venv venv && source venv/bin/activate
fi
echo "Installing packages ..."
pip3 install --upgrade pip
pip3 install Cython
if [ -n "$(uname -m | grep armv7l)" ]; then
	#ARM 32bit - too much trouble
	echo "Sorry, but ARM 32bit is currently not supported!"
	exit 1
else
	#skip GPU stuff by fetching torch+cpu in advance - this will greatly reduce installation size
	echo "Installing torch for CPU (change script if you need GPU) ..."
	pip3 install torch==1.13.1 torchaudio==0.13.1 --index-url https://download.pytorch.org/whl/cpu
	echo "Installing NeMo package ..."
	#pip3 install git+https://github.com/NVIDIA/NeMo.git@{main}#egg=nemo_toolkit[asr]
	pip3 install nemo_toolkit[asr]
fi
echo "DONE"
echo "Note: use 'bash download_models.sh' to get models."
