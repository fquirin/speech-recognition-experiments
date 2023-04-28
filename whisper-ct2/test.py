import os
import re
from timeit import default_timer as timer
import wave
import argparse

parser = argparse.ArgumentParser(description="Running Whisper CT2 test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-m", "--model", default="models/whisper-tiny-ct2", help="Path to model")
parser.add_argument("-l", "--lang", default="auto", help="Language used (default: auto)")
parser.add_argument("-b", "--beamsize", default=1, help="Beam size used (default: 1)")
parser.add_argument("-p", "--init-prompt", default=None, help="Initial prompt (default: None)")
parser.add_argument("-v", "--verbose", action="store_true", help="Get word-level ts and confidence (default: false)")
parser.add_argument("--vad", action="store_true", help="Use VAD to filter silence (>2s by default).")
parser.add_argument("--fp32", action="store_true", help="Use float32 compute type for models.")
parser.add_argument("-i", "--interpret", action="store_true", help="Translate to 'en' (default: false)")
parser.add_argument("-t", "--threads", default=2, help="Threads used (default: 2)")
args = parser.parse_args()

print(f'Importing WhisperModel')
from faster_whisper import WhisperModel

# run on CPU with INT8:
model_path = args.model
print(f'\nLoading model {model_path} ...')
compute_type = "float32" if args.fp32 else "int8"
model = WhisperModel(model_path, device="cpu", compute_type=compute_type, cpu_threads=int(args.threads))
#model = WhisperModel(args.model, device="cuda", compute_type="float16")
print(f'Threads: {args.threads}')
print(f'Beam size: {args.beamsize}')
print(f'Compute type: {compute_type}')

initial_prompt=args.init_prompt
if initial_prompt is not None:
    print(f'Initial prompt: {initial_prompt}')

def transcribe(audio_file):
    print(f'\n---- Loading audio file: {audio_file}')
    wf = wave.open(audio_file, "rb")
    sample_rate_orig = wf.getframerate()
    audio_length = wf.getnframes() * (1 / sample_rate_orig)
    if (wf.getnchannels() != 1 or wf.getsampwidth() != 2
        or wf.getcomptype() != "NONE" or sample_rate_orig != 16000):
        print("Audio file must be WAV format mono PCM.")
        exit (1)
    wf.close()
    print(f'Samplerate: {sample_rate_orig}, length: {audio_length}s')

    file_lang = None
    lang_search = re.findall(r"(?:^|/)(\w\w)_", audio_file)
    if len(lang_search) > 0:
        file_lang = lang_search.pop()
    
    inference_start = timer()

    print("\nTranscribing ...")
    segments = None
    info = None
    skip_file = False
    trans_lang = None
    if ".en" in model_path:
        if file_lang is not None and file_lang != "en":
            print(f"Language found in file name: {file_lang}")
            print("Skipped file to avoid issues with '.en' model")
            skip_file = True
        else:
            trans_lang = None
            print("Model language fixed to 'en'")
    elif args.lang == "auto":
        if file_lang is not None:
            trans_lang = file_lang
            print(f"Language found in file name: {file_lang}")
    else:
        trans_lang = args.lang
        print(f'Pre-defined language: {args.lang}')

    if not skip_file:
        segments, info = model.transcribe(
            audio_file,
            beam_size=int(args.beamsize),
            language=trans_lang,
            initial_prompt=initial_prompt,
            word_timestamps=args.verbose,
            task="transcribe" if not args.interpret else "translate",
            vad_filter=args.vad
        )
        if trans_lang is None or trans_lang == "auto":
            print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
        if segments is not None:
            print("Result:")
            for segment in segments:
                if args.verbose:
                    for word in segment.words:
                        print("[%.2fs -> %.2fs] %s (conf.: %.2fs)" % (word.start, word.end, word.word, word.probability))
                else:
                    print("[%ds -> %ds] %s" % (segment.start, segment.end, segment.text))
            
            print("\nInference took {:.2f}s for {:.2f}s audio file.".format(
                timer() - inference_start, audio_length))

test_files = os.listdir(args.folder)
for file in test_files:
    if file.endswith(".wav"):
        transcribe(args.folder + file)
