#!/bin/bash

waves=($(ls ../test-files/*.wav))

cd whisper.cpp

THREADS=2
MODEL="tiny"
LANG="en" # NOTE: supports "auto"
echo "Using model '$MODEL' with $THREADS threads and language '$LANG'"
echo ""

start_t=$(date +"%s.%N")
for wave in ${waves[@]}; do
  echo "Transcribing file: ../$wave"
  ./main -m "models/ggml-${MODEL}.bin" -f "../$wave" -t $THREADS -l $LANG
  echo ""
done
finish_t=$(date +"%s.%N")
echo "Total: $(expr $finish_t-$start_t | bc)s"
