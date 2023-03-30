from flask import Flask
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import time, datetime
import threading
import win32gui, win32con, win32api, win32console
import sys, os
import pystray
import PIL.Image
from tqdm import tqdm
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import pygame
import speech_recognition as sr
from gtts import gTTS
import webbrowser
import keyboard
import pyperclip, pyautogui, sqlite3, queue, tempfile, re



#os.chdir('C:/Programming/Python Projects/Mchecker')

#todo4 this one below doesnt hide message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
print("")
pygame.mixer.init()



#todo5 add controller class that will contains reusable variables
sleep_duration = 20
current_time = datetime.datetime.now().strftime('%H:%M:%S')


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


def on_hotkey():
	# get the text from the clipboard
	copytext = pyperclip.paste()

	# convert the text to speech
	tts(copytext)


def hotkey_listener():
	# register the hotkey
	keyboard.add_hotkey('alt+s', on_hotkey)

	# start the listener loop
	keyboard.wait()

class buttons_actions():
	def hide_app(self):
		root.withdraw()

	def openLastChapterLink(self, url):
		webbrowser.open(url)

	def get_last_chapters(self):
		with open("lastchaptername.txt", 'r') as file:
			manga_names = [line.strip() for line in file.readlines()]

		with open("lastchapter.txt", 'r') as file:
			urls = file.read().split("\n")

		return manga_names, urls

class gui():
	def __init__(self, master):
		self.master = master

		self.ba = buttons_actions()

		self.main_frame_buttons = ttk.Frame(self.master)
		self.main_frame_buttons.pack(side=TOP)

		self.bottom_frame = ttk.Frame(self.main_frame_buttons)
		self.bottom_frame.pack(side=LEFT)

		self.top_frame = ttk.Frame(self.main_frame_buttons)
		self.top_frame.pack(side=RIGHT)

		#########################################################################################################
		def append_clipboard_to_file():
			clipboard_content = pyperclip.paste()
			# Extract the chapter number from the URL
			chapter_num = re.search(r'chapter-(\d+)', clipboard_content).group(1)
			# Add 1 to the chapter number and create the new URL
			new_url = re.sub(r'chapter-\d+', f'chapter-{int(chapter_num)+1}', clipboard_content)
			with open("data.txt", "a") as f:
				f.write(new_url + "\n")

		self.b1 = ttk.Button(self.top_frame, text="Add url", bootstyle=SUCCESS, command=append_clipboard_to_file)    #lambda: [append_clipboard_to_file(), start_sleep_bar()])
		self.b1.pack(side=LEFT, padx=5, pady=5)
		#########################################################################################################

		self.b3 = ttk.Button(self.top_frame, text="Hide", bootstyle=(DANGER, OUTLINE), command=self.ba.hide_app)
		self.b3.pack(side=RIGHT, padx=5, pady=5)

		self.frame_for_chatbox = ttk.Frame(self.master)
		self.frame_for_chatbox.pack(side=BOTTOM)

		# Create the middle frame for the chat box
		self.middle_frame = ttk.Frame(self.frame_for_chatbox)
		self.middle_frame.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.gui = ttk.Text(self.middle_frame, height=0, width=70)
		self.gui.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.sleep_bar = ttk.Progressbar(self.middle_frame, bootstyle='success', orient=VERTICAL, maximum=100, mode='determinate', length=200, value=0)
		self.sleep_bar.pack(side=RIGHT, fill=X, pady=0, expand=True)



		#########################################################################################################
		self.update_manga_buttons()

	def start_sleep_bar2(self):
		#tts("test")
		print(f"{current_time} === progress bar start")
		# Set the total number of seconds to wait
		total_secs = 20
		# Set the number of steps in the progress bar (e.g. 100 steps for 100%)
		num_steps = 100
		# Calculate the number of seconds for each step
		secs_per_step = sleep_duration / num_steps
		# Set the initial progress bar value to 0
		self.sleep_bar['value'] = 0
		# Update the progress bar every second until it reaches 100%
		for i in range(num_steps):
			self.sleep_bar.step(1)
			self.sleep_bar.update()
			time.sleep(secs_per_step)


	def update_manga_buttons(self):
		manga_names, urls = self.ba.get_last_chapters()

		# Remove existing buttons
		for child in self.bottom_frame.winfo_children():
			child.destroy()

		# Create buttons for each manga and add them to the window
		for i in range(len(manga_names)):
			name = manga_names[i]
			url = urls[i]
			button = ttk.Button(self.bottom_frame, text=name, bootstyle=(DARK, OUTLINE), command=lambda url=url: self.ba.openLastChapterLink(url))
			button.pack(side=LEFT, padx=5, pady=5)

		# Schedule another call to update the manga buttons in 5 seconds
		self.master.after(2000, self.update_manga_buttons)
		#########################################################################################################
	def add_log_message(self, msg):
		self.gui.insert(ttk.END, msg + '\n')
		self.gui.see(ttk.END)


def icon_tray():
	image = PIL.Image.open('power.png')
	win = win32gui.GetForegroundWindow()
	console = win32console.GetConsoleWindow()
	win32gui.ShowWindow(console ,0)
	win32api.SetConsoleCtrlHandler(lambda x: True, True)  
	
	def on_clicked(icon, item):
		current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if str(item) == "open console":
			win32gui.ShowWindow(console, win32con.SW_SHOW)
		elif str(item) == "hide console":
			win32gui.ShowWindow(console ,0)
			win32api.SetConsoleCtrlHandler(lambda x: True, True)     
		elif str(item) == "open app":
			root.deiconify()
		elif str(item) == "hide app":
			root.withdraw()      
		elif str(item) == "Exit":
			root.destroy()

	def action():
		root.deiconify()

	icon = pystray.Icon("power", image)
	icon.menu = pystray.Menu(
		pystray.MenuItem('1', action, default=True, visible=False),
		pystray.MenuItem("open app", on_clicked),
		pystray.MenuItem("hide app", on_clicked),
		pystray.MenuItem("open console", on_clicked),
		pystray.MenuItem("hide console", on_clicked),
		pystray.MenuItem("Exit", on_clicked)
	)       
	icon.run() 

class urlScalping():
	def __init__(self):
		# initialize manga dictionary with data from data.txt
		self.manga_dict = self.get_manga_dict()
	def get_manga_dict(self):
		with open('data.txt') as f:
			data = f.read().splitlines()
		manga_dict = {}
		for line in data:
			start = line.find("read/") + 5
			end = line.find("-", start)
			if end != -1 and end+3 < len(line) and line[end+1:end+3].isdigit():
				#end = line.find("-", end+1)
				key = line[start:end].replace("-", " ")
				start = line.rfind("chapter-") + len("chapter-")
				value = line[start:]
				#print("debug if")
			else:
				end = line.find("-", end+1)
				key = line[start:end].replace("-", " ")
				start = line.rfind("chapter-") + len("chapter-")
				value = line[start:]
				#print("debug else") 
			manga_dict[key.lower()] = {
				'url': line,
				'last_chapter_name': key,
				'chapter_number': int(value)
			}
		return manga_dict

	def manga_checker(self):
		while True:
			#pull fresh data from data.txt
			self.manga_dict = self.get_manga_dict()
			manga_is_out = {}
			for key in self.manga_dict:
				url = self.manga_dict[key]['url'].format(self.manga_dict[key]['chapter_number'])
				response = requests.get(url)
				soup = BeautifulSoup(response.content, 'html.parser')
				scalping = soup.find_all('div', {'class': 'c4-small'}) + soup.find_all('span', {'class': 'hrr-name'}) + soup.find_all('div', {'class': 'd-block'})#fix this + soup.find_all('span', {'class': 'hrr-name'})
				current_time = datetime.datetime.now().strftime('%H:%M:%S')

				if "Oops! We can't find this page." in str(scalping):
					log_message = f"#{key} chapter number {self.manga_dict[key]['chapter_number']} isn't out yet"
					log_messagetts = f"{key}, chapter number {self.manga_dict[key]['chapter_number']}, isn't out yet"
					print(log_message)
					gui.add_log_message(log_message)
					#tts(log_messagetts)
					debug = 1
				elif "Comments".lower() in str(scalping).lower():
					if key not in manga_is_out:
						manga_is_out[key] = self.manga_dict[key]['chapter_number']
					log_message = f"#{key} Chapter number {self.manga_dict[key]['chapter_number']} IS OUT"
					log_messagetts = f"{key}, IS OUT"
					print(log_message)
					gui.add_log_message(log_message)
					tts(log_messagetts)
					self.manga_dict[key]['chapter_number'] += 1  # increment the current chapter number by 1
					time.sleep(3)
					debug = 2
				elif "Bad gateway".lower() in str(scalping):
					debug = 4

				else:
					log_message = f"{key} Chapter number {self.manga_dict[key]['chapter_number']} scalping ERROR"
					log_messagetts = f"{key}, Chapter number {self.manga_dict[key]['chapter_number']}, scalping ERROR"
					print(log_message)
					gui.add_log_message(log_message)
					#tts(log_messagetts)
					debug = 5

			
			#print(debug)
			if debug == 4:
				tts("mangareader is downn")
				print("mangareader is downn")
				time.sleep(60)

			if debug == 5:
				tts("error")
				print("error")
				time.sleep(60)

			elif debug < 3:        
				if manga_is_out:
					with open("lastchapter.txt", 'w') as file:
						for key, value in manga_is_out.items():
							file.write(self.manga_dict[key]['url'].format(value) + "\n")
					#manga_is_out.clear()

					with open("lastchaptername.txt", 'w') as file:
						for key in manga_is_out.keys():
							file.write(key + "\n")
						manga_is_out.clear()

				with open("data.txt", 'w') as file:
					for key in self.manga_dict:
						# Extract the URL prefix by removing the part after "chapter-"
						url_prefix = self.manga_dict[key]['url'][:self.manga_dict[key]['url'].rfind("chapter-")+len("chapter-")]
						# Write the URL with the updated chapter number to the file
						file.write(f"{url_prefix}{self.manga_dict[key]['chapter_number']}\n")
						self.manga_dict[key]['url'] = f"{url_prefix}{self.manga_dict[key]['chapter_number']}"
				
				#log_message_before_sleep = f"====="{current_time}"====="
				gui.add_log_message(f"###> {current_time} <###")
				gui.add_log_message("")
				print(f"{current_time} === starting progress bar for {sleep_duration / 60} minutes")
				gui.start_sleep_bar2()


	def manga_checker_test(self):
		conn = sqlite3.connect('manga.db')
		cursor = conn.cursor()

		cursor.execute('''
			CREATE TABLE IF NOT EXISTS manga (
				title TEXT PRIMARY KEY
			);
		''')
		conn.commit()

		while True:
			url = "https://mangareader.to/home"
			response = requests.get(url)
			soup = BeautifulSoup(response.content, 'html.parser')
			section_block = soup.find('section', {'class': 'block_area_home'})
			latest_chap_div = section_block.find('div', {'id': 'latest-chap'})
			a_tags = latest_chap_div.find_all('a', href=True, title=True)

			new_titles = []
			for a_tag in a_tags:
				title = a_tag.text
				cursor.execute('SELECT * FROM manga WHERE title = ?', (title,))
				row = cursor.fetchone()
				if row is None:
					new_titles.append(title)
					cursor.execute('INSERT INTO manga VALUES (?)', (title,))
					conn.commit()

			if len(new_titles) > 0:
				print(' New titles added to the database:')
#				for title in new_titles:
#					if len(title) < 20:
#						print(title)
#
#
#			# Print out titles with length < 20
#			cursor.execute('SELECT title FROM manga')
#			rows = cursor.fetchall()
#			for row in rows:
#				if len(row[0]) < 20:
#					print(row[0])
			time.sleep(300)


def start_threads():
	t1 = threading.Thread(target=urlScalping().manga_checker)
	t1.daemon = True
	t1.start()

	t2 = threading.Thread(target=icon_tray)
	t2.daemon = True
	t2.start()

	t3 = threading.Thread(target=urlScalping().manga_checker_test)
	t3.daemon = True
	t3.start()


def start_threads_tts():
	t7 = threading.Thread(target=hotkey_listener)
	t7.daemon = True
	t7.start()

if __name__ == "__main__":
	root = ttk.Window()
	gui = gui(root)
	start_threads()
	start_threads_tts()
	root.mainloop()