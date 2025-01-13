# How to Verify Your Configuration

To ensure your AWS Bedrock Agent setup is correct, follow these steps:

1. **Check Environment Variables**
   ```bash
   echo $BEDROCK_AGENT_ID
   echo $BEDROCK_AGENT_ALIAS_ID
   ```
   If they're not set, or set incorrectly, refer to SETUP.md.

2. **Verify AWS Region**
   ```bash
   echo $AWS_DEFAULT_REGION
   ```
   Make sure it matches the region where your Bedrock agent is deployed (default: us-east-1).

3. **Check AWS Credentials**
   ```bash
   aws sts get-caller-identity
   ```
   This should show your AWS account information. If it fails, your AWS credentials are not properly configured.

4. **List Bedrock Agents**
   ```bash
   aws bedrock-agent list-agents --region us-east-1
   ```
   Your agent ID should appear in this list. If not, either:
   - The agent doesn't exist in this account/region
   - Your credentials don't have sufficient permissions
   - You're looking in the wrong region