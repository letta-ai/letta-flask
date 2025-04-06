from flask import Flask, send_from_directory, request

from letta_flask import LettaFlask, LettaFlaskConfig

app = Flask(__name__)

# Initialize
letta_flask = LettaFlask(
    config=LettaFlaskConfig(base_url="https://api.letta.com", api_key="<your-token>")
)


# Return index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# Stream messages
@app.route("/stream", methods=["POST"])
def stream():
    print("Received request with content:", request.json)
    return letta_flask.messages_stream(
        agent_id="agent-091924fb-4c12-42dd-a9cf-b4005e97e73b"
    )


# Attach to app
letta_flask.init_app(app)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
