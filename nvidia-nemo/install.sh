#!/bin/bash
set -e
echo "Installing NVIDIA NeMo ASR ..."
sudo apt update
sudo apt install -y --no-install-recommends python3-pip python3-dev python3-setuptools python3-wheel python3-venv
sudo apt install -y --no-install-recommends libsndfile1 ffmpeg
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
pip3 install nemo_toolkit[asr]
echo "DONE"
echo "Note: use 'bash download_models.sh' to get models."
