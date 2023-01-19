#!/bin/bash

waves=($(ls ../test-files/*.wav))

cd whisper.cpp

THREADS=2
MODEL="tiny"
echo "Using model '$MODEL' with $THREADS threads"
echo ""

start_t=$(date +"%s.%N")
for wave in ${waves[@]}; do
  echo "Transcribing file: ../$wave"
  ./main -m "models/ggml-${MODEL}.bin" -f "../$wave" -t $THREADS
  echo ""
done
finish_t=$(date +"%s.%N")
echo "Total: $(expr $finish_t-$start_t | bc)s"
