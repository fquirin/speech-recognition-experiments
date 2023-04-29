# Vosk

Vosk is a speech recognition toolkit that is lightweight (~5MB runtime), very fast (even on Raspberry Pi), supports streaming audio,
has excellent smaller models for a number of languages (~50MB), works with older Kaldi models and supports KenLM language models.  
  
There is a basic speaker recognition demo available as well (`python test_spk.py -h`). The model calculates speaker vectors for each
audio chunk, so make sure the chunk size is large enough or results will be poor.  
  
Links:
- Vosk GitHub: https://github.com/alphacep/vosk-api
- Vosk Models: https://alphacephei.com/vosk/models
- Language modeling: https://github.com/fquirin/kaldi-adapt-lm (or see Vosk docs)
- KenLM: https://github.com/kpu/kenlm

Tested with:
- Arm32 - Debian 10 - Python 3.7
- Arm64 - Debian 11 - Python 3.9
- x86_64 - Debian 11 - Python 3.9

## License

Apache License 2.0:  
https://github.com/alphacep/vosk-api/blob/master/COPYING  
  
Check the models page for individual model licenses (usually Apache License 2.0 as well).
