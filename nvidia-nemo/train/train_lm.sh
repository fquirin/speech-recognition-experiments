#!/bin/bash
set -e
if [ -d "../venv/" ]; then
	echo "Please make sure you've activated the Python virtual environment!"
	echo "Use: source venv/bin/activate"
else
	echo "No Python virtual environment found."
fi
SENTENCES="sentences.txt"
LM_NAME="kenlm_custom.4gram"
BASE_MODEL="stt_en_conformer_ctc_small.nemo"
echo ""
echo "Sentences list: $SENTENCES"
echo "Base model: $BASE_MODEL"
echo ""
echo "Creating language model..."
echo ""
cd ../asr_language_modeling/ngram_lm
python3 train_kenlm.py --nemo_model_file "../../models/${BASE_MODEL}" \
    --train_file "../../train/${SENTENCES}" \
    --kenlm_bin_path "../../kenlm_bin" \
    --kenlm_model_file "../../models/${LM_NAME}" \
    --ngram_length 4
echo ""
echo "DONE"
echo "LM model name: $LM_NAME"
