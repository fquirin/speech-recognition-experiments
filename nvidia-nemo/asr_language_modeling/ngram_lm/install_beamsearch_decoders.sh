#!/usr/bin/env bash
# install Boost package
sudo apt update
sudo apt install swig build-essential libboost-all-dev cmake zlib1g-dev libbz2-dev liblzma-dev
git clone https://github.com/NVIDIA/OpenSeq2Seq
cd OpenSeq2Seq
git checkout ctc-decoders
cd ..
mv OpenSeq2Seq/decoders .
rm -rf OpenSeq2Seq
cd decoders
./setup.sh
cd ..
