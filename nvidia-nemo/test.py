import os
import argparse
from timeit import default_timer as timer
import wave

parser = argparse.ArgumentParser(description="Running NVIDIA NeMo ASR test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-m", "--model", default="models/stt_en_conformer_ctc_small.nemo", help="Path to model")
parser.add_argument("-t", "--threads", default=2, help="Threads used (default: 2)")
#parser.add_argument("-l", "--lang", default="en", help="Language used (default: en)")
args = parser.parse_args()

print("Importing torch...")
import torch
torch.set_num_threads(int(args.threads))
#has_gpu = torch.cuda.is_available()
print(f"Torch threads: {torch.get_num_threads()} - Device: CPU")

print("Importing nemo...")
# Log-level:
from nemo.utils import logging
logging.setLevel(logging.ERROR)
#logging.setLevel(logging.CRITICAL)
import nemo
# NeMo's ASR collection - this collections contains complete ASR models and
# building blocks (modules) for ASR
import nemo.collections.asr as nemo_asr
from nemo.utils import model_utils

model_path = args.model
print(f"Model path: {model_path}")

print("Loading local model...")

model_cfg = nemo_asr.models.ASRModel.restore_from(restore_path=model_path, return_config=True)
classpath = model_cfg.target  # original class path
imported_class = model_utils.import_class_by_path(classpath)  # type: ASRModel
logging.info(f"Restoring local model : {imported_class.__name__}")
# we can load models from online repository instead:
#model = nemo_asr.models.ASRModel.from_pretrained(model_name, map_location=torch.device(cfg.device))

# load model from checkpoint
map_location = torch.device("cpu")
model = imported_class.restore_from(restore_path=model_path, map_location=map_location)  # type: ASRModel
model.freeze()
model = model.cpu()

print("Start transcribing...")

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

    start_time = timer()

    print("\nTranscribing ...")
    with torch.no_grad():
        print(model.transcribe(paths2audio_files=[audio_file], batch_size=1))
    print("Took: {:3}s".format(timer() - start_time))

test_files = os.listdir(args.folder)
for file in test_files:
    if file.endswith(".wav"):
        transcribe(args.folder + file)
