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
import pyperclip, pyautogui, sqlite3, queue, tempfile



#os.chdir('C:/Programming/Python Projects/Mchecker')

#todo4 this one below doesnt hide message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
print("")
pygame.mixer.init()



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

class Mathtest():
	def mmath(self):
		big = 23
		small = 3
		if big >= small:
			gui.add_log_message("　    　  lﾆヽ")
			gui.add_log_message("　    　 |= | ")
			gui.add_log_message("　    　 |_ |")
			gui.add_log_message("　　/⌒|~ |⌒i-、")
			gui.add_log_message("　 /|　|　|　| ｜")
			gui.add_log_message("　｜(　(　(　(　｜")
			gui.add_log_message("　｜　　　　　 ｜")
			gui.add_log_message("　 ＼　　　　　/")
			gui.add_log_message("　　 ＼　　　 |")

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

class gui:
	def __init__(self, master):
		self.master = master

		self.mt = Mathtest()
		self.ba = buttons_actions()

		self.main_frame_buttons = ttk.Frame(self.master)
		self.main_frame_buttons.pack(side=TOP)

		self.bottom_frame = ttk.Frame(self.main_frame_buttons)
		self.bottom_frame.pack(side=LEFT)

		self.top_frame = ttk.Frame(self.main_frame_buttons)
		self.top_frame.pack(side=RIGHT)
		#todo2		make sidebar that will count from sleep_duration
		#self.progress_bar_frame = ttk.Frame(self.master)
		#self.progress_bar_frame.pack(side=RIGHT, pady=5)

		#self.progress_bar = ttk.Progressbar(self.progress_bar_frame, orient="horizontal", length=300, mode="indeterminate")
		#self.progress_bar.pack(side=TOP, pady=5)
		#
		self.b1 = ttk.Button(self.top_frame, text="Button 1", bootstyle=SUCCESS, command=self.mt.mmath)
		self.b1.pack(side=LEFT, padx=5, pady=5)

		self.b3 = ttk.Button(self.top_frame, text="Hide", bootstyle=(DANGER, OUTLINE), command=self.ba.hide_app)
		self.b3.pack(side=RIGHT, padx=5, pady=5)

		# Create the middle frame for the chat box
		self.middle_frame = ttk.Frame(self.master)
		self.middle_frame.pack(side=TOP, fill=ttk.BOTH, expand=True)

		self.gui = ttk.Text(self.middle_frame, height=15, width=70)
		self.gui.pack(side=TOP, fill=ttk.BOTH, expand=True)

		self.update_manga_buttons()

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

with open('data.txt', 'r') as file:
			for line in file:
				key, value = line.split('=')
				key = key.strip()
				value = value.strip()
				exec(f"{key} = {value}")

#todo		make manga_dict use api, or use both name and value of upper "with function"
#todo3		make easier way to add manga, instead of writing whole new dictionary section and adding it to data.txt

class urlScalping():
	def __init__(self):
		self.manga_dict = {
			'Chainsaw man': {
				'url': "https://mangareader.to/read/chainsaw-man-96/en/chapter-{}",
				'chapter_number': chainsaw_man_chapter,
				'update_chapter': "chainsaw_man_chapter"
			},
			'one-punch man': {
				'url': "https://mangareader.to/read/onepunch-man-40/en/chapter-{}",
				'chapter_number': one_punch_man_chapter,
				'update_chapter': "one_punch_man_chapter"
			},
			'Meiou-sama': {
				'url': "https://mangareader.to/read/meiou-sama-ga-tooru-no-desu-yo-58998/en/chapter-{}",
				'chapter_number': meiou_sama_chapter,
				'update_chapter': "meiou_sama_chapter"
			}
		}

	def manga_checker(self):
		manga_is_out = {}
		while True:
			for key in self.manga_dict:
				url = self.manga_dict[key]['url'].format(self.manga_dict[key]['chapter_number'])
				response = requests.get(url)
				soup = BeautifulSoup(response.content, 'html.parser')
				scalping = soup.find_all('div', {'class': 'c4-small'}) + soup.find_all('h2', {'class': 'manga-name'}) + soup.find_all('div', {'class': 'd-block'})

				current_time = datetime.datetime.now().strftime('%H:%M:%S')

				if "Oops! We can't find this page." in str(scalping):
					log_message = f"{key} chapter number {self.manga_dict[key]['chapter_number']} isn't out yet"
					log_messagetts = f"{key}, chapter number {self.manga_dict[key]['chapter_number']}, isn't out yet"
					print(log_message)
					gui.add_log_message(log_message)
					#tts(log_messagetts)
					debug = 1
				elif key.lower() in str(scalping).lower():
					if key not in manga_is_out:
						manga_is_out[key] = self.manga_dict[key]['chapter_number']
					log_message = f"{key} Chapter number {self.manga_dict[key]['chapter_number']} IS OUT"
					log_messagetts = f"{key}, IS OUT"
					print(log_message)
					gui.add_log_message(log_message)
					tts(log_messagetts)
					self.manga_dict[key]['chapter_number'] += 1  # increment the current chapter number by 1
					time.sleep(3)
					debug = 2
				else:
					log_message = f"{key} Chapter number {self.manga_dict[key]['chapter_number']} scalping ERROR"
					log_messagetts = f"{key}, Chapter number {self.manga_dict[key]['chapter_number']}, scalping ERROR"
					print(log_message)
					gui.add_log_message(log_message)
					#tts(log_messagetts)
					debug = 3

			
			print(debug)
			if debug == 3:
				tts("mangareader is downn")
				print("mangareader is downn")
				time.sleep(10)

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

				sleep_duration = 20 * 60
				#todo2 make scrollbar here
				print(f"{current_time}  ===  checking again in {int(sleep_duration/60)} minutes")
				gui.add_log_message("waiting 20 minutes until next check...")
				gui.add_log_message("")
				time.sleep(1)
				for i in tqdm(range(sleep_duration), desc=f"", bar_format='{l_bar}{bar}|'):
					time.sleep(60)
				print("        ")
				#time.sleep(duration)
				with open("data.txt", 'w') as file:
					for key in self.manga_dict:
						file.write(self.manga_dict[key]['update_chapter'] + "=" + str(self.manga_dict[key]['chapter_number']) + "\n")

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