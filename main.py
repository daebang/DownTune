
import argparse
import yaml
import os
import subprocess
import sys
from src.core import download_playlist


def update_ytdlp():
    """yt-dlp를 최신 버전으로 업데이트합니다."""
    print("[yt-dlp] Checking for updates...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if "Successfully installed" in result.stdout:
            print("[yt-dlp] Updated to latest version!")
        elif "Requirement already satisfied" in result.stdout:
            print("[yt-dlp] Already up to date.")
        else:
            print("[yt-dlp] Update check completed.")
    except Exception as e:
        print(f"[yt-dlp] Warning: Could not update yt-dlp: {e}")
        print("[yt-dlp] Continuing with current version...")

def load_library(library_path):
    if not os.path.exists(library_path):
        print(f"[Error] Library file not found: {library_path}")
        return None
    
    with open(library_path, 'r', encoding='utf-8') as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"[Error] Failed to parse YAML: {e}")
            return None

def main():
    # yt-dlp 자동 업데이트 (YouTube 차단 대응)
    update_ytdlp()
    print()

    parser = argparse.ArgumentParser(description="DownTune: High-quality music downloader.")
    
    # Mode selection
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("url", nargs="?", help="YouTube Playlist or Video URL")
    group.add_argument("--batch", help="Path to YAML library file for batch processing")
    
    # Metadata args (only for single URL mode)
    parser.add_argument("--artist", help="Artist Name (for tagging)")
    parser.add_argument("--album", help="Album Name (for tagging)")

    # Authentication
    parser.add_argument(
        "--browser",
        choices=['chrome', 'edge', 'firefox', 'opera', 'brave', 'chromium', 'safari', 'vivaldi'],
        help="Browser to extract cookies from (for private/age-restricted videos)"
    )
    
    args = parser.parse_args()
    
    base_dir = os.path.join(os.getcwd(), "Downloads")

    if args.batch:
        print(f"Loading library: {args.batch}")
        library = load_library(args.batch)
        if not library:
            return

        for artist, albums in library.items():
            print(f"\nProcessing Artist: {artist}")
            for item in albums:
                album_name = item.get('album')
                url = item.get('url')
                
                if not album_name or not url:
                    print(f"  [Skip] Invalid entry: {item}")
                    continue
                
                # Structure: Downloads/Artist/Album
                output_dir = os.path.join(base_dir, artist, album_name)
                download_playlist(url, output_dir, artist=artist, album=album_name, browser=args.browser)

    elif args.url:
        # Single mode
        artist = args.artist or "Unknown Artist"
        album = args.album or "Unknown Album"
        
        # Structure: Downloads/Artist/Album
        output_dir = os.path.join(base_dir, artist, album)
        download_playlist(args.url, output_dir, artist=args.artist, album=args.album, browser=args.browser)

if __name__ == "__main__":
    main()
