
import os
import json
from fastapi import FastAPI, Header, HTTPException, Request
from mangum import Mangum
import traceback
import subprocess
import httpx

MODELPATH="/opt/modelfile.bin"
stage = os.environ.get('STAGE', None)
openapi_prefix = f"/{stage}" if stage else "/"
app = FastAPI(title="OpenLLaMa on Lambda API", openapi_prefix=openapi_prefix) # Here is the magic

@app.post("/prompt")
async def prompt(
    text: str,
    request: Request,
    prioroutput: str = "",
    tokencount: int = 50,
    penalty: float = 1.1,
    seedval: int = 0,
):
    from llama_cpp import Llama
    import random
    # Check if the headers are present, you can do something with this if you'd like to send headers to your function, otherwise ignore
    requestdict={}
    for header,value in request.headers.items():
        requestdict[header]=value
    returndict={}    

    try:
        if seedval ==0:
            seedval=random.randint(0,65535)
        llm = Llama(model_path=MODELPATH,seed=seedval)
        output = llm(" Below is an instruction that describes a task, as well as any previous text you have generated. You must continue where you left off if there is text following Previous Output. Write a response that appropriately completes the request. When you are finished, write [[COMPLETE]].\n\n Instruction: "+text+" Previous output: "+prioroutput+" Response:", repeat_penalty=penalty, echo=False, max_tokens=tokencount)
        returndict['returnmsg']=output['choices'][0]['text']

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal server error")

    return returndict


handler=Mangum(app)


