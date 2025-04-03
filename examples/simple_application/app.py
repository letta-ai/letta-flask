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

# return index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/stream", methods=["POST"])
def stream():
    print("Received request with content:", request.json)
    
    # Create Letta client
    client = Letta(base_url="http://localhost:8283")
    
    def generate():
        try:
            # Get streaming response from Letta client
            stream = client.agents.messages.create_stream(
                agent_id="agent-091924fb-4c12-42dd-a9cf-b4005e97e73b",
                messages=[
                    MessageCreate(
                        role="user",
                        content=request.json.get("content", "content")
                    )
                ]
            )
            
            # Iterate through the stream
            for chunk in stream:
                if chunk:
                    print("Raw chunk:", chunk)
                    if (chunk.message_type == "reasoning_message"):
                        data = {
                            "type": chunk.message_type,
                            "reasoning": chunk.reasoning
                        }
                    elif (chunk.message_type == "assistant_message"):
                        data = {
                            "type": chunk.message_type,
                            "content": chunk.content
                        }
                    yield f"data: {json.dumps(data)}\n\n".encode("utf-8")
        except Exception as e:
            print("Error in stream:", e)
            yield f"data: {json.dumps({'error': str(e)})}\n\n".encode('utf-8')

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive'
        }
    )

# Attach to app
letta_flask.init_app(app)

if __name__ == "__main__":
    app.run(port=5002, debug=True)