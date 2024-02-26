###以下請修改
#要處理的檔名
video_name = "0225講道"
#要生成的剪接檔名
new_video_name = video_name + "_耶穌不同的眼光"
#影片路徑
full_path = r"C:\Users\lin\Documents\程式\whisper2\影片下載與剪接\{}.mp4".format(video_name)
#根據你要的片段做輸入"hr:min:sec,millisec"
time_ranges = [
    ("00:40:42,420", "00:41:04,151"),
    ("00:41:23,903", "00:41:43,818")
    # ("00:06:53,150", "00:07:02,920"),  #耶穌的方向跟我們是不同的
    # ("00:07:28,480", "00:07:40,060")  
    # ("00:40:57,480", "00:41:22,401")  
    # ("00:32:51,568", "00:33:11,735"),
    # ("00:32:51,568", "00:32:59,068"),
    # ("00:33:01,067", "00:33:11,735"),
    # ("00:45:40,980", "00:45:51,568") 
    # ("00:00:00,000", "00:00:00,000")
]
  

###以下請物修改
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

# 下載目錄
download_folder = r"C:\Users\lin\Documents\程式\whisper2\影片下載與剪接"

def convert_time(time_str):
    """Convert time string to (hours, minutes, seconds, milliseconds) format."""
    parts = time_str.replace(',', ':').split(':')
    h, m, s = map(int, parts[:3])
    ms = int(parts[3]) if len(parts) > 3 else 0
    return h, m, s + ms / 1000

try:
    print("正在剪接影片...")
    # 時間範圍列表
    time_ranges = time_ranges

    # 設定裁剪的起始和結束時間
    clips = []
    for start, end in time_ranges:
        start_time = convert_time(start)
        end_time = convert_time(end)
        clips.append(VideoFileClip(full_path).subclip(start_time, end_time))

    new_video = concatenate_videoclips(clips)
    new_video.write_videofile(os.path.join(download_folder, new_video_name + ".mp4"), codec='libx264')

    print("剪接完成")

except Exception as e:
    print(f"發生錯誤：{e}")

#把.mp4轉一個mp3
video_path = os.path.join(r'C:\Users\lin\Documents\程式\whisper2\影片下載與剪接', new_video_name + '.mp4')
video = VideoFileClip(video_path)
audio = video.audio
audio.write_audiofile(r'C:\Users\lin\Documents\程式\whisper2\影片下載與剪接'+'/'+ new_video_name + '.mp3')

print('mp3 ok!')




mp3_source = r"C:\Users\lin\Documents\程式\whisper2\影片下載與剪接\{}.mp3".format(new_video_name)
whisper_model = "large-v3"
import whisper
import os
from opencc import OpenCC

def convert_to_traditional_chinese(text):
    """将简体中文转换为繁体中文"""
    cc = OpenCC('s2t')  # s2t 表示从简体到繁体
    return cc.convert(text)

def format_time(milliseconds):
    """将毫秒转换为 SRT 时间格式 (HH:MM:SS,mmm)"""
    milliseconds = int(milliseconds)  # 确保毫秒值是整数
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"

def transcribe_audio_to_srt_and_txt(file_path, model_name):
    # 载入 Whisper 模型
    model = whisper.load_model(model_name).to("cuda")

    # 使用模型转写音频
    result = model.transcribe(file_path, word_timestamps=True, initial_prompt= '')

    # 初始化 SRT 文本
    srt_text = ""

    # 遍历转写结果中的每个段落，添加到 SRT 文本
    for index, seg in enumerate(result['segments']):
        start_time = format_time(seg['start'] * 1000)
        end_time = format_time(seg['end'] * 1000)
        translated_text = convert_to_traditional_chinese(seg['text'])

        srt_text += f"{index + 1}\n{start_time} --> {end_time}\n{translated_text}\n\n"

    # 获取不带扩展名的原始文件名
    base_file_name = os.path.splitext(os.path.basename(file_path))[0]

    # 指定要保存 SRT 文件和 TXT 文件的文件夹
    save_folder = r"C:\Users\lin\Documents\程式\whisper2\影片下載與剪接"

    # 创建一个以原始文件名命名的 .srt 文件
    srt_file = os.path.join(save_folder, f"{base_file_name}_{model_name}.srt")
    with open(srt_file, "w", encoding="utf-8") as file:
        file.write(srt_text)
    

    return srt_file

# 执行转写并生成 SRT 文件和 TXT 文件
srt_file = transcribe_audio_to_srt_and_txt(mp3_source, whisper_model)
print(f"SRT 文件已保存为: {srt_file}")

os.remove(r'C:\Users\lin\Documents\程式\whisper2\影片下載與剪接'+'/'+ new_video_name + '.mp3')
