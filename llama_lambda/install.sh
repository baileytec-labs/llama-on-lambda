#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt


read -p "Please provide the direct link to the model you'd like to use (Default https://huggingface.co/vihangd/open_llama_7b_300bt_ggml/resolve/main/ggml-model-q4_0.bin):" MODELURL

MODELURL=${MODELURL:-https://huggingface.co/vihangd/open_llama_7b_300bt_ggml/resolve/main/ggml-model-q4_0.bin}

echo "Downloading $MODELURL"

wget -O ./llama_cpp_docker/modelfile.bin "$MODELURL"

cdk deploy
