
import os
import re
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError


def extract_track_number(filename: str) -> str | None:
    """
    Extract track number from filename.
    Matches patterns like "01 - Song.mp3", "1 - Song.mp3", "01. Song.mp3"
    """
    match = re.match(r'^(\d+)\s*[-.]?\s*', filename)
    if match:
        return match.group(1)
    return None


def tag_files(directory, artist, album):
    """
    Iterate through MP3 files in a directory and update their Artist/Album/Track tags.
    """
    mp3_files = sorted([f for f in os.listdir(directory) if f.endswith('.mp3')])
    total_tracks = len(mp3_files)

    print(f"[Tagger] Updating metadata: Artist='{artist}', Album='{album}'")
    
    count = 0
    for filename in mp3_files:
        filepath = os.path.join(directory, filename)

        try:
            try:
                audio = EasyID3(filepath)
            except ID3NoHeaderError:
                audio = EasyID3()
                audio.save(filepath)

            audio['artist'] = artist
            audio['album'] = album

            # Extract and set track number from filename
            track_num = extract_track_number(filename)
            if track_num:
                audio['tracknumber'] = str(int(track_num))

            audio.save()
            count += 1

        except Exception as e:
            print(f"  [Error] Failed to tag {filename}: {e}")
            
    print(f"[Tagger] Processed {count} files.")
