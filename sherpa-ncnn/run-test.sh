#!/usr/bin/env bash
set -e

waves=($(ls ../test-files/*.wav))

cd sherpa-ncnn
EXE="./build/bin/sherpa-ncnn"
which $EXE

#MODEL="./models/sherpa-ncnn-conv-emformer-transducer-small-2023-01-09"
MODEL="./models/sherpa-ncnn-streaming-zipformer-en-2023-02-13"
THREADS=2
echo "Model: $MODEL"
echo "Threads: $THREADS"
echo ""

start_t=$(date +"%s.%N")
for wave in ${waves[@]}; do
  echo "Transcribing file: ../$wave"
  time $EXE \
    $MODEL/tokens.txt \
    $MODEL/encoder_jit_trace-pnnx.ncnn.param \
    $MODEL/encoder_jit_trace-pnnx.ncnn.bin \
    $MODEL/decoder_jit_trace-pnnx.ncnn.param \
    $MODEL/decoder_jit_trace-pnnx.ncnn.bin \
    $MODEL/joiner_jit_trace-pnnx.ncnn.param \
    $MODEL/joiner_jit_trace-pnnx.ncnn.bin \
    "../$wave" "$THREADS"
    #$wave 4 greedy_search
  echo ""
done
finish_t=$(date +"%s.%N")
echo "Total: $(expr $finish_t-$start_t | bc)s"
