# Whisper for CTranslate2

A port of Open-AI Whisper for CTranslate2.  

Repositories:
- Whisper original: https://github.com/openai/whisper
- Faster Whisper: https://github.com/guillaumekln/faster-whisper

Tested with:
- Arm64 - Debian 11 - Python 3.9
- x86_64 - Debian 11 - Python 3.9

## Tweaking results

- Use `python3 test.py -h` to check-out the possible arguments
- Language is set to `auto` by default, which will use the code of the test files (`en_...`) if given. If not it will use the Whisper detector. Use `--lang en` etc. to skip detection.
- Beam-size is 1 by default which is technically the fastest decoding strategy, but it might be worth to play around with it (e.g. `--beamsize 4` or `--beamsize 64`) to see how it affects speed and accuracy.
- There is a magical Whisper parameter called 'initial_prompt' that will prime the model in some unpredictable way ^^. It can influence accuracy and style of the transcription. Example: `--init-prompt "Hey SEPIA, set a timer`.
