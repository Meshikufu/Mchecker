import os
import queue
import tempfile
from gtts import gTTS
import pygame
import threading

def tts(text):
	# Create a folder for audio files
	os.makedirs("ttsvoice", exist_ok=True)

	# split the text into sentences
	sentences = text.split(". ")
	# create a queue to store the sentences
	sentence_queue = queue.Queue()
	# enqueue the sentences
	for sentence in sentences:
		sentence_queue.put(sentence)
	# create a queue to store the file paths
	file_queue = queue.Queue()
	# create a thread to dequeue and create the audio files
	def create_files():
		while not sentence_queue.empty():
			sentence = sentence_queue.get()
			# create a text to speech object with the desired text
			speech = gTTS(text=sentence, lang='en')
			# save the speech as a file in the ttsvoice folder
			with tempfile.NamedTemporaryFile(suffix='.mp3', dir="ttsvoice", delete=False) as fp:
				speech.write_to_fp(fp)
				filename = fp.name
				print(f" Created file: {filename}")
				# enqueue the file path
				file_queue.put(filename)
	# create and start the thread to create the audio files
	create_files_thread = threading.Thread(target=create_files)
	create_files_thread.start()
	# create and start the thread to play the audio files
	def play_files():
		while True:
			if not file_queue.empty():
				# dequeue the file path
				filename = file_queue.get()
				# load the audio file using pygame mixer
				sound = pygame.mixer.Sound(filename)
				# play the audio file
				sound.play()
				# wait until the audio finishes playing
				pygame.time.wait(int(sound.get_length() * 1000))
				# delete the audio file
				os.remove(filename)
				print(f" Deleted file: {filename}")
			else:
				# wait for a short time if there are no files in the queue
				pygame.time.wait(10)
				# check if the file creation thread has finished and there are no more files in the queue
				if create_files_thread.is_alive() == False and file_queue.empty() == True:
					break
		# Delete all the audio files in the ttsvoice folder
		for file in os.listdir("ttsvoice"):
			if file.endswith(".mp3"):
				os.remove(os.path.join("ttsvoice", file))
		print("All audio files deleted.")
	# create and start the thread to play the audio files
	play_files_thread = threading.Thread(target=play_files)
	play_files_thread.start()