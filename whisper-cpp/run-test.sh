#!/bin/bash
cd whisper.cpp

waves=(
"../../test-files/en_speech_jfk_11s.wav"
"../../test-files/en_sh_lights_70pct_4s.wav"
)

THREADS=2
MODEL="tiny"
echo "Using model '$MODEL' with $THREADS threads"
echo ""

start_t=$(date +"%s.%N")
for wave in ${waves[@]}; do
  echo "Transcribing file: $wave"
  ./main -m "models/ggml-${MODEL}.bin" -f "$wave" -t $THREADS
  echo ""
done
finish_t=$(date +"%s.%N")
echo "Total: $(expr $finish_t-$start_t | bc)s"
