echo "Installing OpenWakeWord requirements ..."
sudo apt update
sudo apt-get install -y --no-install-recommends git python3-pip python3-dev python3-venv python3-setuptools python3-wheel portaudio19-dev
# Virtual env?
if [ -d "venv" ]; then
	source "venv/bin/activate"
else
	python3 -m venv "venv"
	source "venv/bin/activate"
fi
# Packages
pip3 install --upgrade pip
pip3 install openwakeword sounddevice
#git clone https://github.com/dscripka/openWakeWord.git
# Models (already included in 'openwakeword' package)
#mkdir -p models
#cd models
#wget https://github.com/dscripka/openWakeWord/raw/main/openwakeword/resources/models/hey_jarvis_v0.1.onnx
#cd ..
echo "DONE"
