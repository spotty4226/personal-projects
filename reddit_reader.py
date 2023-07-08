from moviepy.editor import ImageClip, AudioFileClip
import reddit_reader_functions as rrf
import os

input_directory = "input"
output_directory = "finished_videos"
story = ""

with open("story.txt", "r", encoding="utf-8") as file:
    story = file.read()

lines = story.split("\n")
rrf.clear_directory(input_directory, ".mp4")

index = 1
for line in lines:
    line = line.strip()
    if line != '':
        audio_clip_filename = os.path.join(input_directory, str(index) + ".mp3")
        text_img_filename = os.path.join(input_directory, str(index) + ".png")
        mp4_filename = os.path.join(input_directory, "video_" + str(index) + ".mp4")
        rrf.create_audio(line, audio_clip_filename)
        if index == 1:
            video_title = line
            rrf.create_header_image(line).save(text_img_filename)
        else:
            rrf.create_text_image(line).save(text_img_filename)
        rrf.create_mp4(ImageClip(text_img_filename), AudioFileClip(audio_clip_filename), mp4_filename)
        print(index)
        index += 1

rrf.clear_directory(input_directory, ".png")
rrf.clear_directory(input_directory, ".mp3")

total_duration = rrf.calculate_total_video_duration(input_directory)

background_dir = 'background_videos'
background_video = os.path.join(background_dir, "mc_parkour.webm")
background_output_video = os.path.join(input_directory, "background.mp4")
try:
    rrf.create_random_background_video(background_video, background_output_video, total_duration)
except OSError as e:
    print("Ignoring OSError: ", e)

video_files = [f for f in os.listdir(input_directory) if f.startswith('video_') and f.endswith('.mp4')]
sorted_list = sorted(video_files, key=lambda x: int(x.split("_")[1].split(".")[0]))

rrf.create_video_file(sorted_list, input_directory, output_directory, video_title)