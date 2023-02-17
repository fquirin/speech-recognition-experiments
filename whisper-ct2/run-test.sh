#!/bin/bash
if [ -d "venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
else
	echo "No Python virtual environment found."
fi
echo ""
time python3 test.py --lang "auto" --beamsize 1 --threads 2 --model "models/whisper-tiny-ct2"
