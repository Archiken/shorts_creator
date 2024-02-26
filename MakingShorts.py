###以下請更改
#請填入需要編輯的影片
edit_video = "0225講道_耶穌不同的眼光.mp4"
#填入對應的.srt
edit_srt = '0225講道_耶穌不同的眼光_large-v3.srt'
#輸出的檔案名稱
output_video = "0225耶穌不同的眼光(剪接).mp4"
#影片中的標題
title =  '耶穌不同的眼光'


###以下不要改
import os
from moviepy.editor import *
from PIL import Image, ImageFont, ImageDraw

def time2sec(t):
    arr = t.split(' --> ')
    s1 = arr[0].split(',')
    s2 = arr[1].split(',')
    start = int(s1[0].split(':')[0])*3600 + int(s1[0].split(':')[1])*60 + int(s1[0].split(':')[2]) + float(s1[1])*0.001
    end = int(s2[0].split(':')[0])*3600 + int(s2[0].split(':')[1])*60 + int(s2[0].split(':')[2]) + float(s2[1])*0.001
    return [start, end]

def read_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        srt_lines = f.read().split('\n')
    
    sec_list = []
    text_list = []

    i = 0
    while i < len(srt_lines):
        if srt_lines[i].isdigit():  
            time_range = srt_lines[i + 1]  
            sec_list.append(time2sec(time_range))
            text = ""
            j = i + 2
            while j < len(srt_lines) and srt_lines[j] != '':
                text += srt_lines[j] + "\n"
                j += 1
            text_list.append(text.strip())  
            i = j  
        i += 1
    return sec_list, text_list

def add_rounded_corners(im, rad, fill_color):
    """
    Add rounded corners to an image.
    :param im: The image to be modified.
    :param rad: The radius of the rounded corner.
    :param fill_color: Fill color for the rounded corner, including alpha for transparency.
    :return: Image with rounded corners.
    """
    # Create a rounded corner mask.
    corner = Image.new('L', (rad, rad), 0)
    draw = ImageDraw.Draw(corner)
    draw.pieslice((0, 0, rad * 2, rad * 2), 180, 270, fill=fill_color[3])
    
    # Create an alpha mask.
    alpha = Image.new('L', im.size, fill_color[3])  # Use alpha from fill color.
    w, h = im.size

    # Apply the rounded corner mask to each corner of the alpha mask.
    alpha.paste(corner, (0, 0))
    alpha.paste(corner.rotate(90), (0, h - rad))
    alpha.paste(corner.rotate(180), (w - rad, h - rad))
    alpha.paste(corner.rotate(270), (w - rad, 0))
    
    # Put the alpha mask onto the image.
    im.putalpha(alpha)
    return im

def create_text_clip(text, font_path='msjhbd.ttc', font_size=45, 
                     card_size=(600, 255), text_color=(255, 255, 255), 
                     card_color=(102, 204, 0, 190), stroke_width=3, 
                     stroke_fill='black', corner_radius=20):
    """
    Create a text clip with specified attributes. Text within parentheses will be colored red, and the parentheses themselves will be removed. Text is centered horizontally.
    """
    # Create a new image with RGBA mode (including alpha for transparency)
    img = Image.new('RGBA', card_size, card_color)
    img = add_rounded_corners(img, corner_radius, card_color)
    draw = ImageDraw.Draw(img)
    
    # Load a font
    font = ImageFont.truetype(font_path, font_size)

    # Split the text into lines
    lines = text.split('\n')
    line_heights = [draw.textsize(line, font=font)[1] for line in lines]
    total_height = sum(line_heights) + (len(lines) - 1) * 10  # 10 pixels line spacing
    # Starting Y position to center text vertically
    y = (card_size[1] - total_height) / 2

    for line in lines:
        # Remove text within parentheses and calculate line width
        processed_line = ''
        start = 0
        while start < len(line):
            start_idx = line.find('(', start)
            end_idx = line.find(')', start) if start_idx != -1 else -1

            if start_idx == -1 or end_idx == -1:
                processed_line += line[start:]
                break

            if start_idx > start:
                processed_line += line[start:start_idx]

            processed_line += line[start_idx+1:end_idx]  # Add text within parentheses
            start = end_idx + 1

        line_width, _ = draw.textsize(processed_line, font=font)
        x = (card_size[0] - line_width) / 2  # 水平居中

        # Draw the processed line
        start = 0
        while start < len(line):
            start_idx = line.find('(', start)
            end_idx = line.find(')', start) if start_idx != -1 else -1

            if start_idx == -1 or end_idx == -1:
                draw.text((x, y), line[start:], font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=stroke_fill)
                break

            if start_idx > start:
                draw.text((x, y), line[start:start_idx], font=font, fill=text_color, stroke_width=stroke_width, stroke_fill=stroke_fill)
                width, _ = draw.textsize(line[start:start_idx], font=font)
                x += width

            red_text = line[start_idx+1:end_idx]
            draw.text((x, y), red_text, font=font, fill=(255, 0, 0), stroke_width=stroke_width, stroke_fill=stroke_fill)
            width, _ = draw.textsize(red_text, font=font)
            x += width

            start = end_idx + 1

        y += draw.textsize(processed_line, font=font)[1] + 10  # 10 pixels line spacing

    return img


def create_title_clip(text, font_path='msjhbd.ttc', font_size=35, 
                      card_size=(300, 112), text_color=(255, 255, 255), 
                      card_color=(0, 76, 153, 128), stroke_width=5, 
                      stroke_fill='black', corner_radius=30):
    """
    Create a title clip with a specific style.
    """
    # Create a new image with RGBA mode (including alpha for transparency)
    img = Image.new('RGBA', card_size, (255, 255, 255, 0))  # Transparent background
    img = add_rounded_corners(img, corner_radius, card_color)  # Add rounded corners
    draw = ImageDraw.Draw(img)
    
    # Load a font
    font = ImageFont.truetype(font_path, font_size)

    # Calculate text width and X position to center text horizontally
    text_width, text_height = draw.textsize(text, font=font)
    x = (card_size[0] - text_width) / 2
    y = (card_size[1] - text_height) / 2

    # Draw the text onto the image with a stroke
    draw.text((x, y), text, font=font, fill=text_color, 
              stroke_width=stroke_width, stroke_fill=stroke_fill)
    
    return img

def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

# font = ImageFont.truetype('msjhbd.ttc', 40)

# font = ImageFont.truetype('STKAITI.TTF', 40)

video = VideoFileClip(edit_video)
original_width, original_height = video.size
x_start = max(original_width - 608, 0)
y_start = max(original_height - 1080, 0)
video = video.crop(x1=x_start, y1=y_start, width=608, height=1080)

sec_list, text_list = read_srt(edit_srt)

output_list = []
previous_end = 0
fadein_duration = 0.8  # 2秒淡入时长

for i, (sec, text) in enumerate(zip(sec_list, text_list)):
    if previous_end < sec[0]:
        output_list.append(video.subclip(previous_end, sec[0]))
    
    text_clip = create_text_clip(text)
    text_clip_path = f'text_clip_{i}.png'
    text_clip.save(text_clip_path)

    subtitle_clip = ImageClip(text_clip_path, transparent=True).set_duration(sec[1]-sec[0]).set_position(('center', 'center'))
    
    # 如果是第一个字幕片段，应用fadein效果
    if i == 0:
        subtitle_clip = subtitle_clip.fadein(fadein_duration)
    
    video_clip = video.subclip(sec[0], sec[1])
    combined_clip = CompositeVideoClip([video_clip, subtitle_clip])
    output_list.append(combined_clip)
    
    previous_end = sec[1]

if previous_end < video.duration:
    output_list.append(video.subclip(previous_end, video.duration))

title_img = create_title_clip(title)
title_img_path = 'title_clip.png'
title_img.save(title_img_path)
title_clip = ImageClip(title_img_path, transparent=True).set_duration(video.duration).set_position(('left', 'top'))

# Combine each clip in the output_list with the title clip
for i, clip in enumerate(output_list):
    output_list[i] = CompositeVideoClip([clip, title_clip.set_duration(clip.duration)])

final_clip = concatenate_videoclips(output_list)
final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac", fps=24, bitrate="8000k")

for i in range(len(text_list)):
    remove_file(f'text_clip_{i}.png')
remove_file(title_img_path)