# Troubleshooting Guide

## Resource Not Found Error

If you're seeing a `resourceNotFoundException` when calling the InvokeAgent operation, check the following:

1. Ensure the `BEDROCK_AGENT_ID` environment variable is set with a valid agent ID:
   ```bash
   export BEDROCK_AGENT_ID='your-agent-id'
   ```

2. Verify that:
   - The Bedrock agent exists in your AWS account
   - The agent is properly deployed and active
   - Your AWS credentials have permission to access the agent
   - You're operating in the correct AWS region (currently hardcoded to us-east-1)

3. Double check the agent ID in the AWS Console:
   - Go to Amazon Bedrock > Agents
   - Find your agent and copy its ID
   - The ID should look something like: "XXXXXXXXXX"

4. If using a custom agent alias:
   ```bash
   export BEDROCK_AGENT_ALIAS_ID='your-alias-id'
   ```
   If not set, it will default to 'latest'

5. Ensure your AWS credentials are properly configured with the necessary permissions:
   - BedrockAgentRuntime:InvokeAgent
   - Additional permissions may be required depending on your agent's knowledge base and actions