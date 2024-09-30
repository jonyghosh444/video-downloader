import yt_dlp
from config import FILE_PATH

# Course page URL
course_page_url = FILE_PATH

# yt-dlp options
ydl_opts = {
    'format': 'best',  # Choose the best quality available
    'outtmpl': 'downloads/%(title)s.%(ext)s',  # Save to the 'downloads' folder  # Path to your cookies file
}

# Download the videos
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([course_page_url])
