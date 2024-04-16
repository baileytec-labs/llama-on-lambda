from aws_cdk import (
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_lambda as aws_lambda,
    aws_iam as iam,
    aws_logs as logs,
    aws_certificatemanager as acm,
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput
)
import random
from aws_cdk import aws_ssm as ssm

from constructs import Construct

class LambdaFunctionStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        titlemessage = "Quantized LLM Running on AWS Lambda"
        apikey = self.node.try_get_context("apikey") or "insert_api_key_here"
        chatformat = self.node.try_get_context("chatformat") or "mistral-instruct"
        modelfile = self.node.try_get_context("modelfile") or "https://huggingface.co/stabilityai/stablelm-2-zephyr-1_6b/resolve/main/stablelm-2-zephyr-1_6b-Q5_K_M.gguf"
        #--------------------------------------llama_lambda_server Lambda Function---------------------------------------------
        llama_lambda_server_lambda_function_name="llama_lambda_server_lambda_function"

        # IAM Role for the Lambda function
        llama_lambda_server_lambda_role = iam.Role(
            self,
            id="llama_lambda_server_lambda_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            # Adding an inline policy for DynamoDB access
        )

        # Attach the basic execution role
        llama_lambda_server_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        )

        llama_lambda_server_lambda_function=aws_lambda.DockerImageFunction(self,llama_lambda_server_lambda_function_name,
        architecture=aws_lambda.Architecture.ARM_64,
        timeout=Duration.seconds(300), #I'm seeing 150s at times needed to process responses, so I'll give double the time just in case.
        log_retention=logs.RetentionDays.ONE_WEEK,
        environment={
        "STAGE":"",
        "TITLEMESSAGE":titlemessage,
        },
        memory_size=3500, #This is good for 1.6B models. Double this for a 3B model, max it out for a 7B model.
        retry_attempts=0,
        role=llama_lambda_server_lambda_role,
        code=aws_lambda.DockerImageCode.from_image_asset("./llama-cpp-server-container",
                                                         build_args={
            "CHAT_FORMAT": chatformat,
            "MODEL_FILE": modelfile,
            "APIKEY":apikey,
        }),
        )

        
        llama_lambda_server_lambda_function_url=llama_lambda_server_lambda_function.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE,
            invoke_mode=aws_lambda.InvokeMode.RESPONSE_STREAM,
            cors=aws_lambda.FunctionUrlCorsOptions(
         #Allow this to be called from websites on https://example.com.
         #Can also be ['*'] to allow all domain.
        allowed_origins=["*"]
        )
        )
        CfnOutput(self, "UnchainedLambdaFunctionUrl",
        value=llama_lambda_server_lambda_function_url.url+"docs"
        )

