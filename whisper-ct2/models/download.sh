#!/bin/bash
set -e
if [ -z "$1" ]; then
	echo "Please add a model name like 'tiny.en', 'small' or 'large-v2' etc."
	exit 1
fi
MODEL_NAME=$1
MODEL_FOLDER="faster-whisper-${MODEL_NAME}"
echo "Downloading CTranslate2-ready models from 'Huggingface/guillaumekln' ..."
echo ""
mkdir -p $MODEL_FOLDER
cd $MODEL_FOLDER
wget "https://huggingface.co/guillaumekln/${MODEL_FOLDER}/resolve/main/README.md"
wget "https://huggingface.co/guillaumekln/${MODEL_FOLDER}/resolve/main/config.json"
wget "https://huggingface.co/guillaumekln/${MODEL_FOLDER}/resolve/main/model.bin"
wget "https://huggingface.co/guillaumekln/${MODEL_FOLDER}/resolve/main/tokenizer.json"
wget "https://huggingface.co/guillaumekln/${MODEL_FOLDER}/resolve/main/vocabulary.txt"
echo "DONE"
