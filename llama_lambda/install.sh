#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt


read -p "Please provide the direct link to the model you'd like to use (Default https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf):" MODELURL

MODELURL=${MODELURL:-https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf}

read -p "Please provide your API key that you want your Lambda LLM Server to require when using (just hit enter if using legacy):" APIKEY
APIKEY=${APIKEY:-insert_key_here}
cdk deploy -c modelfile=$MODELURL -c apikey=$APIKEY
