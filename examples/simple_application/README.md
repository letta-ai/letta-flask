# Simple Letta-Flask Example

## Prerequisites

- [Python 3+](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/) - a dependency manager for Python.
- [Letta Framework](https://github.com/letta-ai/letta) - our open source framework for building stateful LLM applications.

## Setup

1. Run your Letta server. Refer to this [Letta README](https://github.com/letta-ai/letta#setup) for instructions.
2. (Recommended) Set up a python virtual environment

```bash
# on the root directory of this project
python3 -m venv myenv
source myenv/bin/activate
```

3. Install dependencies

```bash
uv pip install -r pyproject.toml
```

## Usage

```bash
uv run app.py
```

Visit [http://localhost:5002](http://localhost:5002) in your browser.
