###以下請根據不同影片作修改
video_url = 'https://www.youtube.com/watch?v=BMpvObeFI_4' #影片網址
custom_title = '0225講道' #想要儲存的檔名
start_time = '00:31:28' #講道開始時間
end_time = '01:25:26' #講道結束時間
download_path = r'C:\Users\lin\Documents\程式\whisper2\影片下載與剪接' #想要存檔的路徑



###以下不用修改
import os
import subprocess

def download_video_ytdlp(url, download_path, custom_title):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    video_path = os.path.join(download_path, f"{custom_title}_video.mp4").replace('\\', '\\\\')
    audio_path = os.path.join(download_path, f"{custom_title}_audio.m4a").replace('\\', '\\\\')
    temp_filepath = os.path.join(download_path, f"{custom_title}_temp.mp4").replace('\\', '\\\\')

    # 下载视频
    cmd_download_video = f"yt-dlp -f 137 -o \"{video_path}\" {url}"
    subprocess.run(cmd_download_video, shell=True)

    # 下载音频
    cmd_download_audio = f"yt-dlp -f 140 -o \"{audio_path}\" {url}"
    subprocess.run(cmd_download_audio, shell=True)

    # 合并视频和音频到临时文件
    cmd_merge = f"ffmpeg -i \"{video_path}\" -i \"{audio_path}\" -c:v copy -c:a aac \"{temp_filepath}\""
    subprocess.run(cmd_merge, shell=True)

    return temp_filepath

def cut_video_ytdlp(filepath, download_path, video_title, start_time, end_time):
    final_output_path = os.path.join(download_path, f'{video_title}.mp4').replace('\\', '\\\\')

    # NVIDIA GPU 加速命令
    cmd = f"ffmpeg -hwaccel cuda -i \"{filepath}\" -ss {start_time} -to {end_time} -c:v h264_nvenc -preset fast \"{final_output_path}\""
    subprocess.run(cmd, shell=True)

    return final_output_path

def delete_intermediate_files(video_path, audio_path, temp_filepath):
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if os.path.exists(temp_filepath):
        os.remove(temp_filepath)


temp_filepath = download_video_ytdlp(video_url, download_path, custom_title)
print("下載和合并完成")

# 中间生成的视频和音频文件路径
video_path = os.path.join(download_path, f"{custom_title}_video.mp4").replace('\\', '\\\\')
audio_path = os.path.join(download_path, f"{custom_title}_audio.m4a").replace('\\', '\\\\')

final_output_path = cut_video_ytdlp(temp_filepath, download_path, custom_title, start_time, end_time)
print("剪辑完成，剪辑后的文件保存为：", final_output_path)

# 删除中间的视频、音频文件和临时合并文件
delete_intermediate_files(video_path, audio_path, temp_filepath)
print("已删除中间文件")



