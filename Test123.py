from  modules.GoogleTTSv2 import TTSv2

text = "$tts Really big test is here!"
path = 'modules/TTSdb'
TTSv2(text)
TTSv2("second test", path)
filename, path_tts_db = TTSv2("additional texts", path)
filename_path = rf'{path_tts_db}/{filename}'
print(filename)
print(path_tts_db)
print(filename_path)