import os
import queue
import tempfile
from gtts import gTTS
import pygame
#from playsound import playsound
import threading
import time

class TTS():
	def __init__(self):
		self.tts_instance_tracker = 1
		self.tts_que = 0

		self.que1 = False
		self.que2 = False
		self.que3 = False
		self.que4 = False
		self.que5 = False

		self.cellsequence = False


	def tts(self, text):
		print(threading.active_count())
		print(threading.enumerate())
	#	print('###starting tracker')
	#	print(self.tts_instance_tracker)
	#	print('###starting tracker')
		if self.tts_instance_tracker >= 2 and self.que1 == False and self.que2 == False:
			self.que1 = True
			print(f"{text} is in FIRST CELL")
			while True:
				time.sleep(0.04)
				if self.tts_instance_tracker == 1:
					
					self.que1 = False
					break

		elif self.tts_instance_tracker >= 2 and self.que1 == True and self.que2 == False and self.cellsequence == False:
			self.que2 = True
			self.cellsequence = True
			print(f"{text} is in SECOND CELL")
			while True:
				self.que2 = False
				time.sleep(0.12)
				if self.tts_instance_tracker == 1 and self.que1 == False:
					self.que2 = False
					#print(f"{self.que1} is a que1 value!")
					break


		elif self.tts_instance_tracker >= 2:
			print(f"{text} is in SHUFFLE CELL")
			#todo make proper que system to make to make them appear in order rather then random
			while True:
				time.sleep(0.36)
				if self.tts_instance_tracker == 1 and self.que1 == False and self.que2 == False:
					self.cellsequence = False
					break


		self.tts_instance_tracker += 1

	#	print('###+1 = 2')
	#	print(self.tts_instance_tracker)
	#	print('###+1 = 2')

		# Create a folder for audio files
		os.makedirs("ttsvoice", exist_ok=True)

		# split the text into sentences
		sentences = text.split(".")
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
				# Skip empty sentences
				if not sentence.strip():
					print("sentance skipped because it was empty")
					continue	

				# create a text to speech object with the desired text
				#print(f"sentance!: {sentence}")
				speech = gTTS(text=sentence, lang='en')
				# save the speech as a file in the ttsvoice folder
				with tempfile.NamedTemporaryFile(suffix='.mp3', dir="ttsvoice", delete=False) as fp:
					self.tts_instance_tracker += 1
					speech.write_to_fp(fp)
					filename = fp.name
					print(f" Created file: {filename}")
					print("")

	#				print('###created file')
	#				print(self.tts_instance_tracker)
	#				print('###created file')
					
					# enqueue the file path
					file_queue.put(filename)
		# create and start the thread to create the audio files
		create_files_thread = threading.Thread(target=create_files)
		create_files_thread.start()
		#create_files_thread.join()
		# create and start the thread to play the audio files
		def play_files():
			while True:
				if not file_queue.empty():
					# dequeue the file path
					filename = file_queue.get()


					# load the audio file using pygame mixer
					sound = pygame.mixer.Sound(filename)	#todo error
					# play the audio file
					sound.play()


				#	playsound(filename)


				#	# wait until the audio finishes playing
					pygame.time.wait(int(sound.get_length() * 1000))

					# delete the audio file
					os.remove(filename)
					print(f" Deleted file: {filename}")
					print("")
					self.tts_instance_tracker -= 1
				else:
					# wait for a short time if there are no files in the queue
					#pygame.time.wait(10)
					time.sleep(0.01)
					# check if the file creation thread has finished and there are no more files in the queue
					if create_files_thread.is_alive() == False and file_queue.empty() == True:
						break
					
			# Delete all the audio files in the ttsvoice folder
			for file in os.listdir("ttsvoice"):
				if file.endswith(".mp3"):
					print("deleting all mp3 files")
					os.remove(os.path.join("ttsvoice", file))
			#print("All audio files deleted.")
			self.tts_instance_tracker -= 1
	#		print('###all files deleted')
	#		print(self.tts_instance_tracker)
	#		print('###all files deleted')

		# create and start the thread to play the audio files
		play_files_thread = threading.Thread(target=play_files)
		play_files_thread.start()
		time.sleep(0.4)
#		self.tts_instance_tracker -= 1
#		print('###3')
#		print(self.tts_instance_tracker)
#		print('###3')
		#play_files_thread.join()

		




#	def tts(self, text):
#		print('###starting tracker')
#		print(self.tts_instance_tracker)
#		print('###starting tracker')
#		if self.tts_instance_tracker >= 2:
#			#todo make proper que system to make to make them appear in order rather then random
#			while self.tts_instance_tracker >= 2:
#				time.sleep(0.05)
#				if self.tts_instance_tracker == 1:
#					break