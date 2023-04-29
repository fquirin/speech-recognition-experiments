#!/bin/bash
set -e
echo "Installing Adapt-LM Tools ..."
sudo apt update
sudo apt install -y --no-install-recommends swig

ADAPT_LM_BRANCH=master
git clone --single-branch --depth 1 -b $ADAPT_LM_BRANCH https://github.com/fquirin/kaldi-adapt-lm.git
cd kaldi-adapt-lm
bash 1-download-requirements.sh
rm *.tar.gz

echo "Downloading models ..."
bash 2-download-model.sh en
#bash 2-download-model.sh de

echo "DONE"

