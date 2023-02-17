#!/bin/bash
set -e
echo "Installing Whisper for CTranslate2 ..."
sudo apt update
sudo apt install -y --no-install-recommends python3-pip python3-dev python3-setuptools python3-wheel python3-venv
if [ -d "venv/" ]; then
	echo "Activating Python virtual env."
	source venv/bin/activate
else
	echo "Creating and activating Python virtual env."
	python3 -m venv venv && source venv/bin/activate
fi
echo "Installing packages ..."
pip3 install --upgrade pip
git clone https://github.com/guillaumekln/faster-whisper
cd faster-whisper
pip3 install -e .[conversion] # to convert models
#pip3 install -e . # if you have models already
echo "Downloading models ..."
cd ..
#bash get-model.sh "tiny.en"
bash get-model.sh "tiny"
echo "DONE"
