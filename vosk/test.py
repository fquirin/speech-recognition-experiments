#!/usr/bin/env python3
import argparse
import os
from timeit import default_timer as timer
from pydub import AudioSegment, effects
import json

# Arguments
parser = argparse.ArgumentParser(description="Running Vosk test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-m", "--model", default="models/vosk-model-small-en-us-0.15", help="Path to model")
parser.add_argument("-c", "--chunk-size-ms", default=500, help="Chunk size for streaming in ms (default: 500)")
parser.add_argument("-s", "--detect-speaker", action="store_true", help="Calculate speaker vector")
#parser.add_argument("-t", "--threads", default=1, help="Threads used (default: 1)") # Vosk CPU runs single core
#parser.add_argument("--alternatives", type=int, default=0,
#    help="Number of alternative transcripts to include in JSON output",
#)
#parser.add_argument("--words", action="store_true",
#    help="Show each word with timestamp",
#)
args = parser.parse_args()

import numpy as np
from vosk import Model, KaldiRecognizer, SpkModel, SetLogLevel

# Vosk log level -1: less verbose, 0: normal, 1: more verbose
SetLogLevel(-1)

print("Loading model and recognizer ...")
model_path = args.model
spk_model = "models/vosk-model-spk-0.4"
model_load_start = timer()
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)
#rec.SetWords(args.words)
#rec.SetMaxAlternatives(args.alternatives)
if args.detect_speaker:
    rec.SetSpkModel(SpkModel(spk_model))
print(f"Took {(timer() - model_load_start):.2f}s.")

chunk_size_ms = int(args.chunk_size_ms)
print(f"Chunk size for streaming: {chunk_size_ms}ms = {(chunk_size_ms*16)} samples")

speakers = []

def cosine_dist(x, y):
    nx = np.array(x)
    ny = np.array(y)
    return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

def analyze_speaker(res):
    if len(speakers) == 0:
        print(res['spk'])
    speakers.append(res['spk'])
    print("Speaker distance:", cosine_dist(speakers[0], res["spk"]))

def transcribe(audio_file):
    print(f'\n---- Loading audio file: {audio_file}')
    audio = AudioSegment.from_file(audio_file, format="wav")
    sample_rate_orig = audio.frame_rate
    audio_length = audio.duration_seconds
    if (audio.channels != 1 or audio.sample_width != 2
        or sample_rate_orig != 16000):
        print("Audio file must be WAV format mono PCM.")
        exit (1)
    #print(f"Max audio amp.: {(audio.max/32768):.2f}")
    print(f"Max audio amp.: {audio.max_dBFS:.2f} dB")
    #audio = effects.normalize(audio)
    #print(f"Max audio amp. after norm.: {audio.max}")
    print(f'Samplerate: {sample_rate_orig}, length: {audio_length}s')

    print("Running chunked inference ...")
    start_time = timer()

    #chunk_size = 25000  # 250ms = 4000 samples
    for i in range(0, len(audio), chunk_size_ms):
        chunk = audio[i:i+chunk_size_ms]
        if rec.AcceptWaveform(chunk.raw_data):
            res = json.loads(rec.Result())
            print(f"Out: {res['text']}")
            if args.detect_speaker and "spk" in res:
                analyze_speaker(res)

    res = json.loads(rec.FinalResult())
    print(f"Out: {res['text']}")
    if args.detect_speaker and "spk" in res:
        analyze_speaker(res)
    print(f"Took: {(timer() - start_time):2f}s")

test_files = os.listdir(args.folder)
for file in test_files:
    if file.endswith(".wav"):
        transcribe(args.folder + file)

#speakers = np.array(speakers)
#print(speakers.shape)
#print(speakers.mean(axis=0))
