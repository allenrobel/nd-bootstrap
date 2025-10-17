# nd-python Copilot Instructions

This repository provides Python classes for interacting with Cisco's Nexus Dashboard 4.1 REST API. It's a pure Python implementation.

## Architecture Overview

### Core Library Structure (`lib/nd_python/`)
- **`common/`**: Shared utilities - logging, HTTP sender, credential management, response handling
- **`credentials/`**: High-level API operations (e.g., `default_switch_save.py`)
- **`endpoints/`**: Low-level REST endpoint definitions with Pydantic validation
- **`validators/`**: Pydantic models for request/response validation
- **`parsers/`**: Argument parsers for command-line scripts

### Key Architecture Patterns

**Three-Layer Pattern**: All API operations follow this structure:
1. **High-level class** (`credentials/default_switch_save.py`) - business logic
2. **Endpoint class** (`endpoints/manage.py`) - REST API definition with validation
3. **Validator class** (`validators/`) - Pydantic models for type safety

**Credential Flow**: Scripts use `NdPythonSender` → `CredentialSelector` → environment variables/Ansible Vault → `Sender`

## Essential Development Patterns

### Adding New API Operations
1. Create endpoint in `endpoints/` with verb, path, and Pydantic validation
2. Create high-level wrapper in appropriate module (`credentials/`, `fabric/`, etc.)
3. Add Pydantic validator in `validators/` for config files
4. Create example script in `examples/` with YAML config

### Script Structure Pattern
All example scripts follow this pattern:
```python
# 1. Import nd_python modules
from nd_python.common.nd_python_logger import NdPythonLogger
from nd_python.common.nd_python_sender import NdPythonSender
from nd_python.common.rest_send_v2 import RestSend

# 2. Setup argument parsing with common parsers
parser = argparse.ArgumentParser(parents=[parser_config, parser_nd_ip4, ...])

# 3. Initialize logging and sender
NdPythonLogger()
nd_sender = NdPythonSender()
nd_sender.args = args
nd_sender.commit()  # Performs login

# 4. Configure RestSend with sender and response handler
rest_send = RestSend({})
rest_send.sender = nd_sender.sender
rest_send.response_handler = ResponseHandler()
```

### Endpoint Definition Pattern
```python
class EpCredentialsDefaultSwitchSave:
    def __init__(self):
        self.verb = "POST"
        self.path = f"{base_url}/defaultSwitchCredentials"
        self.validator = EpCredentialsDefaultSwitchSaveValidator
        
    def commit(self):
        # Pydantic validation before use
        self.validator(**self._body)
```

## Environment Setup Requirements

### PYTHONPATH Configuration
Critical: Must include both nd-python:
```bash
export PYTHONPATH=$PYTHONPATH:$HOME/repos/nd-python/lib
```

### Required Environment Variables
Scripts expect these variables (can be overridden via command line):
- `ND_IP4`: Nexus Dashboard IPv4 address
- `ND_USERNAME`/`ND_PASSWORD`: Nexus Dashboard credentials  
- `NXOS_USERNAME`/`NXOS_PASSWORD`: Switch credentials
- `ND_LOGGING_CONFIG`: Optional logging configuration

### Virtual Environment
Use uv for dependency management: `uv sync` after `source .venv/bin/activate`

## Code Style & Quality

- **Line length**: 180 characters (configured in pyproject.toml)
- **Import sorting**: Uses isort with specific multi-line configuration
- **Type hints**: Extensive use of Pydantic for validation
- **Error handling**: Consistent ValueError raising with detailed messages
- **Logging**: Class-based loggers using `logging.getLogger(f"nd_python.{self.class_name}")`

## Common Gotchas

1. **Credential Precedence**: Command line args → environment variables → Ansible Vault
2. **Commit Pattern**: Most classes require calling `.commit()` before use (performs validation/login)
3. **Config Files**: YAML configs in `examples/config/` must match Pydantic validator schemas exactly

## Testing New Features

Run example scripts from `examples/` directory:
```bash
cd examples
./credentials_default_switch_save.py --config config/credentials_default_switch_save.yaml
```

Check `examples/config/` for YAML configuration templates that match your new validators.