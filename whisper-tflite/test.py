import os
from timeit import default_timer as timer
import wave
import argparse
#import json

print(f'Importing tensorflow and numpy')
import tensorflow as tf
#import tflite_runtime.interpreter as tf
import numpy as np
#import torch

print(f'Importing whisper')
import whisper

parser = argparse.ArgumentParser(description="Running Whisper TFlite test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-m", "--model", default="models/whisper.tflite", help="Path to model")
parser.add_argument("-t", "--threads", default=2, help="Threads used")
args = parser.parse_args()

model_path = args.model
print(f'Loading tflite model {model_path} ...')
interpreter = tf.lite.Interpreter(model_path, num_threads=int(args.threads))
interpreter.allocate_tensors()

def transcribe(audio_file):
    print(f'\nLoading audio file: {audio_file}')
    wf = wave.open(audio_file, "rb")
    sample_rate_orig = wf.getframerate()
    audio_length = wf.getnframes() * (1 / sample_rate_orig)
    if (wf.getnchannels() != 1 or wf.getsampwidth() != 2
        or wf.getcomptype() != "NONE" or sample_rate_orig != 16000):
        print("Audio file must be WAV format mono PCM.")
        exit (1)
    wf.close()
    print(f'Samplerate: {sample_rate_orig}, length: {audio_length}s')

    inference_start = timer()

    print(f'Calculating mel spectrogram...')
    mel_from_file = whisper.audio.log_mel_spectrogram(audio_file)
    input_data = whisper.audio.pad_or_trim(mel_from_file, whisper.audio.N_FRAMES)
    input_data = np.expand_dims(input_data, 0)
    #print("Input data shape:", input_data.shape)

    #input_data = np.frombuffer(wf.readframes(wf.getnframes()), np.int16)
    #input_data = np.random.randn(1, 256, 256, 3)

    input_details = interpreter.get_input_details()
    interpreter.resize_tensor_input(input_details[0]['index'], input_data.shape)

    interpreter.set_tensor(input_details[0]['index'], input_data)

    print("Invoking interpreter ...")
    interpreter.invoke()

    print("Preparing output data ...")
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    #output_data = output_data.squeeze()
    #print(output_data)
    #np.savetxt("output.txt", output_data)
    #print(interpreter.get_output_details()[0])

    # convert tokens to text
    print("Converting tokens ...")
    wtokenizer = whisper.tokenizer.get_tokenizer(False, language="en")
    for token in output_data:
        #print(token)
        token[token == -100] = wtokenizer.eot
        text = wtokenizer.decode(token, skip_special_tokens=True)
        print(text)

    print("\nInference took {:.3}s for {:.3}s audio file.".format(
        timer() - inference_start, audio_length))

test_files = os.listdir(args.folder)
for file in test_files:
    if file.endswith(".wav"):
        transcribe(args.folder + file)
