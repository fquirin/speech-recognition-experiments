#!/bin/bash
if [ -d "venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
else
	echo "No Python virtual environment found."
fi
echo ""
time python3 test.py --model "models/whisper-tiny.tflite" --runtime 2 --threads 2
