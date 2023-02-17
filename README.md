# Speech Recognition Experiments

Experiments to check out different ASR/STT systems and evaluate integration into [SEPIA STT-Server](https://github.com/SEPIA-Framework/sepia-stt-server).  
  
ASR engines:
- [Whisper TFlite](whisper-tflite) - An efficient and fast Tensorflow Lite compatible Whisper port
- [Whisper Cpp](whisper-cpp) - An efficient and small C++ port of Whisper
- [Whisper CT2](whisper-ct2) - An efficient and fast CTranslate2 port of Whisper
- [Sherpa ncnn](sherpa-ncnn) - Next-gen Kaldi implementation for streaming ASR

## Benchmarks

### Raspberry Pi 400 - Aarch64 - Debian Bullseye

Test date: 2023.02.16

| Engine | Model | File | Threads | Stream | Time | RTF | Quality |
| ------ | ----- | ---- | -- | ------ | ---- | --- | ------- |
| Whisper TFlite | tiny.en | 1 | 4 | - | 4.1s | 0.37 | perfect |
| Whisper TFlite | tiny.en | 2 | 4 | - | 3.4s | 0.94 | perfect |
| Whisper TFlite (slim) | tiny.en | 1 | 4 | - | 3.9s | 0.36 | perfect |
| Whisper TFlite (slim) | tiny.en | 2 | 4 | - | 3.2s | 0.90 | perfect |
| Whisper Cpp | ggml-tiny | 1 | 4 | - | 9.1s | 0.83 | perfect |
| Whisper Cpp | ggml-tiny | 2 | 4 | - | 8.6s | 2.39 | perfect |
| Whisper Cpp (BLAS) | ggml-tiny | 1 | 4 | - | 8.4s | 0.76 | perfect |
| Whisper Cpp (BLAS) | ggml-tiny | 2 | 4 | - | 8.0s | 2.22 | perfect |
| Whisper CT2 | whisper-tiny-ct2 | 1 | 4 | - | 3.9s | 0.36 | perfect |
| Whisper CT2 | whisper-tiny-ct2 | 2 | 4 | - | 3.2s | 0.90 | perfect |
| Sherpa ncnn | small-2023-01-09 | 1 | 4 | + | 1.97s | 0.18 | okayish |
| Sherpa ncnn | small-2023-01-09 | 2 | 4 | + | 0.63s | 0.18 | low |

Test notes:
- File 1 is `en_speech_jfk_11s.wav`
- File 2 is `en_sh_lights_70pct_4s.wav`
- `Whisper TFlite (slim)` is the `tflite_runtime` package built with **Bazel** (much faster!)
- `Whisper Cpp` is built with default settings ('NEON = 1', 'BLAS = 0') and `Whisper Cpp (BLAS)` with OpenBlas
- `Whisper CT2` uses the 'int8' model
- `Quality` is a subjective impression of the transcribed result (TODO: replace with WER)
- Sherpa model `small-2023-01-09` full name is `conv-emformer-transducer-small-2023-01-09`

#### Comments

- 'Whisper':
  - Whisper in any form, is very accurate, but the missing streaming support is the biggest drawback.
  - RTF is not linear. Unfortunately the short files (<4s) need almost the same time to transcribe as the larger ones (>10s).
  - For RPi4 based voice assistants you have to wait usually >3s after finishing your input to get a result.
  - `Whisper CT2` seems to be the best version right now for the RPi4 (aarch64 systems?). It has the same speed as the TFlite version but smaller size and better API.
- 'Sherpa ncnn':
  - Sherpa is very fast and supports streaming audio, but without language model WER is too high.
  - Example result (file 1, JFK speech): "AND SAW MY FELLOW AMERICA AS NOT WHAT YOUR COUNTRY CAN DO FOR YOU AND WHAT YOU CAN DO FOR YOUR COUNTRY".
