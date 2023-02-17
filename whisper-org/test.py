import os
from timeit import default_timer as timer
import argparse

parser = argparse.ArgumentParser(description="Running Whisper (original) test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-m", "--model", default="tiny", help="Model name")
parser.add_argument("-l", "--lang", default="en", help="Language used (default: en)")
parser.add_argument("-b", "--beamsize", default=1, help="Beam size used (default: 1)")
args = parser.parse_args()

print("Importing whisper")
import whisper

model_name = args.model
beam_size = int(args.beamsize)
print(f"Loading model {model_name}")
model = whisper.load_model(model_name)
print("Threads: max (this version always tries to use all available threads)")

def transcribe(audio_file):
    inference_start = timer()

    # load audio and pad/trim it to fit 30 seconds
    print(f"\nLoading audio {audio_file} ...")
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    print("Calculating mel spectrogram ...")
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # detect spoken language
    auto_lang = None
    if ".en" in model_name:
        auto_lang = "en"
        print("Language fixed to 'en'")
    elif args.lang == "auto":
        print("Detect language ...")
        _, probs = model.detect_language(mel)
        auto_lang = max(probs, key=probs.get)
        print(f"Detected language: {auto_lang}")

    # decode audio
    print("Decode audio ...")
    if auto_lang is not None:
        options = whisper.DecodingOptions(fp16 = False, language=auto_lang, beam_size=beam_size)
    else:
        options = whisper.DecodingOptions(fp16 = False, language=args.lang, beam_size=beam_size)
    #print(options)
    #options: task='transcribe', language=None, temperature=0.0, sample_len=None, best_of=None, beam_size=None, patience=None, length_penalty=None, prompt=None, prefix=None, suppress_blank=True, suppress_to>
    result = whisper.decode(model, mel, options)

    # print the recognized text
    print("Result:")
    print(result.text)

    print("\nInference took {:.2f}s.".format(timer() - inference_start))

test_files = os.listdir(args.folder)
for file in test_files:
    if file.endswith(".wav"):
        transcribe(args.folder + file)
