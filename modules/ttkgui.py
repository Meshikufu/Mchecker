from flask import Flask
from playsound import playsound
import time, datetime, os, threading, webbrowser, keyboard, subprocess, json
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as tk
import pyperclip, re, sqlite3
from tkinter import Tk, PhotoImage

from modules.GoogleTTS import tts

import modules.constrolPanel
ProgressBarSleepDuration = modules.constrolPanel.ProgressBarSleepDuration
ProgressBarSleepDuration2 = modules.constrolPanel.ProgressBarSleepDuration2
MAX_LINES = modules.constrolPanel.MAX_LINES


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
	def __init__(self, master, tray, chatMain, url_scalping):
		urlScalping = url_scalping
		self.chatMain = chatMain
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

		################
		self.top_frame_buttonsMain = ttk.Frame(self.master)#, bootstyle="secondary")
		self.top_frame_buttonsMain.pack(side=TOP, fill=X)#, expand=YES)

		### button section UP
		self.top_frame_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMain)#, bootstyle="secondary")
		self.top_frame_buttonsMainUp.pack(side=TOP, fill=X)#, expand=YES)

		self.leftleft_subframe_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMainUp, padding=0)
		self.leftleft_subframe_buttonsMainUp.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.left_subframe_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMainUp)#, bootstyle="info")
		self.left_subframe_buttonsMainUp.pack(side=LEFT, fill=tk.X, expand=True)

		self.right_subframe_buttonsMainUp = ttk.Frame(self.top_frame_buttonsMainUp)#, bootstyle="warning")
		self.right_subframe_buttonsMainUp.pack(side=RIGHT)

		###	button section DOWN
		self.top_frame_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMain)#, bootstyle="secondary")
		self.top_frame_buttonsMainDown.pack(side=BOTTOM, fill=X)#, expand=YES)

		self.leftleft_subframe_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMainDown, padding=0)
		self.leftleft_subframe_buttonsMainDown.pack(side=LEFT, fill=ttk.BOTH, expand=True)

		self.right_subframe_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMainDown)#, bootstyle="warning")
		self.right_subframe_buttonsMainDown.pack(side=RIGHT)

		self.left_subframe_buttonsMainDown = ttk.Frame(self.top_frame_buttonsMainDown)#, bootstyle="info")
		self.left_subframe_buttonsMainDown.pack(side=RIGHT, fill=tk.X, expand=True)

		########
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

		########
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

		########
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

		########
		def append_clipboard_to_file():
			clipboard_content = pyperclip.paste()
			# Extract the chapter number from the URL
			chapter_num = re.search(r'chapter-(\d+)', clipboard_content).group(1)
			# Add 1 to the chapter number and create the new URL
			new_url = re.sub(r'chapter-\d+', f'chapter-{int(chapter_num)+1}', clipboard_content)
			with open("temp/Mdata.txt", "a") as f:
				f.write(new_url + "\n")

			my_scalper = urlScalping(tray, chatMain)
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

		####
		self.us = urlScalping(tray, chatMain)

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
##################################################################################################################
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

	def on_option_select(self, url_scalping): # delete button fuction
		urlScalping = url_scalping
		selected_option = self.option_var.get()
		self.menu.delete(0, tk.END)  # clear menu
		with open('temp/Mdata.txt', 'r') as f:
			lines = f.readlines()
		with open('temp/Mdata.txt', 'w') as f:
			for line in lines:
				if line.strip() != selected_option:  # exclude selected option
					f.write(line)
		self.create_menu()

		my_scalper = urlScalping(chatMain)
		my_scalper.update_data_json()

		print(f"{selected_option} is deleted.")
		chatMain.add_log_message(f"{selected_option} is deleted.")
		chatMain.add_log_message("")
		tts("Deleted!")

		####
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

######################################## progress bar triggers
	def start_sleep_bar(self): # manga progress bar
		self.create_menu_open_url()
		#tts("test")
		#print(f"{current_time} === progress bar start")
		# Set the number of steps in the progress bar (e.g. 100 steps for 100%)
		num_steps = 100
		# Calculate the number of seconds for each step
		secs_per_step = ProgressBarSleepDuration / num_steps
		# Set the initial progress bar value to 0
		self.sleep_bar['value'] = 0
		# Update the progress bar every second until it reaches 100%
		for i in range(num_steps):
			self.sleep_bar.step(1)
			self.sleep_bar.update()
			time.sleep(secs_per_step)
		self.create_menu()
		self.create_menu_open_url()

	def start_sleep_bar2(self): # gmail progress bar
		self.create_menu_open_url()
		#tts("test")
		#print(f"{current_time} === progress bar start")
		# Set the number of steps in the progress bar (e.g. 100 steps for 100%)
		num_steps = 100
		# Calculate the number of seconds for each step
		secs_per_step = ProgressBarSleepDuration2 / num_steps
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
	def add_log_message(self, msg): # function to pass text into chat box
		self.chatMain.insert(ttk.END, msg + '\n')
		self.chatMain.see(ttk.END)
someValue = True
if __name__ == "__main__":
	root = ttk.Window()
	chatMain = ttkgui(root, someValue) 