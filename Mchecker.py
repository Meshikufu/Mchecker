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
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as tk
import pygame
import webbrowser
import keyboard
import pyperclip, re, sqlite3
#from gtts import gTTS
#import pyautogui, queue, tempfile
from tkinter import Tk, PhotoImage
import json
#gmail stuff below
import ssl
from simplegmail import Gmail
from simplegmail.query import construct_query
import http.client
import subprocess, yt_whisper
import socket




#os.chdir('C:/Programming/PythonProjects/Mchecker')

#todo4 this one below doesnt hide message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
print("")
pygame.mixer.init()



#todo5 add controller class that will contains reusable variables
sleep_duration = 15 * 40# * 60			#manga
sleep_duration2 = 15 * 2				#twitch
MAX_LINES = 4  # Define the maximum number of lines in gui (name of last scapped thing)

clipboardtext = pyperclip.paste()
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
		with open("temp/lastName.txt", 'r') as file:
			manga_names = [line.strip() for line in file.readlines()]

		with open("temp/lastLink.txt", 'r') as file:
			urls = file.read().split("\n")

		return manga_names, urls


############################################################################################################
############################################################################################################
class ttkgui():
	def __init__(self, master, tray):
		self.tray = tray
		self.master = master
		root.title("Mchecker")
		root.geometry("+700+500")
		# Remove the top bar
		root.overrideredirect(True)
		# Make the window stay on top of other windows
		root.attributes('-topmost', True)


		# Function to handle window dragging
		def start_drag(event):
			root.x = event.x
			root.y = event.y

		def stop_drag(event):
			root.x = None
			root.y = None

		def drag(event):
			deltax = event.x - root.x
			deltay = event.y - root.y
			x = root.winfo_x() + deltax
			y = root.winfo_y() + deltay
			root.geometry(f"+{x}+{y}")

		root.bind("<ButtonPress-1>", start_drag)
		root.bind("<ButtonRelease-1>", stop_drag)
		root.bind("<B1-Motion>", drag)
		
		self.ba = buttons_actions()

		self.top_frame_buttonsMain = ttk.Frame(self.master)#, bootstyle="secondary")
		self.top_frame_buttonsMain.pack(side=TOP, fill=X)#, expand=YES)

		###
		self.top_frame_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMain)#, bootstyle="secondary")
		self.top_frame_buttonsMainUp.pack(side=TOP, fill=X)#, expand=YES)

		self.leftleft_subframe_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMainUp, padding=0)
		self.leftleft_subframe_buttonsMainUp.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.left_subframe_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMainUp)#, bootstyle="info")
		self.left_subframe_buttonsMainUp.pack(side=LEFT, fill=tk.X, expand=True)

		self.right_subframe_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMainUp)#, bootstyle="warning")
		self.right_subframe_buttonsMainUp.pack(side=RIGHT)

		###
		self.top_frame_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMain)#, bootstyle="secondary")
		self.top_frame_buttonsMainDown.pack(side=BOTTOM, fill=X)#, expand=YES)

		self.leftleft_subframe_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMainDown, padding=0)
		self.leftleft_subframe_buttonsMainDown.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.right_subframe_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMainDown)#, bootstyle="warning")
		self.right_subframe_buttonsMainDown.pack(side=RIGHT)

		self.left_subframe_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMainDown)#, bootstyle="info")
		self.left_subframe_buttonsMainDown.pack(side=RIGHT, fill=tk.X, expand=True)

		#########################################################################################################
		def yt_whisper_setup(url, model, task, language):
			desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
			command = f'yt_whisper {url} --model {model} --task {task} --language {language}'
			subprocess.Popen(command, cwd=desktop_path, creationflags=subprocess.CREATE_NEW_CONSOLE)
			#subprocess.Popen(command, cwd=desktop_path, creationflags=subprocess.CREATE_NEW_CONSOLE | win32con.SW_MINIMIZE)

		def YT_whisper_medium():
			copytext = pyperclip.paste()
			if "https://www.youtube.com/watch" in copytext:
				yt_whisper_setup(copytext, "medium", "translate", "Japanese")
				root.withdraw()
			else:
				print("Not a YouTube URL.")

		self.subs = ttk.Button(self.right_subframe_buttonsMainUp, text="YTsubs", bootstyle=DANGER, command=YT_whisper_medium)
		self.subs.pack(side=LEFT, padx=5, pady=5)
		#########################################################################################################
		#def YT_whisper_large():
		#	copytext = pyperclip.paste()
		#	if "https://www.youtube.com/watch" in copytext:
		#		yt_whisper_setup(copytext, "large", "translate", "Japanese")
		#		root.withdraw()
		#	else:
		#		print("Not a YouTube UR_l.")
		#
		#self.subs = ttk.Button(self.right_subframe_buttonsMainUp, text="yt_wisperL", bootstyle=DANGER, command=YT_whisper_large)
		#self.subs.pack(side=LEFT, padx=5, pady=5)
		##########################################################################################################
		import ctypes		
		def launch_translation():
			copytext = pyperclip.paste()
			if "youtube.com/watch" in copytext or "twitch.tv/" in copytext:
				translation_command = f'python translator.py {copytext} --model medium --task translate --language Japanese'
				cmd_command = f'cd /d "C:\\Users\\Kufu\\stream-translator" & {translation_command}'
				subprocess.Popen(f'start cmd /K "{cmd_command}"', shell=True)

				hwnd = ctypes.windll.kernel32.GetConsoleWindow()
				if hwnd != 0:
					ctypes.windll.user32.ShowWindow(hwnd, 0)  # Hide the console window
				root.withdraw()
			else:
				print("Not a Stream URL.")


		self.streamTranslator = ttk.Button(self.right_subframe_buttonsMainUp, text="translation.py", bootstyle=DANGER, command=launch_translation)
		self.streamTranslator.pack(side=LEFT, padx=5, pady=5)
		##########################################################################################################

		def append_clipboard_to_file():
			clipboard_content = pyperclip.paste()
			# Extract the chapter number from the URL
			chapter_num = re.search(r'chapter-(\d+)', clipboard_content).group(1)
			# Add 1 to the chapter number and create the new URL
			new_url = re.sub(r'chapter-\d+', f'chapter-{int(chapter_num)+1}', clipboard_content)
			with open("temp/Mdata.txt", "a") as f:
				f.write(new_url + "\n")

			my_scalper = urlScalping(tray)
			my_scalper.update_data_json()

			self.create_menu()
			print(f"{clipboard_content} is added")
			chatMain.add_log_message(f"{clipboard_content} is added!")
			chatMain.add_log_message("")
			tts("added!")

			#refresh open url menu
			self.open_manga_list.config(menu="")

			# read the data from the JSON file into a Python dictionary
			with open('temp/Mdata.json', 'r') as f:
				data = json.load(f)

			# create the menu
			menu = tk.Menu(self.open_manga_list, tearoff=False)
			for title in data.keys():
				url = data[title]['url']
				menu.add_command(label=title, command=lambda u=url: (webbrowser.open_new_tab(u[:-2] + str(int(u[-2:])-1)), self.ba.hide_app()))
			# attach the menu to the Menubutton
			self.open_manga_list.config(menu=menu)

		self.b1 = ttk.Button(self.right_subframe_buttonsMainUp, text="Add url", bootstyle=SUCCESS, command=append_clipboard_to_file)    #lambda: [append_clipboard_to_file(), start_sleep_bar()])
		self.b1.pack(side=LEFT, padx=5, pady=5)
		#########################################################################################################
		self.us = urlScalping(tray)

		self.menub = ttk.Menubutton(self.right_subframe_buttonsMainUp, text="Delete", bootstyle=DANGER)
		self.menub.pack(side=LEFT, padx=5, pady=5)
		self.create_menu()

#		self.br = ttk.Button(self.right_subframe_buttonsMainDown, text="refresh", bootstyle=DANGER, commaand=self.create_menu_refresh())
#		self.br.pack(side=LEFT, padx=5, pady=5)
#
#
		def exit_app():
			root.destroy()

		self.exit = ttk.Button(self.leftleft_subframe_buttonsMainDown, text="Exit", bootstyle=(DANGER, OUTLINE), command=exit_app)
		self.exit.pack(side=LEFT, padx=5, pady=5)

		self.hide = ttk.Button(self.right_subframe_buttonsMainDown, text="Hide", bootstyle=(DANGER, OUTLINE), command=self.ba.hide_app)
		self.hide.pack(side=RIGHT, padx=5, pady=5)

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

		self.open_manga_list = ttk.Menubutton(self.leftleft_subframe_buttonsMainUp, text="Open URL", bootstyle=(DARK, OUTLINE))
		self.open_manga_list.pack(side=LEFT, padx=5, pady=5)
		self.create_menu_open_url()

##################################################################################################################
	#todo doesnt work
#	def create_menu_refresh(self):
#		tts("eek")
#
#		# read data from file
#		with open('temp/Mdata.txt', 'r') as f:
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
		with open('temp/Mdata.json', 'r') as f:
			data = json.load(f)

		# create the menu
		menu = tk.Menu(self.open_manga_list, tearoff=False)
		for title in data.keys():
			url = data[title]['url']
			menu.add_command(label=title, command=lambda u=url: (webbrowser.open_new_tab(u[:-2] + str(int(u[-2:])-1)), self.ba.hide_app()))
		# attach the menu to the Menubutton
		self.open_manga_list.config(menu=menu)


#	def create_menu_open_url(self):
#		# Destroy the existing menu
#		if hasattr(self, "menu"):
#			self.menu.destroy()
#
#		# Read the data from the JSON file into a Python dictionary
#		with open('temp/Mdata.json', 'r') as f:
#			data = json.load(f)
#
#		# Create the menu
#		menu = tk.Menu(self.open_manga_list, tearoff=False)
#		for title in Mdata.keys():
#			url = data[title]['url']
#			menu.add_command(label=title, command=lambda u=url: (webbrowser.open_new_tab(u[:-2] + str(int(u[-2:])-1)), self.ba.hide_app()))
#
#		# Attach the menu to the Menubutton
#		self.open_manga_list.config(menu=menu)
#
#		# Store the menu reference
#		self.menu = menu	

	def create_menu(self):
		# Read data from file
		with open('temp/Mdata.txt', 'r') as f:
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
		with open('temp/Mdata.txt', 'r') as f:
			lines = f.readlines()
		with open('temp/Mdata.txt', 'w') as f:
			for line in lines:
				if line.strip() != selected_option:  # exclude selected option
					f.write(line)
		self.create_menu()

		my_scalper = urlScalping(tray)
		my_scalper.update_data_json()

		print(f"{selected_option} is deleted.")
		chatMain.add_log_message(f"{selected_option} is deleted.")
		chatMain.add_log_message("")
		tts("Deleted!")

		###############################
		#refresh open url menu
		self.open_manga_list.config(menu="")

		# read the data from the JSON file into a Python dictionary
		with open('temp/Mdata.json', 'r') as f:
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
		for child in self.left_subframe_buttonsMainDown.winfo_children():
			child.destroy()

		# Create buttons for each manga and add them to the window
		for i in range(len(manga_names)):
			name = manga_names[i]
			url = urls[i]
			button = ttk.Button(self.left_subframe_buttonsMainDown, text=name, style=(DARK, OUTLINE), command=lambda url=url: (self.ba.openLastChapterLink(url), self.ba.hide_app()))
			button.pack(side=RIGHT, padx=5, pady=5)
		# Schedule another call to update the manga buttons in 5 seconds
		self.master.after(2000, self.update_manga_buttons)
		#########################################################################################################
	def add_log_message(self, msg):
		self.chatMain.insert(ttk.END, msg + '\n')
		self.chatMain.see(ttk.END)


############################################################################################################
############################################################################################################
class IconTray:
	def __init__(self):
		self.image = PIL.Image.open('pic/web.png')
		self.current_icon = 'web'
		
		self.console = win32console.GetConsoleWindow()
		win32gui.ShowWindow(self.console, 0)
		win32api.SetConsoleCtrlHandler(lambda x: True, True)
		
		self.icon = pystray.Icon("web", self.image)
		self.icon.menu = pystray.Menu(
			pystray.MenuItem('1', self.action, default=True, visible=False),
			pystray.MenuItem("open app", self.on_clicked),
			pystray.MenuItem("hide app", self.on_clicked),
			pystray.MenuItem("open console", self.on_clicked),
			pystray.MenuItem("hide console", self.on_clicked),
			pystray.MenuItem("Exit", self.on_clicked)
		)
	
	def on_clicked(self, icon, item):
		current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		if str(item) == "open console":
			win32gui.ShowWindow(self.console, win32con.SW_SHOW)
		elif str(item) == "hide console":
			win32gui.ShowWindow(self.console, 0)
			win32api.SetConsoleCtrlHandler(lambda x: True, True)
		elif str(item) == "open app":
			root.deiconify()
		elif str(item) == "hide app":
			root.withdraw()
		elif str(item) == "Exit":
			root.destroy()

	def change_icon(self, new_icon_path):
		self.icon.icon = PIL.Image.open(new_icon_path)
		self.current_icon = new_icon_path
		self.icon.update_menu()

	def action(self, icon, item):
		self.change_icon('pic/web.png')
		root.deiconify()


############################################################################################################
############################################################################################################
class urlScalping():
	def __init__(self, tray):
		self.tray = tray
		# initialize manga dictionary with data from Mdata.txt
		self.manga_dict = self.get_manga_dict()
	def get_manga_dict(self):
		with open('temp/Mdata.txt') as f:
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
		with open("temp/Mdata.json", 'w') as file:
			json.dump(self.manga_dict, file)

	def manga_checker(self):
		while True:
			#pull fresh data from Mdata.txt
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
					#print(log_message) #log
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
					chatMain.add_log_message("")
					tts(log_messagetts)
					self.manga_dict[key]['chapter_number'] += 1  # increment the current chapter number by 1
					self.tray.change_icon('pic/alert.png')
					time.sleep(3)
					debug = 2
				elif "Bad gateway".lower() in str(scalping):
					debug = 4

				else:
					log_message = f"{key} Chapter number {self.manga_dict[key]['chapter_number']} scalping ERROR"
					log_messagetts = f"{key}, Chapter number {self.manga_dict[key]['chapter_number']}, scalping ERROR"
					print(log_message)
					#chatMain.add_log_message(log_message)
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
				#tts("error")
				print("	debug = 5 ==error==")
				#chatMain.add_log_message("")
				time.sleep(60)

			
			elif debug < 3:
				if manga_is_out:
					# Write the URLs to the "temp/lastLink.txt" file
					with open("temp/lastLink.txt", 'r') as file:
						lines = file.readlines()
						
					# Check if the number of lines exceeds the maximum
					if len(lines) >= MAX_LINES:
						# Remove the first line
						#chatMain.add_log_message("remove first mana line")
						lines.pop(0)
						
					with open("temp/lastLink.txt", 'w') as file:
						for key, value in manga_is_out.items():
							lines.append(self.manga_dict[key]['url'].format(value) + "\n")
						file.writelines(lines)
					
					# Write the keys to the "lastName.txt" file
					with open("temp/lastName.txt", 'r') as file:
						keys = file.readlines()
						
					# Check if the number of lines exceeds the maximum
					if len(keys) >= MAX_LINES:
						# Remove the first line
						keys.pop(0)
						
					with open("temp/lastName.txt", 'w') as file:
						for key in manga_is_out.keys():
							keys.append(key + "\n")
						file.writelines(keys)

					manga_is_out.clear()

				with open("temp/Mdata.txt", 'w') as file:
					for key in self.manga_dict:
						# Extract the URL prefix by removing the part after "chapter-"
						url_prefix = self.manga_dict[key]['url'][:self.manga_dict[key]['url'].rfind("chapter-")+len("chapter-")]
						# Write the URL with the updated chapter number to the file
						file.write(f"{url_prefix}{self.manga_dict[key]['chapter_number']}\n")
						self.manga_dict[key]['url'] = f"{url_prefix}{self.manga_dict[key]['chapter_number']}"

				with open("temp/Mdata.json", 'w') as file:
					json.dump(self.manga_dict, file)
				
				#log_message_before_sleep = f"====="{current_time}"====="
				#chatMain.add_log_message(f"###> {current_time} <###")
				#chatMain.add_log_message("")

				#print("manga_is_out") #log
				#print(manga_is_out) #log


				#master = tk.Tk()
				#gui = ttkgui(master)
				#gui.self.create_menu()



				#if debug == 2:
					#ttkgui = ttkgui()
					#ttkgui.refresh_del()
					#print("manga_is_out")
					#print(manga_is_out)

				#print(f"{current_time} === starting progress bar for {sleep_duration / 60} minutes") #log
				chatMain.start_sleep_bar()


############################################################################################################
############################################################################################################
class GmailChecker():
	def __init__(self, tray):
		self.tray = tray
		self.gmail = Gmail()
		self.construct_query = construct_query

		from variables.TwtichVariables import subject_list
		from variables.TwtichVariables import snippet_list

		self.subject_list = subject_list
		self.snippet_list = snippet_list

		self.query_params = {
			"labels": ["Twitch"],
			"exact_phrase": self.subject_list + self.snippet_list,
			"newer_than": (21, "hour"), # number of hours it goes in past
			"unread": True
		}

		self.query_params_clear = {
			"labels": ["Twitch"],
			"newer_than": (2, "day"), # number of days it goes in past
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
			if time_diff_minutes < (12 * 60): # minutes after it will delete everything 
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
		if len(lines) > MAX_LINES:
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
			except http.client.RemoteDisconnected as remote_disconnected_error:
				print("Remote Disconnected Error occurred. Retrying...")
				time.sleep(10)  # Wait for some time before retrying
				continue
			except socket.gaierror as gai_error:
				print("getaddrinfo failed. Retrying...")
				time.sleep(10)  # Wait for some time before retrying
				continue
			except Exception as e:
				if str(e).startswith("Exception in thread Thread-4 (twitch_live_announcer)"):
					print("Exception occurred in thread Thread-4 (twitch_live_announcer)")
					time.sleep(10)
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

					if stream_link in open("temp/lastLink.txt").read():
						pass  # Skip execution if stream_link is already present in the file
					else:
						# Append the stream_link to lastLink.txt file
						self.append_to_file("temp/lastLink.txt", stream_link)

						#stream_username = stream_username.replace("_", " ")

						# Append the stream_username to lastName.txt file
						self.append_to_file("temp/lastName.txt", stream_username)

					# Change the icon to alert icon
					self.tray.change_icon('pic/alert.png')
					
				message.subject = message.subject.replace("_", " ")
				tts(message.subject)
				chatMain.add_log_message(message.subject)
				chatMain.add_log_message("")

				time.sleep(10)

			execution_percentage = 3  # Adjust the percentage as desired
			import random
			if random.randint(1, 100) <= execution_percentage:
				try:
					self.messages = self.gmail.get_messages(query=self.construct_query(self.query_params_clear))
				except ssl.SSLEOFError as e:
					print("SSL EOF Error occurred. Retrying...")
					time.sleep(10)  # Wait for some time before retrying
					continue
				except http.client.RemoteDisconnected as remote_disconnected_error:
					print("Remote Disconnected Error occurred. Retrying...")
					time.sleep(10)  # Wait for some time before retrying
					continue
				except socket.gaierror as gai_error:
					print("getaddrinfo failed. Retrying...")
					time.sleep(10)  # Wait for some time before retrying
					continue
				except Exception as e:
					if str(e).startswith("Exception in thread Thread-4 (twitch_live_announcer)"):
						print("Exception occurred in thread Thread-4 (twitch_live_announcer)")
						time.sleep(10)
						continue
				for message in self.messages:
					# Mark the message as read or perform other actions as needed
					message.mark_as_read()

			chatMain.start_sleep_bar2()


def start_threads():
	tray = IconTray()  # Create an instance of IconTray

	def icon_tray_thread():
		tray.icon.run()

	t1 = threading.Thread(target=icon_tray_thread)
	t1.daemon = True
	t1.start()

	url_scalping = urlScalping(tray)
	t2 = threading.Thread(target=url_scalping.manga_checker)
	t2.daemon = True
	t2.start()

	gmail_checker = GmailChecker(tray)  # Pass the tray instance to GmailChecker
	t3 = threading.Thread(target=gmail_checker.twitch_live_announcer)
	t3.daemon = True
	t3.start()

def start_threads_tts():
	t7 = threading.Thread(target=hotkey_listener)
	t7.daemon = True
	t7.start()

if __name__ == "__main__":
	root = ttk.Window()
	tray = IconTray()
	chatMain = ttkgui(root, tray)
	start_threads()
	start_threads_tts()
	root.mainloop()