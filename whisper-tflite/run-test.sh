#!/bin/bash
if [ -d "venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
	echo ""
fi
time python3 test.py

