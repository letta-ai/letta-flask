# Letta-Flask

`letta_flask` is a [Flask](https://flask.palletsprojects.com/en/stable/) extension that provides a simple way to access [Letta](https://www.letta.com/)'s web apis in a safe and secure way.

## Installation

```bash
 pip install flask requests letta-client letta-flask
```

## Usage

```python
from flask import Flask, send_from_directory

from letta_flask import LettaFlask, LettaFlaskConfig

app = Flask(__name__)

# Initialize

letta_flask = LettaFlask(config=LettaFlaskConfig(
    base_url="http://localhost:8283",
    api_key="OPTIONAL_LETTA_API_KEY"
))

# Attach to app
letta_flask.init_app(app)

# do your routing
@app.route('/')
def index():
    return send_from_directory('index.html')

```
