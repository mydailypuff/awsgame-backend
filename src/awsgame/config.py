"""Configuration settings for the AWS Game Backend."""
import os

# Bedrock Agent Configuration
BEDROCK_AGENT_ID = os.getenv('BEDROCK_AGENT_ID')
BEDROCK_AGENT_ALIAS_ID = os.getenv('BEDROCK_AGENT_ALIAS_ID', 'latest')

if not BEDROCK_AGENT_ID:
    raise ValueError("BEDROCK_AGENT_ID environment variable must be set")