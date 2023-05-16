from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as aws_lambda,
    aws_logs as logs,
    CfnOutput,

)


class LlamaLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #--------------------------------------Open_llama Lambda Function---------------------------------------------
        open_llama_lambda_function_name="open_llama_lambda_function"

        open_llama_lambda_role=iam.Role(
            self,
            id="open_llama_lambda_role",
            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com")
        )

        open_llama_lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        open_llama_lambda_function=aws_lambda.DockerImageFunction(self,open_llama_lambda_function_name,
        
        timeout=Duration.seconds(900),
        log_retention=logs.RetentionDays.ONE_WEEK,
        environment={

        "STAGE":"",
        },
        memory_size=10240,
        retry_attempts=0,
        role=open_llama_lambda_role,
        code=aws_lambda.DockerImageCode.from_image_asset("./llama_cpp_docker"),
        )

        open_llama_lambda_function_url=open_llama_lambda_function.add_function_url(
            auth_type=aws_lambda.FunctionUrlAuthType.NONE,
            cors=aws_lambda.FunctionUrlCorsOptions(
         #Allow this to be called from websites on https://example.com.
         #Can also be ['*'] to allow all domain.
        allowed_origins=["*"]
        )
        )
        CfnOutput(self, "OpenLlamaUrl",
        value=open_llama_lambda_function_url.url + "/docs"
        )

        
