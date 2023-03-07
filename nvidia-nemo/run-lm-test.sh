#!/bin/bash
if [ -d "venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
else
	echo "No Python virtual environment found."
fi
echo ""
if [ ! -d "kenlm_bin/" ]; then
	echo "Please install LM tools first!"
	exit 1
fi
python3 test_with_lm.py -m "models/stt_en_conformer_ctc_small.nemo" -l "models/kenlm_custom.4gram" -w 4 -a 1.0 -b 2.0 --all-hypos --threads 4
