# AWS Bedrock Agent Async Streaming Issue

## Current Status
We are encountering issues with async streaming responses from AWS Bedrock agents. Despite trying multiple approaches including:
- Direct async iteration over the response
- Using response.get_stream()
- Different chunk parsing approaches

The error "Use async-for instead" persists.

## Next Steps
1. Open AWS support ticket for guidance on correct async streaming patterns with Bedrock agents
2. Consider implementing a synchronous fallback client
3. Research official AWS examples specific to Bedrock agent async streaming

## Documentation References
- Review [AWS Bedrock API Documentation](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModel.html)
- Check [aioboto3 documentation](https://github.com/terrycain/aioboto3)
- Look for AWS sample code repositories