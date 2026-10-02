import os

from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.environ["AWS_REGION"]
BEDROCK_MODEL_ID = os.environ["BEDROCK_MODEL_ID"]
GUARDRAIL_ID = os.environ["GUARDRAIL_ID"]
AGENTCORE_RUNTIME_ARN = os.environ["AGENTCORE_RUNTIME_ARN"]
BEDROCK_MAX_TOKENS = int(os.environ["BEDROCK_MAX_TOKENS"])
GUARDRAIL_VERSION = os.environ["BEDROCK_GUARDRAIL_VERSION"]