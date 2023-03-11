#!/bin/bash
set -e
echo "Installing stream tool ..."
if [ ! -f "whisper.cpp/main" ]; then
	echo "Please install main tool first."
	exit 1
fi
echo ""
echo "NOTE: If you've used the argument 'BLAS' before please add it here as well!"
echo ""
sudo apt update
sudo apt install -y --no-install-recommends libsdl2-dev
cd whisper.cpp
if [ -n "$1" ] && [ "$1" == "BLAS" ]; then
	WHISPER_OPENBLAS=1 make stream
else
	make stream
fi
echo "DONE"
