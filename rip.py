import argparse
import os
import yt_dlp
from pydub import AudioSegment

def download_video(youtube_url, output_folder="downloads"):
    """Download video from YouTube and return file path."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',  # Download best audio format
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',  # Save file with video title
        'noplaylist': True  # Ensure only one video is downloaded
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        video_path = ydl.prepare_filename(info_dict)
        return video_path

def extract_audio(video_path, output_format="mp3"):
    """Extract audio from the video and save it in the specified format."""
    audio = AudioSegment.from_file(video_path)
    audio_path = video_path.rsplit(".", 1)[0] + f".{output_format}"
    audio.export(audio_path, format=output_format)
    return audio_path

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Ripper - Downloads and extracts audio from a YouTube link.")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    print("📥 Downloading video...")
    video_path = download_video(args.url)

    print("🎵 Extracting audio...")
    audio_path = extract_audio(video_path)

    print(f"✅ Done! Audio saved as: {audio_path}")

if __name__ == "__main__":
    main()
