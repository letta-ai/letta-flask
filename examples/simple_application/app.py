from flask import Flask, send_from_directory

from letta_flask import LettaFlask, LettaFlaskConfig

app = Flask(__name__)

# Initialize

letta_flask = LettaFlask(
    config=LettaFlaskConfig(base_url="https://api.letta.com", api_key="<your-token>")
)


# return index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")


# Attach to app
letta_flask.init_app(app)

if __name__ == "__main__":
    app.run(port=5002)
