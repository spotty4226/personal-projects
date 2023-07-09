# Introduction

The purpose of the Reddit Reader script is to automatically generate a full length video that can be posted to TikTok from a simple text file. If you would like to check out some of the videos that I have made using the script, please view [my TikTok page](https://www.tiktok.com/@reddits_juiciest). The script only takes a few minutes to run, and saves me between 3-6 hours of editing per video uploaded. The script took me about 3-4 hours to write.

<hr>

# How To Use

If you would like to use the script, please follow these steps:
1. Download the code from GitHub.
2. Install the necessary packages found in the <i>requirements.txt</i> file. You can use the command found below.
```
pip install pillow gtts moviepy
``` 
3. Copy the content from a Reddit post (including the title) and paste it into the <i>story.txt</i> file.
4. Run the <b>reddit_reader.py</b> script.
5. Once the script is done running, view the finished video in the <i>finished_videos</i> folder.

<hr>

# Logic

The script's logic is as follows:
1. Clears out any files found in the <i>input</i> folder from the previous run.
2. Reads the story from the <i>story.txt</i> file.
3. Generates an image for every non-empty new line, with the first image being a "title" image (bold and larger text).
4. Using the gTTS library, it generates the necessary audio clip for every non-empty new line.
5. Merges the correlating text and audio files together and saves them as .mp4 files.
6. Sums the duration of all the mp4 files in the <i>input</i> folder and randomly grabs a matching-duration chunk from the video found in the <i>background_videos</i> folder, muting the video before saving it as <i>background.mp4</i> in the <i>input</i> folder.
7. Grabs a list of video file names from the <i>input</i> folder and reorders them to ensure they are in order.
8. Overlays the image/audio videos over the background video, then reshapes it to a 9:16 aspect ratio to match TikTok's requirements.
9. Saves the finished video to the <i>finished_videos</i> folder, naming it the same as the title found in the <i>story.txt</i> file.

Once the script is done running, the video is available to upload to TikTok, or any other social media platform you prefer!

<hr>

# Disclaimer

This script is a simplified version of the script that I personally use. This is to avoid having to install FFMpeg for speeding up the TTS audio and lengthy downloads due to the large video files that can be found in the <i>background_videos</i> folder.<p>

Other features include:
<ul>
    <li>Randomly selecting a background video from over a dozen videos.
    <li>Creating multiple stories in a row from a folder filled with text files.
    <li>Creating landscape AND portrait videos (for both YouTube and TikTok).
    <li>Speeding up the text.
</ul>