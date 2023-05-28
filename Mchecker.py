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
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as tk
import pygame
import speech_recognition as sr
from gtts import gTTS
import webbrowser
import keyboard
import pyperclip, pyautogui, sqlite3, queue, tempfile, re
from tkinter import Tk, PhotoImage
import json
#gmail stuff below
import ssl
from simplegmail import Gmail
from simplegmail.query import construct_query



#os.chdir('C:/Programming/PythonProjects/Mchecker')

#todo4 this one below doesnt hide message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
print("")
pygame.mixer.init()



#todo5 add controller class that will contains reusable variables
sleep_duration = 15 * 20# * 60
sleep_duration2 = 15 * 2

current_time = datetime.datetime.now().strftime('%H:%M:%S')

from modules.GoogleTTS import tts


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
###########################################
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

class ttkgui():
	def __init__(self, master):
		self.master = master
		#root.overrideredirect(True)
		#menu = ttk.Menu(root)
		#root.config(menu=menu)
		root.title("Mchecker")
		root.geometry("+700+500")
		#icon = PhotoImage(file='cat.gif')
		#root.wm_iconphoto(True, icon)
		
		self.ba = buttons_actions()

		self.top_frame_buttonsMain = ttk.Frame(self.master)#, bootstyle="secondary")
		self.top_frame_buttonsMain.pack(side=TOP, fill=X)#, expand=YES)

		self.leftleft_subframe_buttonsMain = ttk.Frame(self.top_frame_buttonsMain, padding=0)
		self.leftleft_subframe_buttonsMain.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.left_subframe_buttonsMain = ttk.Frame(self.top_frame_buttonsMain)#, bootstyle="info")
		self.left_subframe_buttonsMain.pack(side=LEFT, fill=tk.X, expand=True)

		self.right_subframe_buttonsMain = ttk.Frame(self.top_frame_buttonsMain)#, bootstyle="warning")
		self.right_subframe_buttonsMain.pack(side=RIGHT)

		#########################################################################################################
		def append_clipboard_to_file():
			clipboard_content = pyperclip.paste()
			# Extract the chapter number from the URL
			chapter_num = re.search(r'chapter-(\d+)', clipboard_content).group(1)
			# Add 1 to the chapter number and create the new URL
			new_url = re.sub(r'chapter-\d+', f'chapter-{int(chapter_num)+1}', clipboard_content)
			with open("data.txt", "a") as f:
				f.write(new_url + "\n")

			my_scalper = urlScalping()
			my_scalper.update_data_json()

			self.create_menu()
			print(f"{clipboard_content} is added")
			chatMain.add_log_message(f"{clipboard_content} is added!")
			chatMain.add_log_message("")
			tts("added!")

			#refresh open url menu
			self.open_manga_list.config(menu="")

			# read the data from the JSON file into a Python dictionary
			with open('data.json', 'r') as f:
				data = json.load(f)

			# create the menu
			menu = tk.Menu(self.open_manga_list, tearoff=False)
			for title in data.keys():
				url = data[title]['url']
				menu.add_command(label=title, command=lambda u=url: (webbrowser.open_new_tab(u[:-2] + str(int(u[-2:])-1)), self.ba.hide_app()))
			# attach the menu to the Menubutton
			self.open_manga_list.config(menu=menu)

		self.b1 = ttk.Button(self.right_subframe_buttonsMain, text="Add url", bootstyle=SUCCESS, command=append_clipboard_to_file)    #lambda: [append_clipboard_to_file(), start_sleep_bar()])
		self.b1.pack(side=LEFT, padx=5, pady=5)
		#########################################################################################################
		self.us = urlScalping()

		self.menub = ttk.Menubutton(self.right_subframe_buttonsMain, text="Delete", bootstyle=DANGER)
		self.menub.pack(side=LEFT, padx=5, pady=5)
		self.create_menu()

#		self.br = ttk.Button(self.right_subframe_buttonsMain, text="refresh", bootstyle=DANGER, commaand=self.create_menu_refresh())
#		self.br.pack(side=LEFT, padx=5, pady=5)
#
#
		self.b3 = ttk.Button(self.right_subframe_buttonsMain, text="Hide", bootstyle=(DANGER, OUTLINE), command=self.ba.hide_app)
		self.b3.pack(side=RIGHT, padx=5, pady=5)

		self.bottom_frame_chatMain = ttk.Frame(self.master, padding=0)
		self.bottom_frame_chatMain.pack(side=BOTTOM, fill=ttk.BOTH, expand=True)

		self.right_subframe_chatMain = ttk.Frame(self.bottom_frame_chatMain, padding=0, bootstyle="info")
		self.right_subframe_chatMain.pack(side=RIGHT, fill=ttk.BOTH)
		
		self.left_subframe_chatMain = ttk.Frame(self.bottom_frame_chatMain, padding=0)
		self.left_subframe_chatMain.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.chatMain = ttk.Text(self.left_subframe_chatMain, height=12, width=70)
		self.chatMain.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.sleep_bar = ttk.Progressbar(self.right_subframe_chatMain, bootstyle='success-striped', orient=VERTICAL, maximum=100, mode='determinate', length=200, value=0)
		self.sleep_bar.pack(side=RIGHT, expand=YES, padx=1, pady=1, fill=ttk.BOTH)

		self.sleep_bar2 = ttk.Progressbar(self.right_subframe_chatMain, bootstyle='danger-striped', orient=VERTICAL, maximum=100, mode='determinate', length=200, value=0)
		self.sleep_bar2.pack(side=RIGHT, expand=YES, padx=1, pady=1, fill=ttk.BOTH)

		self.update_manga_buttons()
		#self.menu_list()

		self.open_manga_list = ttk.Menubutton(self.leftleft_subframe_buttonsMain, text="Open URL", bootstyle=(DARK, OUTLINE))
		self.open_manga_list.pack(side=LEFT, padx=5, pady=5)
		self.create_menu_open_url()

##################################################################################################################
	#todo doesnt work
#	def create_menu_refresh(self):
#		tts("eek")
#
#		# read data from file
#		with open('data.txt', 'r') as f:
#			self.data = [line.strip() for line in f.readlines()]
#
#		# clear old menu
#		self.menu.delete(0, tk.END)
#
#		# add new options to menu
#		for option in self.data:
#			self.menu.add_radiobutton(label=option, value=option, variable=self.option_var, command=self.on_option_select)

	def create_menu_open_url(self):
		#refresh open url menu
		self.open_manga_list.config(menu="")

		# read the data from the JSON file into a Python dictionary
		with open('data.json', 'r') as f:
			data = json.load(f)

		# create the menu
		menu = tk.Menu(self.open_manga_list, tearoff=False)
		for title in data.keys():
			url = data[title]['url']
			menu.add_command(label=title, command=lambda u=url: (webbrowser.open_new_tab(u[:-2] + str(int(u[-2:])-1)), self.ba.hide_app()))
		# attach the menu to the Menubutton
		self.open_manga_list.config(menu=menu)

	def create_menu(self):
		# Read data from file
		with open('data.txt', 'r') as f:
			self.data = [line.strip() for line in f.readlines()]

		# create menu
		self.menu = ttk.Menu(self.menub)

		# add options
		self.option_var = ttk.StringVar()
		for option in self.data:
			self.menu.add_radiobutton(label=option, value=option, variable=self.option_var, command=self.on_option_select)

		# associate menu with menubutton
		self.menub['menu'] = self.menu
		


	def on_option_select(self):
		selected_option = self.option_var.get()
		self.menu.delete(0, tk.END)  # clear menu
		with open('data.txt', 'r') as f:
			lines = f.readlines()
		with open('data.txt', 'w') as f:
			for line in lines:
				if line.strip() != selected_option:  # exclude selected option
					f.write(line)
		self.create_menu()

		my_scalper = urlScalping()
		my_scalper.update_data_json()

		print(f"{selected_option} is deleted.")
		chatMain.add_log_message(f"{selected_option} is deleted.")
		chatMain.add_log_message("")
		tts("Deleted!")

		###############################
		#refresh open url menu
		self.open_manga_list.config(menu="")

		# read the data from the JSON file into a Python dictionary
		with open('data.json', 'r') as f:
			data = json.load(f)

		# create the menu
		menu = tk.Menu(self.open_manga_list, tearoff=False)
		for title in data.keys():
			url = data[title]['url']
			menu.add_command(label=title, command=lambda u=url: (webbrowser.open_new_tab(u[:-2] + str(int(u[-2:])-1)), self.ba.hide_app()))
		# attach the menu to the Menubutton
		self.open_manga_list.config(menu=menu)



	def on_option_select_refresh(self):
		print("BAAAAAAAAAAAAAAAAAAAAAM")
		#todo del menu refresh and fix single diget in it

########################################
	def start_sleep_bar(self):
		self.create_menu_open_url()
		#tts("test")
		#print(f"{current_time} === progress bar start")
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
		self.create_menu()
		self.create_menu_open_url()

	def start_sleep_bar2(self):
		self.create_menu_open_url()
		#tts("test")
		#print(f"{current_time} === progress bar start")
		# Set the number of steps in the progress bar (e.g. 100 steps for 100%)
		num_steps = 100
		# Calculate the number of seconds for each step
		secs_per_step = sleep_duration2 / num_steps
		# Set the initial progress bar value to 0
		self.sleep_bar2['value'] = 0
		# Update the progress bar every second until it reaches 100%
		for i in range(num_steps):
			self.sleep_bar2.step(1)
			self.sleep_bar2.update()
			time.sleep(secs_per_step)			

	def update_manga_buttons(self):
		manga_names, urls = self.ba.get_last_chapters()

		# Remove existing buttons
		for child in self.left_subframe_buttonsMain.winfo_children():
			child.destroy()

		# Create buttons for each manga and add them to the window
		for i in range(len(manga_names)):
			name = manga_names[i]
			url = urls[i]
			button = ttk.Button(self.left_subframe_buttonsMain, text=name, style=(DARK, OUTLINE), command=lambda url=url: (self.ba.openLastChapterLink(url), self.ba.hide_app()))
			button.pack(side=RIGHT, padx=5, pady=5)
		# Schedule another call to update the manga buttons in 5 seconds
		self.master.after(2000, self.update_manga_buttons)
		#########################################################################################################
	def add_log_message(self, msg):
		self.chatMain.insert(ttk.END, msg + '\n')
		self.chatMain.see(ttk.END)


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

#clear = 1


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

	def update_data_json(self):
		with open("data.json", 'w') as file:
			json.dump(self.manga_dict, file)

	def manga_checker(self):
		while True:
			#pull fresh data from data.txt
			self.manga_dict = self.get_manga_dict()
			manga_is_out = {}
			for key in self.manga_dict:
				url = self.manga_dict[key]['url'].format(self.manga_dict[key]['chapter_number'])
				response = requests.get(url)
				soup = BeautifulSoup(response.content, 'html.parser')
				scalping = soup.find_all('div', {'class': 'c4-small'}) + soup.find_all('span', {'class': 'hrr-name'}) + soup.find_all('div', {'class': 'd-block'}) + soup.find_all('span', {'class': 'inline-block'})
				current_time = datetime.datetime.now().strftime('%H:%M:%S')
				
				#if clear == 1:
				if "Oops! We can't find this page." in str(scalping):
					log_message = f"#{key} chapter number {self.manga_dict[key]['chapter_number']} isn't out yet"
					log_messagetts = f"{key}, chapter number {self.manga_dict[key]['chapter_number']}, isn't out yet"
					print(log_message)
					#chatMain.add_log_message(log_message)
					#tts(log_messagetts)
					debug = 1
				elif "Comments".lower() in str(scalping).lower():
					if key not in manga_is_out:
						manga_is_out[key] = self.manga_dict[key]['chapter_number']
					log_message = f"#{key} Chapter number {self.manga_dict[key]['chapter_number']} IS OUT"
					log_messagetts = f"{key}, IS OUT"
					print(log_message)
					chatMain.add_log_message(log_message)
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
					chatMain.add_log_message(log_message)
					#tts(log_messagetts)
					debug = 5

				#elif clear == 2:
				#	print("clear is:")
				#	print(clear)
				#	debug = 1
			

			#MIN_NUM_NAMES = 2

			#print(debug)
			if debug == 4:
				tts("mangareader is downn")
				print("mangareader is downn")
				chatMain.add_log_message("")
				time.sleep(60)

			if debug == 5:
				tts("error")
				print("	debug = 5 ==error==")
				chatMain.add_log_message("")
				time.sleep(60)

			
			elif debug < 3:
				print(manga_is_out)
				print([self.manga_dict])
				if manga_is_out:
					with open("lastchapter.txt", 'w') as file:
						for key, value in manga_is_out.items():
							file.write(self.manga_dict[key]['url'].format(value) + "\n")

					with open("lastchaptername.txt", 'w') as file:
						for key in manga_is_out.keys():
							file.write(key + "\n")

					with open("lastchaptername.json", 'r') as file:
						manga_names = json.load(file)

					# Add the new manga name to the list if it is unique
					new_manga_name = list(manga_is_out.keys())[0]
					if new_manga_name not in manga_names:
						manga_names.append(new_manga_name)

					# Keep only the last two names in the list
					manga_names = manga_names[-2:]

					with open("lastchaptername.json", 'w') as file:
						json.dump(manga_names, file)

					manga_is_out.clear()

				with open("data.txt", 'w') as file:
					for key in self.manga_dict:
						# Extract the URL prefix by removing the part after "chapter-"
						url_prefix = self.manga_dict[key]['url'][:self.manga_dict[key]['url'].rfind("chapter-")+len("chapter-")]
						# Write the URL with the updated chapter number to the file
						file.write(f"{url_prefix}{self.manga_dict[key]['chapter_number']}\n")
						self.manga_dict[key]['url'] = f"{url_prefix}{self.manga_dict[key]['chapter_number']}"

				with open("data.json", 'w') as file:
					json.dump(self.manga_dict, file)
				
				#log_message_before_sleep = f"====="{current_time}"====="
				#chatMain.add_log_message(f"###> {current_time} <###")
				#chatMain.add_log_message("")

				print("manga_is_out")
				print(manga_is_out)


				#master = tk.Tk()
				#gui = ttkgui(master)
				#gui.self.create_menu()



				#if debug == 2:
					#ttkgui = ttkgui()
					#ttkgui.refresh_del()
					#print("manga_is_out")
					#print(manga_is_out)

				print(f"{current_time} === starting progress bar for {sleep_duration / 60} minutes")
				chatMain.start_sleep_bar()


class GmailChecker():
	def __init__(self):
		self.gmail = Gmail()
		self.construct_query = construct_query

		from variables.TwtichVariables import subject_list

		self.subject_list = subject_list
		#self.subject_list = ["test1", "test2"]
		#self.snippet_list = ["test"]

		# For even more control use queries:
		self.query_params = {
			"labels": ["Twitch"],
			"subject": self.subject_list,
			"newer_than": (12, "hour"), # number of hours it goes in past
			"unread": True
		}

	def extract_first_word(self, subject):
		words = subject.split()
		if words:
			return words[0]
		return None

	def append_to_file(self, file_path, data):
		append = True

		# Check the last modification time of the file
		if os.path.exists(file_path):
			last_modified = os.path.getmtime(file_path)
			current_time = time.time()
			time_diff = current_time - last_modified
			time_diff_minutes = time_diff / 60.0

			# If the last modification was within the last 15 minutes, append to the file
			if time_diff_minutes < 30: # minutes after it will delete everything 
				append = True
			else:
				append = False

		# Read the existing lines from the file
		lines = []
		if append and os.path.exists(file_path):
			with open(file_path, "r") as file:
				lines = file.readlines()

		# Append the new data to the lines
		lines.append(data + "\n")

		# If the number of lines exceeds the maximum, remove the first line
		max_lines = 4 # max lines in .txt files
		if len(lines) > max_lines:
			lines = lines[1:]

		# Write the updated lines to the file
		with open(file_path, "w") as file:
			file.writelines(lines)

	def twitch_live_announcer(self):
		while True:
			try:
				self.messages = self.gmail.get_messages(query=self.construct_query(self.query_params))
			except ssl.SSLEOFError as e:
				print("SSL EOF Error occurred. Retrying...")
				time.sleep(10)  # Wait for some time before retrying
				continue

			for message in self.messages:
				print("Subject:", message.subject)
				print("Snippet:", message.snippet)
				print("-" * 20)
				print()

				# Mark the message as read
				message.mark_as_read()

				# Extract the first word from the subject as the stream username
				stream_username = self.extract_first_word(message.subject)
				if stream_username:
					# Construct the Twitch stream link
					stream_link = f"https://www.twitch.tv/{stream_username}"
					print("Stream Link:", stream_link)

					# Append or overwrite the stream link to lastchapter.txt file
					self.append_to_file("lastchapter.txt", stream_link)

					# Append or overwrite the stream username to lastchaptername.txt file
					self.append_to_file("lastchaptername.txt", stream_username)

				tts(message.subject)
				chatMain.add_log_message(message.subject)
				chatMain.add_log_message("")

				time.sleep(10)

			chatMain.start_sleep_bar2()


def start_threads():
	t1 = threading.Thread(target=icon_tray)
	t1.daemon = True
	t1.start()

	t2 = threading.Thread(target=urlScalping().manga_checker)
	t2.daemon = True
	t2.start()

	t3 = threading.Thread(target=GmailChecker().twitch_live_announcer)
	t3.daemon = True
	t3.start()


def start_threads_tts():
	t7 = threading.Thread(target=hotkey_listener)
	t7.daemon = True
	t7.start()

if __name__ == "__main__":
	root = ttk.Window()
	chatMain = ttkgui(root)
	start_threads()
	start_threads_tts()
	root.mainloop()