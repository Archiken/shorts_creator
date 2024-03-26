1. 使用Download.py將Youtube影片下載並剪輯出要保留的講道片段。
2. 使用Transcript.py將講道影片轉成逐字稿，一份(無時間軸).txt與一份(附時間軸).srt 
3. 將.txt輸入ChatGPT，告訴ChatGPT:【請針對上傳的文檔做摘要，並給出與主旨相符4至6段與文檔一模一樣的內容，長度介於140至180字之間。】
5. 在ChatGPT提供的內文中找出自己感興趣的段落，回去參照.srt檔的時間軸，並將需要的段落時間輸入Clip.py
6. Clip.py將把指示的時間段剪下(並將多段合併成)一部影片；同時用這部影片再利用whisper生成.srt檔案的逐字稿。
7. 點進Clip生成的.srt檔，確認每一行不超過13個中文字(以免短影片字幕超出橫幅)，並將想要紅字強調的部分使用小括號()框起來。
8. 完成.srt檔的編輯後，使用MakingShorts.py，將短影片生成。

安裝包注意:
運行MakingShorts.py時可能碰到: AttributeError: 'ImageDraw' object has no attribute 'textsize'；可以嘗試確認Pillow的安裝版本，若是10.0請嘗試重新安裝Pillow=9.5.0
