from typing import TypedDict, Optional
from flask import Flask, request, Response, stream_with_context
import requests
from letta_client import Letta, MessageCreate
import json
import re


class LettaFlaskConfig(TypedDict):
    base_url: str
    api_key: Optional[str]


class LettaFlask:
    # define base_url and api_key
    base_url: str
    api_key: Optional[str] = None

    def __init__(
        self, app: Optional[Flask] = None, config: LettaFlaskConfig = None
    ) -> None:
        self.base_url = config["base_url"]
        self.api_key = config.get("api_key")

        if app is not None:
            self.init_app(app)


    def init_app(self, app: Flask) -> None:
        # proxy routes to base_url
        @app.route("/v1/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
        def proxy_v1(path: str) -> Response:
            # if path is messages/stream, create a stream
            if path.endswith("messages/stream"):
                # /v1/agents/{agent_id}/messages/stream
                agent_id = re.search(r"agents/(.*?)/messages/stream", path).group(1)

                return self.messages_stream(agent_id=agent_id)

            # Build the target URL
            target_url = f"{self.base_url}/v1/{path}"

            # Forward the request with all its data
            headers = {key: value for key, value in request.headers if key != "Host"}

            # Add API key to headers if provided
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            # Send the request to the target URL
            resp = requests.request(
                method=request.method,
                url=target_url,
                headers=headers,
                params=request.args,
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False,
            )

            # Create a Flask response with the same content
            response = Response(
                resp.content, resp.status_code, headers=dict(resp.headers)
            )

            return response


    def messages_stream(self, agent_id: str) -> Response:
        data = request.get_data()

        letta = Letta(base_url=self.base_url, token=self.api_key)
        parsed = json.loads(data)

        def streamer():
            try:
                response = letta.agents.messages.create_stream(
                    agent_id=agent_id,
                    messages=[
                        MessageCreate(
                            role="user",
                            content=parsed.get("content", "content")
                        )
                    ]
                )
                
                for chunk in response:  
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
            stream_with_context(streamer()),
            mimetype='text/event-stream',
            headers={
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive'
            }
        )
