# AWS Game Backend

A Python package for integrating AWS Bedrock Agent with game backends.

## Installation

```bash
# Install for development
pip install -e ".[dev]"

# Install for production
pip install .
```

## Package Structure

```
awsgame-backend/
├── src/awsgame/         # Main package
│   ├── handlers/        # Lambda handler implementations
│   ├── clients/         # AWS service clients
│   └── exceptions/      # Custom exceptions
├── tests/               # Test suite
│   └── unit/           # Unit tests
└── docs/               # Documentation
```

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

3. Run tests:
```bash
pytest
```

4. Check code style:
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/
mypy src/ tests/
```

## Usage Example

```python
from awsgame.clients.bedrock import BedrockAgentClient
from awsgame.exceptions.custom_exceptions import AgentError

try:
    client = BedrockAgentClient()
    response = client.communicate("Hello agent!", "session-123")
    print(response['completion'])
except AgentError as e:
    print(f"Error: {e}")
```

## Configuration

Before using the package, make sure to replace the following placeholders in the `src/awsgame/clients/bedrock.py` file:
- `YOUR_AGENT_ID`: Your Bedrock Agent ID
- `YOUR_ALIAS_ID`: Your Bedrock Agent Alias ID

The AWS region defaults to us-east-1 if not specified.

## License

MIT License