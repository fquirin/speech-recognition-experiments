#!/bin/bash

TEST_FILES="../test-files/"
waves=($(ls "$TEST_FILES"*.wav))

THREADS=2
MODEL="tiny"
LANG="en" # NOTE: supports "auto"
BEAM_SIZE=1
INIT_PROMPT=""

echo "Using model '$MODEL' with language '$LANG', beam-size=$BEAM_SIZE and $THREADS threads"
if [ ! -z "$INIT_PROMPT" ]; then
	echo "Initial prompt: $INIT_PROMPT"
fi
echo ""

cd whisper.cpp

start_t=$(date +"%s.%N")
for wave in ${waves[@]}; do
  echo "Transcribing file: ../$wave"
  ./main -m "models/ggml-${MODEL}.bin" -f "../$wave" -t $THREADS -l $LANG --beam-size $BEAM_SIZE --prompt "$INIT_PROMPT"
  echo ""
done
finish_t=$(date +"%s.%N")
echo "Total: $(expr $finish_t-$start_t | bc)s"
