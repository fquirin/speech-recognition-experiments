import os
import argparse
from datetime import datetime
from timeit import default_timer as timer

import sounddevice as sd

import numpy as np

from openwakeword.model import Model
from openwakeword import get_pretrained_model_paths


# Parse input arguments
parser = argparse.ArgumentParser(description="Run OpenWakeWord detection.")
parser.add_argument(
    "-m", "--model", help="Model name (must be in list of available models atm)",
    default="hey_jarvis"
)
parser.add_argument(
    "-c", "--chunk_size", help="Audio chunk size in samples. Use multiples of 1280 (80ms).",
    type=int, default=1280
)
parser.add_argument(
    "-d", "--audio_device", help="Index of audio device to use for recording.",
    default=None
)
args=parser.parse_args()


available_models = get_pretrained_model_paths()
selected_model = None
print("\nAvailable models:")
for i, mdl in enumerate(available_models):
    name = os.path.basename(mdl)
    print(f"{i}: {name}")
    if name.startswith(args.model):
        selected_model = mdl
print(f"Selected model: {selected_model}\n")

# Load pre-trained openwakeword models
owwModel = Model(
    wakeword_model_paths=[selected_model],
    enable_speex_noise_suppression=False,
    vad_threshold=0
)
ww_detected_ts = 0
NEXT_ACTIVATION_DELAY_S = 5

def process_audio(audio_chunk: np.ndarray):
    global ww_detected_ts
    # Feed to openWakeWord model
    prediction = owwModel.predict(audio_chunk)
    ww_detected = False
    for key, value in prediction.items():
        if value > 0.66:
            current_time = datetime.now().strftime("%H:%M:%S")
            print(f"{current_time} - {key}: {value}")
            if timer() - ww_detected_ts > NEXT_ACTIVATION_DELAY_S:
                ww_detected_ts = timer()
                ww_detected = True
    return ww_detected


# Get microphone stream
FORMAT = np.int16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = args.chunk_size
if args.audio_device is not None:
    AUDIO_DEVICE = int(args.audio_device)
else:
    AUDIO_DEVICE = None
audio_stream = None

print("\nAvailable audio devices:")
for device in sd.query_devices():
    print(f"Index: {device['index']} - Name: {device['name']}")
print(f"Default devices (in/out): {sd.default.device}")
print("Note you can use '-d [index]' argument to change the device.")

def audio_handler(data: np.ndarray, frames, time, status):
    """Send audio from queue when new data arrives"""
    try:
        #audio_chunk = np.frombuffer(data, dtype=np.int16)
        audio_chunk = np.squeeze(data)
        if process_audio(audio_chunk):
            print("--WW DETECTED--")
    except Exception as err:
        print(f'Error in audio queue: {err}')

def stream_end():
    print("Stream END")


# Run capture loop continuously, checking for wake-words
if __name__ == "__main__":
    # Generate output string header
    print(f"\nListening for wake-word '{args.model}'...\n")
    try:
        with sd.InputStream(
            samplerate=RATE,
            channels=CHANNELS,
            dtype=FORMAT,
            blocksize=CHUNK_SIZE,
            device=AUDIO_DEVICE,
            callback=audio_handler,
            finished_callback=stream_end
        ) as audio_stream:
            #sd.sleep(1000000)
            input("--> Press ENTER or CTRL+C to END recording <--\n\n")
    except KeyboardInterrupt:
        print(" STOP ");
