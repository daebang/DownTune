
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
    
    return False
