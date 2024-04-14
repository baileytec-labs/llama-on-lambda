#!/usr/bin/env python3

import aws_cdk as cdk

from llama_lambda.llama_lambda_stack import LlamaLambdaStack
from llama_lambda.lambda_function_stack import LambdaFunctionStack


app = cdk.App()
LambdaFunctionStack(app,"llama-Lambda-function-stack")

app.synth()
