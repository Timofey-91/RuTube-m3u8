from flask import Flask, Response, abort
from rutube import get_m3u8_url

app = Flask(__name__)

# Только эти каналы будут доступны
channels_to_update = {
    "kino_i_zhizn": "09e51eefa939595a4ac67182c6fb3e4e",
    "kinozhelezo": "4965b7b928c4a143d708ab424be01d37",
    "sreda": "5fa486bf465c8735fff9f41b372610cc"
}

@app.route("/")
def index():
    return Response(
        "\n".join([f"/channel/{name}" for name in channels_to_update]),
        mimetype="text/plain"
    )

@app.route("/channel/<channel_name>")
def serve_channel(channel_name):
    m3u8_url = m3u8_cache.get(channel_name)
    if not m3u8_url:
        return "Channel not found or stream unavailable", 404
    return redirect(m3u8_url, code=302)

    )

if __name__ == "__main__":
    app.run(debug=True)
