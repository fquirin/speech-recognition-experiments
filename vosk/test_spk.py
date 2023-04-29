#!/usr/bin/env python3
import argparse
import os
from timeit import default_timer as timer
import wave
from pydub import AudioSegment, effects
import json

# Arguments
parser = argparse.ArgumentParser(description="Running Vosk speaker ID test.")
parser.add_argument("-f", "--folder", default="../test-files/", help="""Folder with speaker test WAV files.
Please name your files ref-[ID]-[n].wav and test-[ID]-[n].wav, e.g.: ref-S1-1.wav etc..""")
parser.add_argument("-m", "--model", default="models/vosk-model-small-en-us-0.15", help="Path to model")
parser.add_argument("-c", "--chunk-size-ms", default=1000, help="Chunk size for streaming in ms (default: 1000)")
args = parser.parse_args()

import numpy as np
from vosk import Model, KaldiRecognizer, SpkModel, SetLogLevel

# Vosk log level - -1: off, 0: normal, 1: more verbose
SetLogLevel(-2)

print("Loading model and recognizer ...")
model_path = args.model
spk_model = "models/vosk-model-spk-0.4"
model_load_start = timer()
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)
rec.SetSpkModel(SpkModel(spk_model))
print(f"Took {(timer() - model_load_start):.2f}s.")

chunk_size_ms = int(args.chunk_size_ms)
print(f"Chunk size for streaming: {chunk_size_ms}ms = {(chunk_size_ms*16)} samples")

speakers = []
speaker_ids = []
wrong_ids = 0
correct_ids = 0

def cosine_dist(x, y):
    nx = np.array(x)
    ny = np.array(y)
    return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)

def analyze_speaker(file_name, res):
    global correct_ids, wrong_ids
    this_id = file_name.split('-')[1]
    print(f"This ID: {this_id}")
    best_dist = 2
    best_id = None
    for id, spkr in enumerate(speakers):
        dist = cosine_dist(spkr, res["spk"])
        if dist < best_dist:
            best_dist = dist
            best_id = speaker_ids[id]
        print(f"Speaker distance: {speaker_ids[id]} = {dist:.2f}")
    if best_id is not None:
        print(f"Best match: {best_id} = {best_dist:.2f}")
        if this_id == best_id:
            print("CORRECT")
            correct_ids += 1
        elif this_id not in speaker_ids:
            print("UNKNOWN")
        else:
            print("WRONG")
            wrong_ids += 1

def store_speaker(file_name, res):
    speakers.append(res['spk'])
    speaker_ids.append(file_name.split("-")[1])

def transcribe(audio_file_name, do_store_speaker):
    audio_file = args.folder + audio_file_name
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
            if "spk" in res:
                if do_store_speaker:
                    store_speaker(audio_file_name, res)
                else:
                    analyze_speaker(audio_file_name, res)

    res = json.loads(rec.FinalResult())
    print(f"Out: {res['text']}")
    if "spk" in res:
        if do_store_speaker:
            store_speaker(audio_file_name, res)
        else:
            analyze_speaker(audio_file_name, res)
    print(f"Took: {(timer() - start_time):.2f}s")

test_files = os.listdir(args.folder)

print("\n---- Get reference speakers ...")
for file in test_files:
    if file.startswith("ref") and file.endswith(".wav"):
        transcribe(file, True)

print("\n---- Test speakers ...")
for file in test_files:
    if file.startswith("test") and file.endswith(".wav"):
#    if file.endswith(".wav"):
        transcribe(file, False)

print(f"\nDetected correct: {correct_ids}")
print(f"Detected wrong: {wrong_ids}")
