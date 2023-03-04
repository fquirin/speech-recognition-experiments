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
if [ -n "$(uname -m | grep aarch64)" ]; then
	#ARM 64bit
	pip3 install nemo_toolkit[asr]
elif [ -n "$(uname -m | grep armv7l)" ]; then
	#ARM 32bit - too much trouble
	echo "Sorry, but ARM 32bit is currently not supported!"
	exit 1
else
	#x86_64 - skip GPU stuff by fetching torch+cpu in advance - this will greatly reduce installation size
	PY_VERSION=$(python3 --version)
	if [ $(echo "$PY_VERSION" | grep 3.9 | wc -l) -eq 1 ]; then
		echo "Python 3.9 detected, using available torch+cpu wheel"
		pip3 install https://download.pytorch.org/whl/cpu/torch-1.13.1%2Bcpu-cp39-cp39-linux_x86_64.whl
	elif [ $(echo "$PY_VERSION" | grep 3.8 | wc -l) -eq 1 ]; then
		echo "Python 3.8 detected, using available torch+cpu wheel"
		pip3 install https://download.pytorch.org/whl/cpu/torch-1.13.1%2Bcpu-cp38-cp38-linux_x86_64.whl
	elif [ $(echo "$PY_VERSION" | grep 3.10 | wc -l) -eq 1 ]; then
		echo "Python 3.10 detected, using available torch+cpu wheel"
		pip3 install https://download.pytorch.org/whl/cpu/torch-1.13.1%2Bcpu-cp310-cp310-linux_x86_64.whl
	else
		echo "NOTE: If you don't need GPU support you can install torch+cpu to reduce size."
		echo "Check out: https://download.pytorch.org/whl/cpu/"
	fi
	pip3 install nemo_toolkit[asr]
fi
echo "DONE"
echo "Note: use 'bash download_models.sh' to get models."
