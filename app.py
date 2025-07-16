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
def stream_channel(channel_name):
    if channel_name not in channels_to_update:
        return abort(404, description="Канал не найден.")
    
    video_id = channels_to_update[channel_name]
    m3u8_url = get_m3u8_url(video_id)
    if not m3u8_url:
        return abort(503, description="Поток недоступен.")

    # Проксируем как .m3u8
    return Response(
        f"#EXTM3U\n#EXTINF:-1,{channel_name}\n{m3u8_url}\n",
        mimetype="application/vnd.apple.mpegurl"
    )

if __name__ == "__main__":
    app.run(debug=True)
