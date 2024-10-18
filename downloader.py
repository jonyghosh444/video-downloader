import streamlit as st
import yt_dlp
import os

# Define download directory
DOWNLOAD_DIR = "downloads"

# Create the download directory if it doesn't exist
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Streamlit app title
st.title("Video Downloader App")

# Input for the video link
video_url = st.text_input("Enter the video link:")

# Initialize session state variables
if "available_formats" not in st.session_state:
    st.session_state.available_formats = []
if "selected_format_code" not in st.session_state:
    st.session_state.selected_format_code = None

# Button to list available formats
if st.button("List Available Formats"):
    if video_url:
        try:
            # Set options to list formats
            ydl_opts = {
                "noplaylist": True,  # Ignore playlist, download single video only
                "quiet": True,  # Disable verbose output
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract video info
                info_dict = ydl.extract_info(video_url, download=False)
                formats = info_dict.get("formats", None)

                # Display available formats and populate the dropdown
                format_options = []
                for f in formats:
                    # Safely get fields, provide default values if they don't exist
                    format_id = f.get("format_id", "N/A")
                    resolution = f.get(
                        "resolution", f.get("height", "N/A")
                    )  # Fallback to height if resolution is missing
                    format_note = f.get("format_note", "N/A")

                    format_label = f"{format_id} - {resolution} - {format_note}"
                    format_options.append(
                        (format_label, format_id)
                    )  # Tuple (label, format_id)

                st.session_state.available_formats = (
                    format_options  # Store in session state
                )
                st.write(
                    "Formats loaded successfully! Please select a format from the dropdown below."
                )
        except Exception as e:
            st.error(f"Error occurred while fetching formats: {e}")
    else:
        st.warning("Please enter a valid video link.")

# If formats are available, display the dropdown
if st.session_state.available_formats:
    # Get the list of format labels and codes
    format_labels = [f[0] for f in st.session_state.available_formats]
    format_codes = [f[1] for f in st.session_state.available_formats]

    # Store the selected format using Streamlit's selectbox
    selected_format_label = st.selectbox("Select a format:", format_labels)

    # Get the corresponding format code based on the selected label
    if selected_format_label:
        st.session_state.selected_format_code = format_codes[
            format_labels.index(selected_format_label)
        ]

# Button to trigger download
if st.button("Download Video"):
    if video_url and st.session_state.selected_format_code:
        st.write("Starting download...")

        # yt-dlp options with user-specified format
        ydl_opts = {
            "format": st.session_state.selected_format_code,
            "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",  # Save to the 'downloads' folder
        }

        # Function to display progress
        def progress_hook(d):
            if d["status"] == "downloading":
                percentage = d["downloaded_bytes"] / d["total_bytes"] * 100
                st.session_state.progress = percentage
                st.session_state.progress_bar.progress(percentage)

        # Initialize Streamlit progress bar
        st.session_state.progress = 0
        st.session_state.progress_bar = st.progress(0)

        # Show loading spinner during download
        with st.spinner("Downloading... Please wait."):
            try:
                with yt_dlp.YoutubeDL(
                    {**ydl_opts, "progress_hooks": [progress_hook]}
                ) as ydl:
                    ydl.download([video_url])
                st.success(
                    f"Download complete! Video saved in '{DOWNLOAD_DIR}' folder."
                )
            except Exception as e:
                st.error(f"Error occurred during download: {e}")
    else:
        st.warning("Please enter a valid video link and select a format.")
