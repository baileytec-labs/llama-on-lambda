python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

$MODELURL = Read-Host -Prompt "Please provide the direct link to the model you'd like to use (Default https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf)"
if ($MODELURL -eq "") {
    $MODELURL = "https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf"
}

$APIKEY = Read-Host -Prompt "Please provide your API key that you want your Lambda LLM Server to require when using (just hit enter if using legacy)"
if ($APIKEY -eq "") {
    $APIKEY = "insert_key_here"
}

cdk deploy -c modelfile=$MODELURL -c apikey=$APIKEY