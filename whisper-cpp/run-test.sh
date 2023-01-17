#!/bin/bash
waves=(
"../test-files/en_speech_jfk_11s.wav"
"../test-files/en_sh_lights_70pct_4s.wav"
)

THREADS=2
MODEL="tiny"

echo "Using model $MODEL with $THREADS threads"
start_t=$(date +"%s.%N")
for wave in ${waves[@]}; do
  ./main -m "models/ggml-${MODEL}.bin" -f "$wave" -t $THREADS
done
finish_t=$(date +"%s.%N")
echo "Took: $(expr $finish_t-$start_t | bc)s"
