# DownTune

A simple, robust CLI tool to download high-quality music albums from YouTube.

## Features
- **Zero Config**: Comes with bundled FFmpeg, so no external installation is needed.
- **High Quality**: Downloads best audio and converts to 320kbps MP3.
- **Smart Tagging**: Automatically tags files with Artist and Album metadata.
- **Batch Mode**: Download entire collections via a YAML library file.

## Installation

1.  Clone the repository.
2.  Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Single Album (CLI)
Download a playlist and tag it:
```bash
python main.py "THE_PLAYLIST_URL" --artist "Artist Name" --album "Album Name"
```

### Batch Mode
Create a `library.yaml` file (see `library.yaml.example`) and run:
```bash
python main.py --batch library.yaml
```

### Library File Format
```yaml
Artist Name:
  - album: "Album One"
    url: "https://youtube.com/..."
  - album: "Album Two"
    url: "https://youtube.com/..."
```
