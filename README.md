# Speech Recognition Experiments

Experiments to check out different ASR/STT systems and evaluate integration into [SEPIA STT-Server](https://github.com/SEPIA-Framework/sepia-stt-server).  
  
ASR engines:
- [Whisper org](whisper-org) - The original Whisper version by Open-AI
- [Whisper TFlite](whisper-tflite) - A Tensorflow Lite compatible Whisper port
- [Whisper Cpp](whisper-cpp) - A small C++ port of Whisper
- [Whisper CT2](whisper-ct2) - An efficient and fast CTranslate2 port of Whisper
- [Sherpa ncnn](sherpa-ncnn) - Next-gen Kaldi implementation for streaming ASR
- [Nvidia NeMo](nvidia-nemo) - A toolkit for various end-to-end ASR models and languages
- [Vosk](vosk) - Fast, small, accurate (for clear audio), easy to customize. Works with classic Kaldi models. One of the core engines of SEPIA STT Server.

Other great engines already included in SEPIA:
- [Coqui STT](https://github.com/coqui-ai/STT) - Successor of Mozilla's Deep Speech project. End-to-end ASR with CTC decoder and "optional" LMs.

## Installation

- Each ASR experiment folder has an install bash script, simply run `bash install.sh`.
- Sometimes you will find additional scripts to download models. They should be mentioned during installation.
- After a successful installation use `bash run-test.sh` to run a default test. If the script uses Python you need to activate the right virtual environment first: `source venv/bin/activate`.

## Comments and Impressions

- Whisper:
  - Whisper in any form, is very accurate, but the missing streaming support is the biggest drawback.
  - RTF is not linear. Unfortunately the short files (<4s) need almost the same time to transcribe as the larger ones (>10s).
  - For Raspberry Pi 4 based voice assistants you have to wait usually >3s after finishing your input to get a result (bad UX).
  - An Orange Pi 5 with optimal Whisper is fast enough to run the 'tiny' model and get good UX (usually <1.5s inference time for every input <30s).
  - `Whisper CT2` seems to be the best version right now for the Arm64/Aarch64 systems (RPi4 etc.). It has the same speed as the TFlite version or even faster, is smaller in size, works better with non-en languages and has a cleaner API.
- Sherpa ncnn:
  - Sherpa is very fast and supports streaming audio, but without language model WER is a bit high at the moment. Results look very promising though.
  - Example result (file 1, JFK speech): "AND SAW MY FELLOW AMERICANS ASK NOT WHAT YOUR COUNTRY CAN DO FOR YOU ASK WHAT YOU CAN DO FOR YOUR COUNTRY".
  - UPDATED 2023.04.29: Included better English model.
- Nvidia NeMo:
  - Nvidia NeMo small models (e.g. 'en_conformer_ctc_small') are very fast and precise for clear and simple audio files.
  - Unfortunately NeMo has no pre-trained models for streaming conformer yet (2023.03.07)
  - Non-streaming is a bit faster than Sherpa-ncnn but way more precise
  - The test results below currently indicate the quality is as good as Whisper, but more complicated vocabulary and noisy audio quickly shows that Whisper still performs much better, especially compared to larger NeMo models.
  - NeMo can be tuned easily using (phoneme free!) language models. Depending on your beam parameters (width, alpha, beta) accuracy for your LM vocabulary can increase dramatically, while it will drop for out-of-vocabulary words.
- Vosk:
  - Vosk is very small, fast, supports streaming audio and you can convert most of the classic Kaldi models to be used with it.
  - The small models are only ~50MB and surprisingly good, even for general dictation tasks ... if your input audio isn't too noisy.
  - The larger models are solid, but I never really use them, because they are much slower, need more RAM and don't offer much better results in my everyday tests with SEPIA assistant.
  - If you want good accuracy in a specific domain you should train your own language model. The Vosk homepage has some documentation, but for SEPIA I use the [kaldi-adapt-lm](https://github.com/fquirin/kaldi-adapt-lm) repo.
  - Vosk with a custom LM is probably your best ASR choice on low-end hardware.

## Benchmarks

Test notes:
- File 1 is `en_speech_jfk_11s.wav`
- File 2 is `en_sh_lights_70pct_4s.wav`
- All Whisper tests are done without language detection!
- `Whisper TFlite (slim)` is the `tflite_runtime` package built with **Bazel** (faster than default!)
- `Whisper Cpp` is built with default settings ('NEON = 1', 'BLAS = 0') and `Whisper Cpp (BLAS)` with OpenBlas
- `Whisper CT2` uses the 'int8' model
- `Quality` is a subjective impression of the transcribed result (TODO: replace with WER)
- Sherpa model `small-2023-01-09` full name is `conv-emformer-transducer-small-2023-01-09`

### Raspberry Pi 400 - Aarch64 - Debian Bullseye

Test date: 2023.02.17

| Engine | Model | File | Threads | Stream | Time | RTF | Quality |
| ------ | ----- | ---- | ------- | ------ | ---- | --- | ------- |
| Whisper original | tiny | 1 | 4 | - | 5.9s | 0.54 | perfect |
| Whisper original | tiny | 2 | 4 | - | 4.3s | 1.19 | perfect |
| Whisper TFlite | tiny.en | 1 | 4 | - | 4.1s | 0.37 | perfect |
| Whisper TFlite | tiny.en | 2 | 4 | - | 3.4s | 0.94 | perfect |
| Whisper TFlite (slim) | tiny.en | 1 | 4 | - | 3.9s | 0.36 | perfect |
| Whisper TFlite (slim) | tiny.en | 2 | 4 | - | 3.2s | 0.90 | perfect |
| Whisper TFlite (slim) | tiny | 1 | 4 | - | 4.7s | 0.43 | perfect |
| Whisper TFlite (slim) | tiny | 2 | 4 | - | 3.8s | 1.06 | perfect |
| Whisper Cpp | ggml-tiny | 1 | 4 | - | 9.1s | 0.83 | perfect |
| Whisper Cpp | ggml-tiny | 2 | 4 | - | 8.6s | 2.39 | perfect |
| Whisper Cpp (BLAS) | ggml-tiny | 1 | 4 | - | 8.4s | 0.76 | perfect |
| Whisper Cpp (BLAS) | ggml-tiny | 2 | 4 | - | 8.0s | 2.22 | perfect |
| Whisper CT2 | whisper-tiny-ct2 | 1 | 4 | - | 3.9s | 0.36 | perfect |
| Whisper CT2 | whisper-tiny-ct2 | 2 | 4 | - | 3.2s | 0.90 | perfect |
| Sherpa ncnn | small-2023-01-09 | 1 | 4 | + | 2.0s | 0.18 | okayish |
| Sherpa ncnn | small-2023-01-09 | 2 | 4 | + | 0.6s | 0.18 | low |

Test date: 2023.03.07

| Engine | Model | File | Threads | Stream | Time | RTF | Quality |
| ------ | ----- | ---- | ------- | ------ | ---- | --- | ------- |
| Nvidia NeMo | en_conformer_ctc_small | 1 | 4 | - | 1.1s | 0.10 | perfect |
| Nvidia NeMo | en_conformer_ctc_small | 2 | 4 | - | 0.5s | 0.14 | perfect |

### Orange Pi 5 8GB - Aarch64 - Armbian Bullseye (Kernel 5.10.110-rockchip-rk3588)

Test date: 2023.02.19

| Engine | Model | File | Threads | Stream | Time | RTF | Quality |
| ------ | ----- | ---- | ------- | ------ | ---- | --- | ------- |
| Whisper original | tiny | 1 | 4 | - | 3.0s | 0.27 | perfect |
| Whisper original | tiny | 2 | 4 | - | 1.9s | 0.53 | perfect |
| Whisper TFlite (slim) | tiny | 1 | 4 | - | 1.4s | 0.13 | perfect |
| Whisper TFlite (slim) | tiny | 2 | 4 | - | 1.4s | 0.39 | perfect |
| Whisper Cpp (BLAS) | ggml-tiny | 1 | 4 | - | 3.7s | 0.34 | perfect |
| Whisper Cpp (BLAS) | ggml-tiny | 2 | 4 | - | 3.5s | 0.97 | perfect |
| Whisper CT2 | whisper-tiny-ct2 | 1 | 4 | - | 1.3s | 0.12 | perfect |
| Whisper CT2 | whisper-tiny-ct2 | 2 | 4 | - | 1.4s | 0.39 | perfect |

Test date: 2023.03.07

| Engine | Model | File | Threads | Stream | Time | RTF | Quality |
| ------ | ----- | ---- | ------- | ------ | ---- | --- | ------- |
| Sherpa ncnn | small-2023-01-09 | 1 | 4 | + | 0.6s | 0.05 | okayish |
| Sherpa ncnn | small-2023-01-09 | 2 | 4 | + | 0.2s | 0.06 | low |
| Nvidia NeMo | en_conformer_ctc_small | 1 | 4 | - | 0.4s | 0.03 | perfect |
| Nvidia NeMo | en_conformer_ctc_small | 2 | 4 | - | 0.2s | 0.06 | perfect |
