import argparse
import os
import yt_dlp
from pydub import AudioSegment

# Always find script's own directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(SCRIPT_DIR, "downloads")

def download_video(youtube_url, output_folder=DOWNLOAD_FOLDER):
    """download audio from YouTube and return file path"""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        video_path = ydl.prepare_filename(info_dict)
        return video_path

def extract_audio(video_path, output_format="mp3"):
    """extract audio and save it in specified format"""
    audio = AudioSegment.from_file(video_path)
    audio_path = os.path.splitext(video_path)[0] + f".{output_format}"
    audio.export(audio_path, format=output_format)

    return audio_path

def main():
    parser = argparse.ArgumentParser(description="YouTube Audio Ripper - Downloads and extracts audio from a YouTube link.")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()

    print("📥 Downloading audio...")
    video_path = download_video(args.url)

    print("🎵 Extracting audio...")
    try:
        audio_path = extract_audio(video_path)
        print(f"✅ Audio saved as: {audio_path}")

        # Clean up original file
        if os.path.exists(audio_path):
            os.remove(video_path)
            print(f"🧹 Removed original file: {video_path}")

    except Exception as e:
        print(f"❌ Error extracting audio: {e}")

if __name__ == "__main__":
    main()
