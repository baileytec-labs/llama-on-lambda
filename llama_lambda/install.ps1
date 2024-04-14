# This script should be run with PowerShell

# Create a Python virtual environment
python -m venv .venv
# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Prompt the user for the model URL
$modelURL = Read-Host "Please provide the direct link to the model you'd like to use (Default https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf)"

# If no URL is provided, use the default
if ([string]::IsNullOrEmpty($modelURL)) {
    $modelURL = "https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf"
}

# Deploy using the cdk command, adjusting for correct context parameter usage in PowerShell
cdk deploy --context modelfile=$modelURL
