#!/bin/bash
model="tiny"
if [ -n "$1" ]; then
	model=$1
else
	echo "Please specify the model to download."
	echo "Examples: tiny, tiny.en, base, small, ..."
	exit
fi
echo "Downloading and converting: openai/whisper-$1 (from https://huggingface.co/openai)..."
echo "NOTE: If download fails check the experiments repository for model files."
echo ""
mkdir -p models
if [ ! -d "models/whisper-$1-ct2" ]; then
	ct2-transformers-converter --model "openai/whisper-$1" --output_dir "models/whisper-$1-ct2" --quantization int8
else
	echo "Folder already exists: models/whisper-$1-ct2 - skipped"
fi
