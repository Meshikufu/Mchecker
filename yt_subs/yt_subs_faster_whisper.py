import os
import shutil
import pyperclip
from pytube import YouTube
from moviepy.editor import *
from faster_whisper import WhisperModel
import time
import re
from tqdm import tqdm

def download_audio(url):
    # Download YouTube video
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()

    # Create temp_audio directory if it doesn't exist
    temp_audio_directory = "temp_audio"
    if not os.path.exists(temp_audio_directory):
        os.makedirs(temp_audio_directory)

    # Extract video title and remove non-alphanumeric characters
    video_title = re.sub(r'\W+', '_', yt.title)

    if_mp3_exists = False

    # Check if .mp3 file already exists
    audio_output_path = f"{video_title}.mp3"
    audio_output_full_path = os.path.join(temp_audio_directory, audio_output_path)
    if os.path.exists(audio_output_full_path):
        if_mp3_exists = True
        print("Audio file already exists. Skipping download.")
        return audio_output_full_path
    
    if if_mp3_exists == False:
        # Download audio
        print("Preapering to download...")
        audio_filename = f"{video_title}.mp4"
        audio_path = os.path.join(temp_audio_directory, audio_filename)
        stream.download(output_path=temp_audio_directory, filename=audio_filename)

        # Convert video to audio
        video_clip = AudioFileClip(audio_path)
        audio_output_path = f"{video_title}.mp3"
        audio_output_full_path = os.path.join(temp_audio_directory, audio_output_path)
        video_clip.write_audiofile(audio_output_full_path)

        # Clean up temp video file
        video_clip.close()
        os.remove(audio_path)

        print("Audio downloaded successfully.")

        return audio_output_full_path


def transcribe_audio(audio_path, output_language="en"):
    # Create the WhisperModel with desired settings
    model_size = "large-v2"
    model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # Transcribe audio from the beginning
    segments, info = model.transcribe(audio_path, beam_size=5, language="ja")

    # Check if the detected language is not English, and translate the segments if necessary
    if info.language != output_language:
        print(f"Translating segments to {output_language}...")
        segments, _ = model.transcribe(audio_path, beam_size=5, language=output_language)

    print("Audio transcribed successfully.")

    return segments

from datetime import timedelta
def format_time(seconds):
    # Convert seconds to an integer
    seconds = int(seconds)
    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    # Calculate milliseconds
    milliseconds = int((seconds - int(seconds)) * 1000)
    # Format as HH:MM:SS,mmm with leading zeros
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def generate_srt(segments, video_title):
    # Output SRT file name
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    srt_filename = os.path.join(desktop_path, f"{video_title}.srt")

    # Convert generator to list to get its length
    segments_list = list(segments)
    total_segments = len(segments_list)

    # Create and write subtitles to SRT file
    with open(srt_filename, 'w') as srt_file:
        subtitle_number = 1
        for i, segment in enumerate(segments_list):
            start_time_formatted = format_time(segment.start)
            end_time_formatted = format_time(segment.end)
            srt_file.write(f"{subtitle_number}\n")
            srt_file.write(f"{start_time_formatted} --> {end_time_formatted}\n")
            srt_file.write(f"{segment.text}\n\n")
            subtitle_number += 1
            
            # Update progress bar
            progress = (i + 1) / total_segments * 100
            print(f"Generating SRT: [{'#' * int(progress / 2):50s}] {progress:.2f}%\r", end='', flush=True)
            time.sleep(0.1)  # Introduce a slight delay to ensure the progress bar is visible


def process_youtube_url(url):
    # Check if the URL contains "youtube.com/watch"
    if "youtube.com/watch" not in url:
        print("Wrong URL. Please make sure the URL contains 'youtube.com/watch'.")
        time.sleep(3)
        flag = True
        return
    # Download audio
    audio_path = download_audio(url)

    # Transcribe audio
    segments = tqdm(transcribe_audio(audio_path))

    # Generate SRT file
    generate_srt(segments, os.path.splitext(os.path.basename(audio_path))[0])

    # Move audio file to temp_audio folder
    shutil.move(audio_path, os.path.join("temp_audio", os.path.basename(audio_path)))


process_youtube_url(pyperclip.paste())