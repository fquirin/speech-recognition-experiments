#!/bin/bash
start_t=$(date +"%s.%N")
time python3 test.py
finish_t=$(date +"%s.%N")
echo "Took: $(expr $finish_t-$start_t | bc)s"

