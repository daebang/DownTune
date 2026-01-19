
import os
import sys
import shutil

def setup_ffmpeg():
    """
    Ensure ffmpeg is in the PATH.
    Priority:
    1. Global PATH
    2. Local 'bin' folder in the project directory.
    """
    
    # Check if ffmpeg is already available globally
    if shutil.which("ffmpeg"):
        return True

    # If not, check local bin directory
    # Assuming bin/ is next to the src/ folder (parent of this file)
    # Project structure:
    # DownTune/
    #   bin/
    #   src/
    #     utils.py
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    local_bin = os.path.join(project_root, "bin")

    if os.path.exists(os.path.join(local_bin, "ffmpeg.exe")):
        # Add to PATH for the current process
        os.environ["PATH"] += os.pathsep + local_bin
        print(f"[Info] Using bundled FFmpeg from: {local_bin}")
        return True
    
    # Attempt to auto-download if missing
    print("[Info] FFmpeg not found locally or globally. Attempting download...")
    try:
        download_ffmpeg(local_bin)
        os.environ["PATH"] += os.pathsep + local_bin
        return True
    except Exception as e:
        print(f"[Error] Failed to download FFmpeg: {e}")
        return False

def download_ffmpeg(bin_dir):
    """
    Download FFmpeg binaries from gyan.dev and extract them.
    """
    import urllib.request
    import zipfile
    
    os.makedirs(bin_dir, exist_ok=True)
    
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(bin_dir, "ffmpeg.zip")
    
    print(f"  Downloading from {url}...")
    urllib.request.urlretrieve(url, zip_path)
    
    print("  Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract specific files
        for file in zip_ref.namelist():
            if file.endswith("bin/ffmpeg.exe"):
                 zip_ref.extract(file, bin_dir)
                 # Move up
                 source = os.path.join(bin_dir, file)
                 target = os.path.join(bin_dir, "ffmpeg.exe")
                 shutil.move(source, target)
                 
            elif file.endswith("bin/ffprobe.exe"):
                 zip_ref.extract(file, bin_dir)
                 source = os.path.join(bin_dir, file)
                 target = os.path.join(bin_dir, "ffprobe.exe")
                 shutil.move(source, target)

    # Cleanup
    os.remove(zip_path)
    # Remove extracted subdirectory if empty or needed
    # (Simplified cleanup, main files are moved)
    print("  FFmpeg installed successfully.")
