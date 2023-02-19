#!/bin/bash
if [ -d "venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
else
	echo "No Python virtual environment found."
fi
echo ""
export OMP_NUM_THREADS=2
time python3 test.py --model "tiny" --beamsize 1 --lang "en"
