#!/bin/bash
set -e
echo "Installing language model tools ..."
sudo apt update
sudo apt install -y --no-install-recommends swig libboost-thread-dev libboost-program-options-dev unzip
if [ -d "venv/" ]; then
	echo "Activating Python virtual env."
	source venv/bin/activate
else
	echo "Creating and activating Python virtual env."
	python3 -m venv venv && source venv/bin/activate
fi
echo ""
echo "NOTE: ctc-decoders wheels are only available for Python 3.9 atm."
echo "For other versions please use this script:"
echo "asr_language_modeling/ngram_lm/install_beamsearch_decoders.sh"
echo ""
#get ctc-decoder Wheel and KenLM binaries
if [ -n "$(uname -m | grep aarch64)" ]; then
	#ARM 64bit
	wget https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/kenlm_bin_aarch64.zip
	unzip kenlm_bin_aarch64.zip -d kenlm_bin
	rm kenlm_bin_aarch64.zip
	pip3 install https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/ctc_decoders-1.1-cp39-cp39-linux_aarch64.whl
elif [ -n "$(uname -m | grep armv7l)" ]; then
	#ARM 32bit - we don't have the files right now
	echo "Sorry, but ARM 32bit is currently not supported!"
	exit 1
else
	#x86_64 - skip GPU stuff by fetching torch+cpu in advance
	wget https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/kenlm_bin_amd64.zip
	unzip kenlm_bin_amd64.zip -d kenlm_bin
	rm kenlm_bin_amd64.zip
	pip3 install https://github.com/fquirin/speech-recognition-experiments/releases/download/v1.0.0/ctc_decoders-1.1-cp39-cp39-linux_x86_64.whl
fi
#make sure KenLM binaries are executable
chmod +x kenlm_bin/*
echo "DONE"
