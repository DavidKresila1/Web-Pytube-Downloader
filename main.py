from flask import Flask, render_template, request, session, send_file, redirect, url_for, jsonify, redirect
from pytube import YouTube, Playlist
from pytube.cli import on_progress
from io import BytesIO

from network import get_ip
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

ip = get_ip()

@app.route("/")
def index():
    return redirect(url_for("youtube"))


@app.route("/youtube", methods=["GET", "POST"])
def youtube():
    if request.method == "POST":
        session["link"] = request.form.get("url")
        try:
            url = YouTube(session["link"], on_progress_callback=on_progress)
            url.check_availability()
        except:
            return render_template("error.html")
        return render_template("downloadYouTube.html", url=url)
    return render_template("getYouTubeData.html")


@app.route("/youtubeDownload", methods=["POST"])
def downloadYouTubeAudio():
    session["link"] = request.form.get("url")
    try:
        url = YouTube(session["link"])
        url.check_availability()
    except:
        return render_template("error.html")
    buffer = BytesIO()
    audioStream = url.streams.filter(only_audio=True).order_by("abr").desc().all()
    if len(audioStream) == 0:
        return render_template("error.html")
    
    audioStream[0].stream_to_buffer(buffer)
    buffer.seek(0)
    
    title = url.title
    fileName = f"{title}.mp3"

    return send_file(buffer, as_attachment=True, download_name=fileName, mimetype="audio/mpeg")





if __name__ == "__main__":
    app.run(host=ip, debug=True)
