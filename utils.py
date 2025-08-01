import os
import whisper
import subprocess
from pytube import YouTube
from googletrans import Translator

translator = Translator()
model = whisper.load_model("base")

def download_youtube_audio(video_url, filename="audio.mp4"):
    yt = YouTube(video_url)
    stream = yt.streams.filter(only_audio=True).first()
    stream.download(filename=filename)
    return filename

def download_youtube_video(video_url, filename="video.mp4"):
    yt = YouTube(video_url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
    stream.download(filename=filename)
    return filename

def transcribe_audio_to_srt(audio_file, srt_file="subtitles.srt"):
    result = model.transcribe(audio_file, verbose=False, task="transcribe")
    segments = result["segments"]
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            text = translator.translate(seg["text"], dest='ar').text
            f.write(f"{i+1}\n{start} --> {end}\n{text.strip()}\n\n")
    return srt_file

def format_timestamp(seconds):
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"

def merge_video_with_subtitles(video_file, srt_file, output_file="output.mp4"):
    cmd = [
        "ffmpeg",
        "-i", video_file,
        "-vf", f"subtitles={srt_file}",
        "-c:a", "copy",
        output_file
    ]
    subprocess.run(cmd, check=True)
    return output_file