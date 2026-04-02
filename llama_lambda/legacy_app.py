#!/usr/bin/env python3

import aws_cdk as cdk

from llama_lambda.llama_lambda_stack import LlamaLambdaStack


app = cdk.App()
LlamaLambdaStack(app,"llama-Lambda-function-stack")

app.synth()
