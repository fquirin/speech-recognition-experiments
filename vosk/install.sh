#!/bin/bash
set -e
echo "Installing Vosk ASR ..."
sudo apt update
sudo apt install -y --no-install-recommends python3-pip python3-dev python3-setuptools python3-wheel python3-venv unzip
if [ -d "venv/" ]; then
	echo "Activating Python virtual env."
	source venv/bin/activate
else
	echo "Creating and activating Python virtual env."
	python3 -m venv venv && source venv/bin/activate
fi
echo "Installing packages ..."
pip3 install --upgrade pip
pip3 install vosk
pip3 install pydub
echo "Downloading models ..."
mkdir -p models
cd models
if [ ! -d "vosk-model-small-en-us-0.15" ]; then
	wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
	unzip "vosk-model-small-en-us-0.15.zip"
fi
if [ ! -d "vosk-model-small-de-0.15" ]; then
	wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
	unzip "vosk-model-small-de-0.15.zip"
fi
if [ ! -d "vosk-model-spk-0.4" ]; then
        wget https://alphacephei.com/vosk/models/vosk-model-spk-0.4.zip
        unzip "vosk-model-spk-0.4.zip"
fi
#if [ ! -d "vosk-model-en-us-0.22" ]; then
#	wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip
#	unzip "vosk-model-en-us-0.22.zip"
#fi
#if [ ! -d "vosk-model-en-us-0.22-lgraph" ]; then
#       wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22-lgraph.zip
#       unzip "vosk-model-en-us-0.22-lgraph.zip"
#fi
rm *.zip
echo "DONE"

