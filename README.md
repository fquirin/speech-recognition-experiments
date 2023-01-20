# Speech Recognition Experiments

Experiments to check out different ASR/STT systems and evaluate integration into [SEPIA STT-Server](https://github.com/SEPIA-Framework/sepia-stt-server).  
  
ASR engines:
- [Whisper TFlite](whisper-tflite) - An efficient Tensorflow Lite compatible Whisper port
- [Whisper Cpp](whisper-cpp) - An efficient and small C++ port of Whisper
- [Sherpa ncnn](sherpa-ncnn) - Next-gen Kaldi implementation for streaming ASR

## Benchmarks

### Raspberry Pi 400 - Aarch64 - Debian Bullseye

TODO

| Engine | Model | File | Th | Stream | RTF | WER |
| ------ | ----- | ---- | -- | ------ | --- | --- |
| Whisper TFlite | Whisper tiny.en | ---- | -- | ------ | --- | --- |
| Whisper Cpp | Whisper tiny | ---- | -- | ------ | --- | --- |
| Sherpa ncnn | conv-emformer-transducer-small-2023-01-09 | ---- | -- | ------ | --- | --- |

#### Comments

TBD
