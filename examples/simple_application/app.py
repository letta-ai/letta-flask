from flask import Flask, send_from_directory, request, Response, stream_with_context
import requests
import json

from letta_flask import LettaFlask, LettaFlaskConfig
from letta_client import MessageCreate, Letta

app = Flask(__name__)

# Initialize
letta_flask = LettaFlask(
    config=LettaFlaskConfig(
        base_url="http://localhost:8283",
    )
)

# Return index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Stream messages
@app.route("/stream", methods=["POST"])
def stream():
    print("Received request with content:", request.json)
    return letta_flask.messages_stream(agent_id="agent-091924fb-4c12-42dd-a9cf-b4005e97e73b")

# Attach to app
letta_flask.init_app(app)

if __name__ == "__main__":
    app.run(port=5002, debug=True)