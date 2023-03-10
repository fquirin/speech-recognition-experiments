# Adapted from 'asr_language_modeling/ngram_lm/eval_beamsearch_ngram.py

import os
import argparse
from timeit import default_timer as timer
import wave
from typing import List, Dict, Optional

parser = argparse.ArgumentParser(description="Running NVIDIA NeMo ASR with LM test inference.")
parser.add_argument("-f", "--folder", default="../test-files/", help="Folder with WAV input files")
parser.add_argument("-s", "--transcriptions", default=None, help="Folder with transcriptions for WAV files")
parser.add_argument("-m", "--acoustic-model", default="models/stt_en_conformer_ctc_small.nemo", help="Path to acoustic model")
parser.add_argument("-l", "--language-model", default="models/kenlm_custom.4gram", help="Path to n-gram language model")
parser.add_argument("-w", "--beam-widths", nargs='+', default=[8], type=int, help="Integer value(s) for beam_width (aka beam-size) (default: 8)")
parser.add_argument("-a", "--beam-alphas", nargs='+', default=[0.0, 1.0, 2.0], type=float, help="Float value(s) for beam_alpha (default: 0.0 1.0 2.0)")
parser.add_argument("-b", "--beam-betas", nargs='+', default=[0.0, 2.0, 4.0], type=float, help="Float value(s) for beam_beta (default: 0.0 2.0 4.0)")
parser.add_argument("-v", "--all-hypos", action='store_true', help="Return all hypotheses given by beam-width instead of best.")
parser.add_argument("-t", "--threads", default=2, help="Threads used (default: 2)")
args = parser.parse_args()

print("Importing torch ...")
import torch
torch.set_num_threads(int(args.threads))
print(f"Torch threads: {torch.get_num_threads()} - Device: CPU")

from sklearn.model_selection import ParameterGrid
import editdistance

print("Importing nemo ...")
from nemo.utils import logging
logging.setLevel(logging.ERROR)

import nemo.collections.asr as nemo_asr
from nemo.collections.asr.parts.submodules import ctc_beam_decoding
from nemo.utils import logging


class BeamSearchNGramConfig:
    # The path of the '.nemo' file of the ASR model
    nemo_model_file: str = args.acoustic_model

    # The path of the KenLM binary model file
    kenlm_model_file: Optional[str] = args.language_model

    # The (torch) device to load the model onto to calculate log probabilities
    device: str = "cpu"

    # Beam Search hyperparameters

    # The decoding scheme to be used for evaluation.
    # In theory this can be one of ["greedy", "beamsearch", "beamsearch_ngram"]
    decoding_mode: str = "beamsearch_ngram"  # ... but we've only implement this here
    decoding_strategy: str = "beam"  # Supports 'beam' and new: 'flashlight'
    return_best_hypothesis: bool = not args.all_hypos  # Return only "best" hypothesis or all beams

    beam_width: List[int] = args.beam_widths  # One or more widths for beam search decoding, e.g. [4, 8]
    beam_alpha: List[float] = args.beam_alphas  # One or more alpha parameters for the beam search decoding, e.g. [0.0, 1.0, 2.0, 5.0]
    beam_beta: List[float] = args.beam_betas  # One ore more beta parameters for the beam search decoding, e.g. [0.0, 1.0, 2.0, 4.0]


def beam_search_eval(
    model: nemo_asr.models.ASRModel,
    cfg: BeamSearchNGramConfig,
    char_log_probs: torch.Tensor,
    beam_alpha: float = 1.0,
    beam_beta: float = 2.0,
    beam_width: int = 8
):
    """
    Apply n-gram KenLM language model to character log probabilities via beam search decoding.
    """
    level = logging.getEffectiveLevel()
    logging.setLevel(logging.CRITICAL)
    # Reset config
    model.change_decoding_strategy(None)

    # Override the beam search config with current search candidate configuration
    beamConfig: ctc_beam_decoding.BeamCTCInferConfig = ctc_beam_decoding.BeamCTCInferConfig(
        beam_size = beam_width,
        beam_alpha = beam_alpha,
        beam_beta = beam_beta,
        return_best_hypothesis = cfg.return_best_hypothesis,
        kenlm_path = cfg.kenlm_model_file
    )

    # Update model's decoding strategy config
    model.cfg.decoding.strategy = cfg.decoding_strategy
    model.cfg.decoding.beam = beamConfig

    # Update model's decoding strategy
    model.change_decoding_strategy(model.cfg.decoding)
    logging.setLevel(level)

    # disabling type checking
    probs_lengths = torch.tensor([char_log_probs.shape[0]])
    with torch.no_grad():
        # we build a "batch" with a single entry
        packed_batch = torch.zeros(1, max(probs_lengths), char_log_probs.shape[-1], device='cpu')
        packed_batch[0, : probs_lengths[0], :] = torch.tensor(
            char_log_probs, device=packed_batch.device, dtype=packed_batch.dtype
        )
        if cfg.return_best_hypothesis:
            # returns: best_hyp_text
            all_hyps_batch = model.decoding.ctc_decoder_predictions_tensor(
                decoder_outputs=packed_batch, decoder_lengths=probs_lengths, return_hypotheses=True,
            )
        else:
            # returns: best_hyp_text, all_hyp_text
            _, all_hyps_batch = model.decoding.ctc_decoder_predictions_tensor(
                decoder_outputs=packed_batch, decoder_lengths=probs_lengths, return_hypotheses=True,
            )
    return all_hyps_batch[0]  # we only have one entry in our "pseudo" batch


def transcribe(
    asr_model: nemo_asr.models.ASRModel,
    cfg: BeamSearchNGramConfig,
    audio_file: str,
    transcript_file: str
):
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
    
    if transcript_file is not None and os.path.exists(transcript_file):
        with open(transcript_file, 'r') as file:
            target_transcript = file.read().replace('\n', ' ')
        print(f'Expected result: {target_transcript} - from file: {transcript_file}')
    else:
        target_transcript = None

    start_time = timer()
    
    with torch.no_grad():
        #transcribe() generates a text applying a CTC greedy decoder to raw probabilities distribution over
        #alphabet's characters from ASR model. We can get those raw probabilities with logprobs=True argument.
        print("Calculating character probabilities ...")
        batch_size: int = 1  # 1 file at a time
        all_log_probs = asr_model.transcribe(paths2audio_files=[audio_file], batch_size=batch_size, logprobs=True)
    char_log_probs = all_log_probs[0]  #we work with a single audio file
    
    prob_time = timer() - start_time
    print(f"Took: {prob_time:.2f}s")
    
    # beam search has to run on CPU?
    #asr_model = asr_model.to('cpu')

    params = {'beam_width': cfg.beam_width, 'beam_alpha': cfg.beam_alpha, 'beam_beta': cfg.beam_beta}
    transcription_results: List[Dict] = []
    
    # build all combinations for testing
    hp_grid = ParameterGrid(params)
    hp_grid = list(hp_grid)
    for hp in hp_grid:
        beam_width = hp['beam_width']
        beam_alpha = hp['beam_alpha']
        beam_beta = hp['beam_beta']
        print(f"Starting beam search for beam-width: {beam_width}, beam-alpha: {beam_alpha}, beam-beta: {beam_beta} ...")
        start_time = timer()
        all_hypos = beam_search_eval(
            asr_model,
            cfg,
            char_log_probs=char_log_probs,
            beam_width=beam_width,
            beam_alpha=beam_alpha,
            beam_beta=beam_beta
        )
        beam_time = timer() - start_time
        for candidate_idx, candidate in enumerate(all_hypos):  # type: (int, ctc_beam_decoding.rnnt_utils.Hypothesis)
            pred_text = candidate.text
            score = candidate.score
            #print(f"beam_i: {candidate_idx} -- text: {pred_text} -- score: {score}")
            transcription_results.append({
                "cer": editdistance.eval(pred_text, target_transcript) if target_transcript is not None else None,
                "text": pred_text,
                "params": [candidate_idx, beam_width, beam_alpha, beam_beta],
                "time": f"{(prob_time + beam_time):.2f}s"
            })

    if target_transcript is not None:
        print("Sorting results...")
        transcription_results.sort(key=lambda x: x['cer'], reverse=True)
        for res in transcription_results:
            print(f"cer: {res['cer']} - params: {res['params']} - text: {res['text']} - time: {res['time']}")
    else:
        if len(transcription_results) == 1:
            res = transcription_results[0]
            print(f"text: {res['text']}")
            print(f"Total: {res['time']}")
        else:
            for res in transcription_results:
                print(f"params: {res['params']} - text: {res['text']} - time: {res['time']}")


def main():
    print("Start")
    cfg = BeamSearchNGramConfig()

    #valid_decoding_modes = ["greedy", "beamsearch", "beamsearch_ngram"]
    valid_decoding_modes = ["beamsearch_ngram"]
    if cfg.decoding_mode not in valid_decoding_modes:
        raise ValueError(
            f"Given decoding_mode={cfg.decoding_mode} is invalid. Available options are :\n" f"{valid_decoding_modes}"
        )

    print("Loading local model...")
    asr_model = nemo_asr.models.ASRModel.restore_from(cfg.nemo_model_file, map_location=torch.device(cfg.device))

    test_files = os.listdir(args.folder)
    transcription_files = os.listdir(args.transcriptions) if args.transcriptions is not None else None
    for file in test_files:
        if file.endswith(".wav"):
            audio_file = args.folder + file
            if transcription_files is not None:
                # get the matching [filename].txt for [filename].wav
                transcript_file = args.transcriptions + os.path.splitext(file)[0] +'.txt'
            else:
                transcript_file = None
            transcribe(
                asr_model=asr_model,
                cfg=cfg,
                audio_file=audio_file,
                transcript_file=transcript_file
            )


if __name__ == '__main__':
    main()
