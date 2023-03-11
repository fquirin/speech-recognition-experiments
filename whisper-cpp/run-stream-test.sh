#!/bin/bash

echo "This script requires a microphone and will use default system settings."
echo "Your sound-cards are:"
echo ""
cat /proc/asound/cards
echo ""
echo "To test your mic you can use:"
echo "arecord -r 16000 -f S16_LE -c 1 -d 6 test.wav"
echo ""

THREADS=4
MODEL="tiny"
LANG="en"
#CAPTURE_DEVICE="-1"
AUDIO_STEP_MS=5000
AUDIO_LEN_MS=5000
VAD_THRESH=0.5

echo "Using model '$MODEL' with language '$LANG' and $THREADS threads"
echo "To see all options run './stream -h' in 'whisper.cpp' folder."
echo "To learn more visit:"
echo "https://github.com/ggerganov/whisper.cpp/tree/master/examples/stream"
echo ""
read -p "Press any key to continue (CTRL+C to abort)."

cd whisper.cpp
#./stream -m "models/ggml-${MODEL}.bin" -l $LANG  -t $THREADS --step $AUDIO_STEP_MS --length $AUDIO_LEN_MS --keep-context
./stream -m "models/ggml-${MODEL}.bin" -l $LANG  -t $THREADS --step $AUDIO_STEP_MS --length $AUDIO_LEN_MS
#./stream -m "models/ggml-${MODEL}.bin" -l $LANG  -t $THREADS --step 0 --length $AUDIO_LEN_MS --vad-thold $VAD_THRESH
