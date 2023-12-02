from  modules.GoogleTTSv2 import GenerateAudioFile

text = "$tts Really big test is here!"

GenerateAudioFile(text)
GenerateAudioFile("second test")
GenerateAudioFile("additional text")