
import os
import json
from fastapi import FastAPI, Header, HTTPException, Request
from mangum import Mangum
import traceback
import subprocess
import httpx

MODELPATH="/opt/modelfile.bin"
#os.environ.get('MODELPATH') #this will need to be set.
#CHATPATH=os.environ.get('CHATPATH')
#API_PROXY_SECRET=os.environ.get("APIPROXYSECRET")
#API_PROXY_HOST=os.environ.get("APIPROXYHOST")
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(title="OpenLLaMa on Lambda API", openapi_prefix=openapi_prefix) # Here is the magic


#@app.post("/stream")
#async def stream(
#    text: str,
    #x_rapidapi_key: str = Header(None, alias="X-RapidAPI-Key"),
    #x_rapidapi_proxy_secret: str = Header(None, alias="X-RapidAPI-Proxy-Secret"),
#):
    # Check if the headers are present
#    returndict={}
    #if not x_rapidapi_key or not x_rapidapi_proxy_secret:
    #    raise HTTPException(status_code=401, detail="Missing RapidAPI authentication headers")


    # Validate the headers (replace with your actual values)
    #if x_rapidapi_proxy_secret != API_PROXY_SECRET:
    #    raise HTTPException(status_code=403, detail="Invalid RapidAPI authentication")

#    try:
    #    validapi=validate_rapidapi_key(x_rapidapi_key)

    #    if validapi:
        #returndict['returnmsg']=runPrompt(text)
#        return StreamingResponse(runPrompt(text))
    #    else:
    #        raise HTTPException(status_code=403, detail="Invalid API Key")


#    except Exception as e:
#        print(traceback.format_exc())

#        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/prompt")
async def prompt(
    text: str,
    request: Request,
    prioroutput: str = "",
    tokencount: int = 50,
    penalty: float = 1.1,
):
    from llama_cpp import Llama
    import random
# Check if the headers are present
    requestdict={}
    for header,value in request.headers.items():
        requestdict[header]=value
    returndict={}    

    try:
        llm = Llama(model_path=MODELPATH,seed=random.randint(0,65535))
        output = llm(" Below is an instruction that describes a task, as well as any previous text you have generated. You must continue where you left off if there is text following Previous Output. Write a response that appropriately completes the request. When you are finished, write [[COMPLETE]].\n\n Instruction: "+text+" Previous output: "+prioroutput+" Response:", repeat_penalty=penalty, echo=False, max_tokens=tokencount)
        returndict['returnmsg']=output['choices'][0]['text']

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

    return returndict


handler=Mangum(app)


