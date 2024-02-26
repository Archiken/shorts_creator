###以下請修改
#影片名稱
audio_name = "0225講道"
#影片目錄
audio_source = r"C:\Users\lin\Documents\程式\whisper2\影片下載與剪接\{}.mp4".format(audio_name)
#根據電腦規格調整想要使用的whisper模型
whisper_model = "large-v3"


###以下請勿修改
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
    result = model.transcribe(file_path, word_timestamps=True)

    # 初始化 SRT 文本
    srt_text = ""
    txt_text = ""

    # 遍历转写结果中的每个段落，添加到 SRT 文本
    for index, seg in enumerate(result['segments']):
        start_time = format_time(seg['start'] * 1000)
        end_time = format_time(seg['end'] * 1000)
        translated_text = convert_to_traditional_chinese(seg['text'])
        srt_text += f"{index + 1}\n{start_time} --> {end_time}\n{translated_text}\n\n"
        txt_text += f"{translated_text}\n"

    # 获取不带扩展名的原始文件名
    base_file_name = os.path.splitext(os.path.basename(file_path))[0]

    # 指定要保存 SRT 文件和 TXT 文件的文件夹
    save_folder = r"C:\Users\lin\Documents\程式\whisper2\影片下載與剪接"

    # 创建一个以原始文件名命名的 .srt 文件
    srt_file = os.path.join(save_folder, f"{base_file_name}_{model_name}.srt")
    with open(srt_file, "w", encoding="utf-8") as file:
        file.write(srt_text)
    
    # 创建一个以原始文件名命名的 .txt 文件
    txt_file = os.path.join(save_folder, f"{base_file_name}_{model_name}.txt")
    with open(txt_file, "w", encoding="utf-8") as file:
        file.write(txt_text)

    return srt_file, txt_file

# 执行转写并生成 SRT 文件和 TXT 文件
srt_file, txt_file = transcribe_audio_to_srt_and_txt(audio_source, whisper_model)
print(f"SRT 文件已保存为: {srt_file}")
print(f"TXT 文件已保存为: {txt_file}")



