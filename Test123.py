from  modules.GoogleTTSv2 import TTSv2

text = "$tts Really big test is here!"
path = 'modules/TTSdb'
#TTSv2(text)
#TTSv2("second test", path)
unpack_NamePath = TTSv2("additional texts", path)
filename, path_tts_db = unpack_NamePath
filename_path = rf'{path_tts_db}/{filename}'
print(filename)
print(path_tts_db)
print(filename_path)
print(unpack_NamePath)