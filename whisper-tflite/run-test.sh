#!/bin/bash
if [ -d "venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
fi
start_t=$(date +"%s.%N")
time python3 test.py
finish_t=$(date +"%s.%N")
echo "Took: $(expr $finish_t-$start_t | bc)s"

