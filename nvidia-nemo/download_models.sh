#!/bin/bash
set -e
echo "Downloading models ..."
mkdir -p models
cd models
if [ ! -f "stt_en_conformer_ctc_small.nemo" ]; then
	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_ctc_small/versions/1.6.0/files/stt_en_conformer_ctc_small.nemo'
fi
#if [ ! -f "stt_en_conformer_transducer_small.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_transducer_small/versions/1.6.0/files/stt_en_conformer_transducer_small.nemo'
#fi
#if [ ! -f "stt_en_conformer_ctc_small_ls.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_ctc_small_ls/versions/1.0.0/files/stt_en_conformer_ctc_small_ls.nemo'
#fi
#if [ ! -f "stt_en_conformer_ctc_medium.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_ctc_medium/versions/1.6.0/files/stt_en_conformer_ctc_medium.nemo'
#fi
#if [ ! -f "stt_en_conformer_transducer_medium.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_transducer_medium/versions/1.6.0/files/stt_en_conformer_transducer_medium.nemo'
#fi
#if [ ! -f "stt_en_squeezeformer_ctc_medium_ls.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_squeezeformer_ctc_medium_ls/versions/1.13.0/files/stt_en_squeezeformer_ctc_medium_ls.nemo'
#fi
#if [ ! -f "stt_en_conformer_ctc_large.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_en_conformer_ctc_large/versions/1.10.0/files/stt_en_conformer_ctc_large.nemo'
#fi
#if [ ! -f "stt_de_conformer_ctc_large.nemo" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_de_conformer_ctc_large/versions/1.5.0/files/stt_de_conformer_ctc_large.nemo'
#fi
#if [ ! -f "de_kenlm.4gram" ]; then
#	wget 'https://api.ngc.nvidia.com/v2/models/nvidia/nemo/stt_de_conformer_ctc_large/versions/1.5.0_lm/files/kenlm.4gram'
#	mv "kenlm.4gram" "de_kenlm.4gram"
#fi
echo "DONE"
echo "Note: You can edit this script to download more/larger models and check-out"
echo "'https://catalog.ngc.nvidia.com/orgs/nvidia/collections/nemo_asr' for new ones."
