import os
from timeit import default_timer as timer
import wave
import argparse
#import json

parser = argparse.ArgumentParser(description="Running Whisper TFlite test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-m", "--model", default="models/whisper.tflite", help="Path to model")
parser.add_argument("-t", "--threads", default=2, help="Threads used")
parser.add_argument("-l", "--lang", default="en", help="Language used")
parser.add_argument("-r", "--runtime", default="1", help="Tensorflow runtime, 1: 'tf.lite' or 2: 'tflite_runtime'")
args = parser.parse_args()

if args.runtime == "1":
    print(f'Importing tensorflow (for tf.lite)')
    import tensorflow as tf
else:
    print(f'Importing tflite_runtime')
    import tflite_runtime.interpreter as tf

print(f'Importing numpy')
import numpy as np
#import torch

print(f'Importing whisper')
import whisper

model_path = args.model
print(f'Loading tflite model {model_path} ...')
if args.runtime == "1":
    interpreter = tf.lite.Interpreter(model_path, num_threads=int(args.threads))
else:
    interpreter = tf.Interpreter(model_path, num_threads=int(args.threads))
interpreter.allocate_tensors()
input_tensor = interpreter.get_input_details()[0]['index']
output_tensor = interpreter.get_output_details()[0]['index']
if args.lang == "en":
    wtokenizer = whisper.tokenizer.get_tokenizer(False, language="en")
else:
    wtokenizer = whisper.tokenizer.get_tokenizer(True, language=args.lang)

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

    print("Invoking interpreter ...")
    interpreter.set_tensor(input_tensor, input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_tensor)

    print("Preparing output data ...")
    output_details = interpreter.get_output_details()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    #output_data = output_data.squeeze()
    #print(output_data)
    #np.savetxt("output.txt", output_data)
    #print(interpreter.get_output_details()[0])

    # convert tokens to text
    print("Converting tokens ...")
    for token in output_data:
        #print(token)
        token[token == -100] = wtokenizer.eot
        text = wtokenizer.decode(token, skip_special_tokens=True)
        print(text)

    print("\nInference took {:.2f}s for {:.2f}s audio file.".format(
        timer() - inference_start, audio_length))

test_files = os.listdir(args.folder)
for file in test_files:
    if file.endswith(".wav"):
        transcribe(args.folder + file)
