# NVIDIA NeMo ASR

NVIDIA NeMo is a toolkit for conversational AI including several models for ASR.  
  
Links:
- NeMo GitHub: https://github.com/NVIDIA/NeMo
- NeMo ASR Docs: https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/intro.html
- NeMo ASR Models: https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nemo_asr
- Language Modeling: https://docs.nvidia.com/deeplearning/nemo/user-guide/docs/en/main/asr/asr_language_modeling.html
- KenLM: https://github.com/kpu/kenlm

Tested with:
- Arm64 - Debian 11 - Python 3.9
- x86_64 - Debian 11 - Python 3.9

## Train and use language models

The beam search decoders in NeMo support N-gram language models trained for example with the KenLM toolbox.  
Use `bash install_lm_tools.sh` to get pre-built KenLM binaries and the required ctc-decoders. The wheels are not available for all Python version,
so you might need to build them yourself (see: asr_language_modeling/ngram_lm/install_beamsearch_decoders.sh).  

- Check-out the ['train'](train) folder to learn how to build a simple n-gram LM in ~5 minutes
- Use `python3 test_with_lm.py -h` to see available options
- Read the Nvidia 'language modeling' docs (see above) to learn about beam width, alpha and beta parameters
- To run inference with LM use something like `python3 test_with_lm.py -m "models/stt_en_conformer_ctc_small.nemo" -l "models/kenlm_custom.4gram" -w 4 -a 1.0 -b 2.0`
- You can get a "naive" character error rate (CER) score for transcriptions by adding a txt-file for each wav-file with the target transcription (same name, just '.txt' ending) and using the `--transcriptions [folder]` argument
