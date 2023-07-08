from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips, vfx
import random
import os

def create_text_image(text):
    max_line_length = 55
    font_color = (255, 255, 255)
    font_size = 24
    font_path = "fonts/NotoSans-SemiBold.ttf"
    font = ImageFont.truetype(font_path, font_size)
    line_height = font.getsize("hg")[1]
    words = text.split()
    lines = []
    line = []
    line_length = 0
    for word in words:
        if line_length + len(word) + 1 > max_line_length:
            lines.append(" ".join(line))
            line = []
            line_length = 0
        line.append(word)
        line_length += len(word) + 1
    if line:
        lines.append(" ".join(line))
    num_lines = len(lines)
    max_text_width = max(font.getsize(line)[0] for line in lines)
    image_width = max_text_width + 20
    image_height = num_lines * line_height + 20

    image = Image.new("RGB", (image_width, image_height), (0, 0, 0))

    draw = ImageDraw.Draw(image)
    y_position = (image_height - num_lines * line_height) // 2
    for line in lines:
        x_position = 10
        draw.text((x_position, y_position), line, font=font, fill=font_color)
        y_position += line_height

    return image


def create_header_image(text):
    max_line_length = 35
    font_color = (255, 255, 255)
    font_size = 36
    font_path = "fonts/NotoSans-ExtraBold.ttf"
    font = ImageFont.truetype(font_path, font_size)
    line_height = font.getsize("hg")[1]
    words = text.split()
    lines = []
    line = []
    line_length = 0
    for word in words:
        if line_length + len(word) + 1 > max_line_length:
            lines.append(" ".join(line))
            line = []
            line_length = 0
        line.append(word)
        line_length += len(word) + 1
    if line:
        lines.append(" ".join(line))
    num_lines = len(lines)
    max_text_width = max(font.getsize(line)[0] for line in lines)
    image_width = max_text_width + 20
    image_height = num_lines * line_height + 20

    image = Image.new("RGB", (image_width, image_height), (0, 0, 0))

    draw = ImageDraw.Draw(image)
    y_position = (image_height - num_lines * line_height) // 2
    for line in lines:
        x_position = 10
        draw.text((x_position, y_position), line, font=font, fill=font_color)
        y_position += line_height

    return image


def create_audio(text, filename):
    tts = gTTS(text=text, lang='en', slow=True)
    tts.save(filename)

def create_mp4(image, audio, mp4_filename):
    duration = audio.duration
    image = image.set_duration(duration)
    width = image.size[0]
    height = image.size[1]
    width = width - (width % 2)
    height = height - (height % 2)
    image = image.resize((width, height))
    video = image.set_audio(audio)
    fps = 30
    video = video.set_fps(fps)
    audio = audio.set_fps(fps)
    video.write_videofile(mp4_filename, codec="h264", audio_codec="mp3", audio=True, ffmpeg_params=["-pix_fmt", "yuv420p"])
    video.close()


def clear_directory(directory, file_extension):
    for filename in os.listdir(directory):
        if filename.endswith(file_extension):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")


def calculate_total_video_duration(directory):
    total_duration = 0.0
    for filename in os.listdir(directory):
        if filename.startswith('video_') and filename.endswith('.mp4'):
            video = VideoFileClip(os.path.join(directory, filename))
            total_duration += video.duration
    return total_duration


def create_random_background_video(input_video, background_video, duration):
    video = VideoFileClip(input_video)
    duration = min(duration, video.duration)
    max_start_time = video.duration - duration
    start_time = random.uniform(0, max_start_time)
    subclip = video.resize((1280, 720)).subclip(start_time, start_time + duration)
    subclip.write_videofile(background_video, codec="h264", audio_codec="mp3", audio=True, ffmpeg_params=["-pix_fmt", "yuv420p"])
    video.close()


def create_video_file(video_files, input_directory, output_directory, video_title):
    background_video_path = os.path.join(input_directory, 'background.mp4')
    background_clip_full = VideoFileClip(background_video_path).volumex(0)
    aspect_ratio = 9 / 16
    new_width = int(background_clip_full.h * aspect_ratio)
    new_width = new_width if new_width % 2 == 0 else new_width - 1
    portrait_video_clips = []
    cumulative_duration = 0
    for video_file in video_files:
        video_path = os.path.join(input_directory, video_file)

        portrait_video_file_width = int(new_width * 0.9)
        portrait_video_clip = VideoFileClip(video_path).resize(width=portrait_video_file_width).set_position('center')
        portrait_background_clip_full = background_clip_full.fx(vfx.crop, x_center=background_clip_full.w/2, y_center=background_clip_full.h/2, width=new_width, height=background_clip_full.h)
        portrait_background_clip = portrait_background_clip_full.subclip(cumulative_duration, cumulative_duration + portrait_video_clip.duration)
        portrait_video_clips.append(CompositeVideoClip([portrait_background_clip, portrait_video_clip]))
        cumulative_duration += portrait_video_clip.duration

    final_portrait_clip = concatenate_videoclips(portrait_video_clips)
    final_portrait_clip.write_videofile(os.path.join(output_directory, video_title + '.mp4'), codec="h264", audio_codec="mp3", audio=True, ffmpeg_params=["-pix_fmt", "yuv420p"])
