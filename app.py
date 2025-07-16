from flask import Flask, redirect
from rutube import get_stream_link

app = Flask(__name__)

channels_to_update = {
    "kino_i_zhizn": "09e51eefa939595a4ac67182c6fb3e4e",
    "kinozhelezo": "4965b7b928c4a143d708ab424be01d37",
    "sreda": "5fa486bf465c8735fff9f41b372610cc"
}

@app.route('/stream/<channel>')
def stream(channel):
    video_id = channels_to_update.get(channel)
    if not video_id:
        return "Channel not found", 404
    m3u8_link = get_stream_link(video_id)
    return redirect(m3u8_link, code=302)

@app.route('/')
def index():
    return "<h3>Используй ссылки типа /stream/kino_i_zhizn</h3>"
