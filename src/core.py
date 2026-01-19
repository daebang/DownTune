
import os
import yt_dlp
from .utils import setup_ffmpeg
from .tagger import tag_files

def download_playlist(url, output_dir, artist=None, album=None):
    """
    Download a playlist or video using yt-dlp.
    """
    
    # Ensure FFmpeg is available
    if not setup_ffmpeg():
        print("[Warning] FFmpeg not found. Conversions may fail.")
        
    print(f"\n[Downloader] Starting download...")
    print(f"  > URL: {url}")
    print(f"  > To: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # yt-dlp configuration
    ydl_opts = {
        'format': 'bestaudio/best',
        # Naming: PlaylistIndex - Title.ext
        'outtmpl': os.path.join(output_dir, '%(playlist_index)s - %(title)s.%(ext)s'),
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
            {
                'key': 'EmbedThumbnail',
            },
            {
                'key': 'FFmpegMetadata',
            }
        ],
        'writethumbnail': True,
        'ignoreerrors': True,
        'quiet': False,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Automatic tagging if Artist/Album provided
    if artist and album:
        tag_files(output_dir, artist, album)
