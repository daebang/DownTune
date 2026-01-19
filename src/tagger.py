
import os
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

def tag_files(directory, artist, album):
    """
    Iterate through MP3 files in a directory and update their Artist/Album tags.
    """
    print(f"[Tagger] Updating metadata: Artist='{artist}', Album='{album}'")
    
    count = 0
    for filename in os.listdir(directory):
        if not filename.endswith(".mp3"):
            continue
            
        filepath = os.path.join(directory, filename)
        
        try:
            try:
                audio = EasyID3(filepath)
            except ID3NoHeaderError:
                audio = EasyID3()
                audio.save(filepath)

            audio['artist'] = artist
            audio['album'] = album
            audio.save()
            count += 1
            
        except Exception as e:
            print(f"  [Error] Failed to tag {filename}: {e}")
            
    print(f"[Tagger] Processed {count} files.")
