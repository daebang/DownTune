
import os
import re
import yt_dlp
from .utils import setup_ffmpeg
from .tagger import tag_files


def add_track_numbers(directory: str) -> None:
    """
    Check MP3 files in directory and add track numbers if missing.
    Files already starting with numbers (e.g., "01 - Song.mp3") are skipped.
    Files starting with "NA - " are treated as missing track numbers.
    """
    mp3_files = sorted([f for f in os.listdir(directory) if f.endswith('.mp3')])

    if not mp3_files:
        return

    # Pattern to detect if filename starts with a track number
    # Matches: "01 - ", "1 - ", "01. ", "1.", etc.
    track_number_pattern = re.compile(r'^(\d+)\s*[-.]?\s*')
    # Pattern to detect "NA - " prefix (yt-dlp uses this when playlist_index is unavailable)
    na_pattern = re.compile(r'^NA\s*[-.]?\s*', re.IGNORECASE)

    needs_numbering = False
    for filename in mp3_files:
        # Check if file needs numbering (no number or starts with NA)
        if na_pattern.match(filename) or not track_number_pattern.match(filename):
            needs_numbering = True
            break

    if not needs_numbering:
        print("[Numbering] All files already have track numbers.")
        return

    print("[Numbering] Adding track numbers to files...")

    for idx, filename in enumerate(mp3_files, start=1):
        old_path = os.path.join(directory, filename)

        # Remove "NA - " prefix if present
        clean_name = na_pattern.sub('', filename)
        # Remove existing number prefix if present (to avoid double numbering)
        clean_name = track_number_pattern.sub('', clean_name)

        # Format: "01 - Title.mp3" (zero-padded based on total count)
        padding = len(str(len(mp3_files)))
        new_filename = f"{idx:0{padding}d} - {clean_name}"
        new_path = os.path.join(directory, new_filename)

        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"  {filename} -> {new_filename}")

    print(f"[Numbering] Processed {len(mp3_files)} files.")

def download_playlist(url, output_dir, artist=None, album=None, browser=None):
    """
    Download a playlist or video using yt-dlp.

    Args:
        url: YouTube URL to download
        output_dir: Directory to save files
        artist: Artist name for tagging
        album: Album name for tagging
        browser: Browser name to extract cookies from (chrome, edge, firefox, etc.)
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

    # Add browser cookies for authentication if specified
    if browser:
        print(f"  > Using cookies from: {browser}")
        ydl_opts['cookiesfrombrowser'] = (browser,)
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Add track numbers if missing
    add_track_numbers(output_dir)

    # Automatic tagging if Artist/Album provided
    if artist and album:
        tag_files(output_dir, artist, album)
