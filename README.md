# OpenLLaMa on AWS Lambda

:warning: **FOR EDUCATIONAL PURPOSES ONLY** :warning:

Docker images, code, buildspecs, and guidance provided as proof of concept only and for educational purposes only.

### Update: The Docker container has been upgraded to now be fully compatible with the [OpenAI API Spec](https://platform.openai.com/docs/api-reference/introduction)

## Backgorund

Today, there is an explosion of generative AI capabilities across various platforms. Recently, an [open source release of a LLaMa compatible model](https://github.com/openlm-research/open_llama) was trained on the open RedPyjama Dataset, which now opens the possibilities for more freedom to use these types of generative models in various applications. 

Efforts have also been made to make these models as efficient as possible via the [llama.cpp project](https://github.com/ggerganov/llama.cpp), enabling the usage of more accessible CPU and RAM configurations instead of the limited and expensive GPU capabilities. In fact, with many of the quantizations of these models, you can provide reasonably responsive inferences on as little as 4-6 GB of RAM on a CPU, and even on an Android smartphone, if you're patient enough.

This has sparked an idea -- What if we could have a scalable, serverless LLM Generative AI inference engine? After some experimentation, it turns out that not only is it possible, but it also works quite well! 

---

## Introducing OpenLLama on Lambda

The premise is rather simple: deploy a container which can run the llama.cpp converted models onto AWS Lambda. This gives the advantages of scale which Lambda provides, minimizing cost and maximizing compute availability for your project. This project contains the AWS CDK code to create and deploy a Lambda function leveraging your model of choice**, with a FastAPI frontend accessible from a Lambda URL. Lambda also provides a great case for developers and businesses which want to deploy functions such as this: You get 400k GB-s of Lambda Compute each month for free, meaning with proper tuning, you can have scalable inference of these Generative AI LLMs for minimal cost.


**Note that you will need to have ggml quantized versions of your model, and you will likely need model sizes which are under 6GB. Regardless, your inference RAM requirements cannot exceed 9GB, or your Lambda function will fail**

_Wait, what?_ 

Lambda Docker Containers have a hard limit of 10GB in size, but that offers plenty of room for these models. However, the models cannot be stored in the proper invocation directory, but you _can_ place them in `/opt`. By pre-baking the models ino the `/opt` directory, you can include the entire package into your function without needing extra storage.

---
## Requirements
* You need [Docker](https://www.docker.com/) installed on your system and running. You will be building a container.
* Go to [Huggingface](https://huggingface.co/models) and pick out a GGML quantized model compatible with llama.cpp.
* You need to have the [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) installed on your system, as well as an AWS account, proper credentials, etc.
* Python3.9+

---
## Installation

### The default installation deploys the new OpenAI API compatible endpoint. See the Usage sectionfor more details. If you would like to leverage the original legacy version of this deployment, simply rename the `llama_lambda/legacy_app.py` to `llama_lambda/app.py` and everything should run normally. I recommend you make a copy of the original app.py. Maybe call it something like "newapp.py"? 

Once you've installed the requirements, on Mac/Linux:

1) Download this repository.
2) cd into the root directory of this repo (/wherever/you/downloaded/it/llama-on-lambda)
3) `cd ./llama_lambda`
4) `chmod +x install.sh`
5) `./install.sh`
6) Follow the prompts, and when complete, the CDK will provide you with a Lambda Function URL to test the function.

Note that this could take quite some time to build (on an M1 MBP 16GB it took 1600s to complete, so go get a coffee.)

For Windows users, ensure you have the requirements properly installed, and do the following:

1) Download this repository
2) Open a command prompt terminal, and cd into the root directory of this repo.
3) `cd ./llama_lambda`
4) `powershell -File ./install.ps1`
    * Note that if you get a permissions based error, you can manually open the install.ps1 script and type out the commands manually. You will need to look into `Set-ExecutionPolicy`, and I will not be providing security recommendations for your system.
5) Follow the prompts, and when complete, the CDK will provide you with a Lambda Function URL to test the function.

Note: On first use, there is a chance an error will surface related to AWS allocation of DRAM for individual lambda functions.  This can happen even if the allocation in your region's service quotas is at the ~10GB limit.  An independent service request increase has to be sent to alter this hidden limit.

---

## Usage

### OPENAI COMPATIBLE API

Since the original development of this project, there has been an explosion in the development of the ggmml project into the gguf project, and all the trappings in between. I've updated the docker container and the cdk code to deploy a new optimized Lambda function which is fully compatible with the OpenAI API Spec using the [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) library. This means you can deploy your function using a model (I recommend a 3B or smaller, the current configuration is set up for a 1.6B) and actually have it stream at 3-6 Tokens Per Second. Here's a code example on how you can interact with your endpoint:

```
!pip install openai requests
from openai import OpenAI
import datetime
import requests
import time
import random
yourUrl="<The Lambda function URL without /docs>"
promptmessage = "What is the capital of France?"
yourAPIKey="<the key you specified in the config.json>" 
# Configuration Settings - Adjusted for local LLM or compatible endpoint
agentprompt="You are a helpful assistant."
prompt_message=promptmessage
if not yourUrl.endswith("/v1"):
  yourUrl = yourUrl + "/v1"
client=OpenAI(api_key=yourAPIKey,base_url=yourUrl)
starttime=time.time()
stream = client.chat.completions.create(
    model="fastmodel", #fastmodel or strongmodel
    messages= [
            {"content": agentprompt, "role": "system"},
            {"content": prompt_message, "role": "user"},
        ],
    stream=True,
)
firstchunk=True
totalchunks=0
try:
  for chunk in stream:
      #print(chunk)
        if firstchunk:
            timetofirstchunk=time.time()
            firstchunk=False
        if "[/" in str(chunk.choices[0].delta.content):
          break
        print(chunk.choices[0].delta.content or "", end="")
        totalchunks+=1
except Exception as e:
  print(str(e))
endtime=time.time()
tps = totalchunks/(endtime-starttime)
try:
  firstchunktime = timetofirstchunk - starttime
except:
  firstchunktime = "N/A"
print("")
print("Tokens per second:")
print(tps)
print("Time to first chunk (seconds):")
print(firstchunktime)
print("Total Time (seconds): ")
print(endtime-starttime)
print("Total Chunks (tokens): ")
print(totalchunks)

```

This way, you don't need to create custom code to interact with your endpoint, instead using industry standard code. And, because it's compatible with the OpenAI API Spec, anything which leverages it (such as LangChain) will be fully compatible, so long as you point the client to your URL and API key.


### LEGACY: 
Open your browser and navigate to the URL that you were provided by the CDK output and you should be presented with a simple FastAPI frontend allowing you to test out the functionality of your model. Note that it does NOT load the model until you use the `/prompt` endpoint of your API, so if there are problems with your model, you won't know until you get to that point. This is by design so you can see if the Lambda function is working properly before testing the model.

Here's what the different input values do:

`text` -- This is the text you'd like to prompt the model with. Currently, it is pre-prompt loaded with a question/response text, which you can modify if you'd like from the `llama_cpp_docker/main.py` file.

`prioroutput` -- You can provide the previous output of the model into this input if you'd like it to continue where it left off. Remember to keep the same original text prompt.

`tokencount` -- Default at 120, but is the number of tokens the model will generate before returning output. Rule of thumb is that the lower token count, the faster the response, but the less information is contained in the response. You can tweak this to balance accordingly.

`penalty` -- Default at 5.5, this is the repeat penalty. Essentially, this value impacts how much the model will repeat itself in its output.

`seedval` -- Default at 0, this is the seed for your model. If you have it set to zero, it will choose a random seed for each generation. 

___

## Next Steps

This Lambda function is deployed with the largest values Lambda supports (10GB Memory). However, feel free to tweak the models, the function configuration, and the input values you want to use in order to optimize for your Lambda consumption. _Remember, AWS Accounts get 400k GB-s of Lambda functions for free each month_, which opens up the possibilities to have Generative AI capabilities with minimal cost. Check CloudWatch to determine what is going on with your function, and enjoy! Huge thanks to the [llama.cpp](https://github.com/ggerganov/llama.cpp) and the [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) projects, without which this project would not be possible!

# <a name="connect"></a> 🔗 Connect with me

<a href="https://www.baileytec.net" target="_blank"><img alt="Website" src="https://img.shields.io/badge/Personal%20Website-%2312100E.svg?&style=for-the-badge&logoColor=white" /></a>
<a href="https://medium.com/@seanbailey518" target="_blank"><img alt="Medium" src="https://img.shields.io/badge/medium-%2312100E.svg?&style=for-the-badge&logo=medium&logoColor=white" /></a>
<a href="https://www.linkedin.com/in/baileytec/" target="_blank"><img alt="LinkedIn" src="https://img.shields.io/badge/linkedin-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" /></a>
