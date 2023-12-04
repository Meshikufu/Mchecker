#from flask import Flask
#from playsound import playsound
import time, datetime, os, threading, webbrowser, pygame, keyboard, subprocess, json
import win32gui, win32con, win32api, win32console
import ttkbootstrap as ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import tkinter as tk
import pyperclip, re
from tkinter import Tk, PhotoImage






#os.chdir('C:/Programming/PythonProjects/Mchecker')

#todo4 this one below doesnt hide message in console
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
print("")
pygame.mixer.init()

clipboardtext = pyperclip.paste()
current_time = datetime.datetime.now().strftime('%H:%M:%S')

from modules.GoogleTTS import TTS
from modules.SocketClient import Schat
#from modules.GmailChecker import GmailChecker
from modules.IconTray import IconTray
from modules.urlScalping import urlScalping
#from modules.socketserverM import socketServer
#from modules.socketserverM import socketServerAndroid
from gBot.gPriceCheckerModule import PriceChecker
from bot.ss import SS_OfferChecker
from modules.GoogleTTSv2 import TTSv2


import save.controlPanel
ProgressBarSleepDuration = save.controlPanel.ProgressBarSleepDuration
ProgressBarSleepDuration2 = save.controlPanel.ProgressBarSleepDuration2
MAX_LINES = save.controlPanel.MAX_LINES
geometry_starting_positiong = save.controlPanel.geometry_starting_position
gPriceChecker_Is_On = save.controlPanel.gPriceChecker_Is_On
TopRowButtons_Activation = save.controlPanel.top_row_buttons





def on_hotkey():

	# get the text from the clipboard
	copytext = pyperclip.paste()

	# convert the text to speech
	TTS.tts(copytext)


def hotkey_listener():
	# register the hotkey
	keyboard.add_hotkey('alt+t', on_hotkey)

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
	def __init__(self, master, tray, chatMain, TTS):
		self.TTS = TTS
		self.chatMain = chatMain
		self.tray = tray
		self.master = master
		root.title("Mchecker")
		root.geometry(geometry_starting_positiong)
		# Remove the top bar
		root.overrideredirect(True)
		# Make the window stay on top of other windows
		root.attributes('-topmost', True)

		self.ConsoleCondition = False


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

		if TopRowButtons_Activation is True:
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

		if TopRowButtons_Activation is True:
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

			my_scalper = urlScalping(tray, chatMain, TTS)
			my_scalper.update_data_json()

			self.create_menu()
			print(f"{clipboard_content} is added")
			message = (f"{clipboard_content} is added")
			Schat(message) # print to chatbox
			#chatMain.add_log_message(f"{clipboard_content} is added!")
			#chatMain.add_log_message("")
			message = "Added!"
			Schat(message) # tts signal
			#self.TTS.tts("added!")

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

		if TopRowButtons_Activation is True:
			self.b1 = ttk.Button(self.right_subframe_buttonsMainUp, text="Add url", bootstyle=SUCCESS, command=append_clipboard_to_file)    #lambda: [append_clipboard_to_file(), start_sleep_bar()])
			self.b1.pack(side=LEFT, padx=5, pady=5)

		####
		self.us = urlScalping(tray, chatMain, TTS)

		if TopRowButtons_Activation is True:
			self.menub = ttk.Menubutton(self.right_subframe_buttonsMainUp, text="Delete", bootstyle=DANGER)
			self.menub.pack(side=LEFT, padx=5, pady=5)
			self.create_menu()

#		self.br = ttk.Button(self.right_subframe_buttonsMainDown, text="refresh", bootstyle=DANGER, commaand=self.create_menu_refresh())
#		self.br.pack(side=LEFT, padx=5, pady=5)
#
#
		def exit_app():
			global Gmailprocess  # Use the global process variable
			if Gmailprocess is not None:  # Check if the subprocess was started
				Gmailprocess.terminate()
			root.destroy()

		self.exit = ttk.Button(self.right_subframe_buttonsMainDown, text="Exit", bootstyle=(DANGER, OUTLINE), command=exit_app)
		self.exit.pack(side=LEFT, padx=5, pady=5)

		self.hide = ttk.Button(self.leftleft_subframe_buttonsMainDown, text="Hide", bootstyle=(DANGER, OUTLINE), command=self.ba.hide_app)
		self.hide.pack(side=LEFT, padx=5, pady=5)

		self.console = ttk.Button(self.leftleft_subframe_buttonsMainDown, text="Terminal", bootstyle=(INFO,OUTLINE), command=self.console_button)
		self.console.pack(side=LEFT, padx=5, pady=5)

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

		if TopRowButtons_Activation is True:
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
	def console_button(self):
		self.console = win32console.GetConsoleWindow()
		win32gui.ShowWindow(self.console, 0)
		win32api.SetConsoleCtrlHandler(lambda x: True, True)
		if self.ConsoleCondition == False:
			win32gui.ShowWindow(self.console, win32con.SW_SHOW)
			self.ConsoleCondition = True
		else:
			win32gui.ShowWindow(self.console, 0)
			win32api.SetConsoleCtrlHandler(lambda x: True, True)
			self.ConsoleCondition = False

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

	def on_option_select(self): # delete button fuction
		selected_option = self.option_var.get()
		self.menu.delete(0, tk.END)  # clear menu
		with open('temp/Mdata.txt', 'r') as f:
			lines = f.readlines()
		with open('temp/Mdata.txt', 'w') as f:
			for line in lines:
				if line.strip() != selected_option:  # exclude selected option
					f.write(line)
		self.create_menu()

		my_scalper = urlScalping(tray, chatMain, TTS)
		my_scalper.update_data_json()

		print(f"{selected_option} is deleted.")
		chatMain.add_log_message(f"{selected_option} is deleted.")
		chatMain.add_log_message("")
		message = "Deleted!"
		Schat(message)
		#self.TTS.tts("Deleted!")

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

		# todo MEMORY LEAK below
		#self.create_menu_open_url()

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

		# todo MEMORY LEAK below
		#self.create_menu()
		#self.create_menu_open_url()

	def start_sleep_bar2(self): # gmail progress bar
		#self.create_menu_open_url()
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

#########################################################################################################
#########################################################################################################
#from modules.ttkgui import ttkgui



import socket
#from modules.SocketClient import Schat
#from modules.GoogleTTS import tts
from save.myip import myip


def tts_thread(message):
    TTS.tts(message)

def socketServer(tray, chatMain, TTS):
	global Gmailprocess 
	chatMain = chatMain
	tray = tray
	HOST = socket.gethostname()
	PORT = 1235

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5)

	print("Socket server started successfully!")

	def start_sleep_bar2_daemon():
		chatMain.start_sleep_bar2()

	while True:
		clientsocket, address = s.accept()
		#print(f"Connection from {address} has been established!")

		# Receive the message from the client
		message = clientsocket.recv(1024).decode("utf-8")
		#print(message)
		#print("this was message above")
#
		if message != "StartSleepBar2" and message != "change_icon_alert":

			print(f"socketServer-Received message: {message}")

		if message == "change_icon_alert":
			tray.change_icon('pic/alert.png')
		elif message == "start_sleep_bar2":
			chatMain.start_sleep_bar2()	
		elif message == "Added!" or message == "Deleted!":
			TTS.tts(message)
		elif message == "GmailprocessNone":
			Gmailprocess = None
		elif message == "KillSubprocessGmail":
			if Gmailprocess is not None:  # Check if the subprocess was started
				Gmailprocess.terminate()
			root.destroy()
		elif message == "RestartingGmailChecker":
			time.sleep(5)
			Gmail_Checker()
		#elif message == "StartSleepBar2":
		#	chatMain.start_sleep_bar2()
		elif message == "StartSleepBar2":
			threadSleepBar2 = threading.Thread(target=start_sleep_bar2_daemon)
			threadSleepBar2.daemon = True  # Set the thread as a daemon thread
			threadSleepBar2.start()
			#print("starting")
			#print(current_time)
		elif "$tts" in message:
			message = message.replace("$tts ", "")
			message = message.replace(".", " point ")
			ttsThread = threading.Thread(target=tts_thread, args=(message,))
			ttsThread.daemon = True  # Set the thread as a daemon thread
			ttsThread.start()
		elif "#tts" in message:
			message = message.replace("#tts ", "")
			message = message.replace(".", " point ")
			TTS.tts(message)	
			chatMain.add_log_message(message)
			chatMain.add_log_message("")
		else:
			#TTS.tts(message)
			chatMain.add_log_message(message)
			chatMain.add_log_message("")

		# Process the received message as needed
		clientsocket.close()


def socketServerTTS():
	HOST = socket.gethostname()
	PORT = 1279

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5)

	print("Socket server TTS started successfully!")
	while True:
		clientsocket, address = s.accept()
		message = clientsocket.recv(1024).decode("utf-8")

		print(f"TTS socketServer-Received message: {message}")

		if message is not None and message.strip() != "":
			if "$tts" in message:
				message = message.replace("$tts ", "")
			TTSv2(message)

		clientsocket.close()




def socketServerAndroid(tray, chatMain, TTS):
	chatMain = chatMain
	tray = tray
	HOST = myip #socket.gethostname()
	PORT = 59621

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(5)

	print("Socket server for Android started successfully!")

	while True:
		clientsocket, address = s.accept()
		print(f"Connection from {address} has been established!")

		# Receive the message from the client
		message = clientsocket.recv(1024).decode("utf-8")

		print(f"socketServerAndroid-Received message: {message}")
		print(message)

		if message == "AndroidSignal":
			TTS.tts("Android signal recieved!")
		# $tts Package is ready for pickup!
		elif message is not None and message.strip() != "":
			if "$tts" in message:
				message = message.replace("$tts ", "")
			TTSv2(message)
		

		# Process the received message as needed
		clientsocket.close()


def start_threads():
	tray = IconTray(root)  # Icon in tray

	def icon_tray_thread():
		tray.icon.run()

	t1 = threading.Thread(target=icon_tray_thread)
	t1.daemon = True
	t1.start()

	url_scalping = urlScalping(tray, chatMain, TTS)  # mandagex scalping
	t3 = threading.Thread(target=url_scalping.manga_checker)
	t3.daemon = True
	t3.start()

	#gmail_checker = GmailChecker(tray, chatMain, TTS)  # Gmail API 
	#t4 = threading.Thread(target=gmail_checker.twitch_live_announcer)
	#t4.daemon = True
	#t4.start()

	tSocketServer = threading.Thread(target=socketServer, args=(tray, chatMain, TTS,))
	tSocketServer.daemon = True
	tSocketServer.start()

	tSocketServerTTS = threading.Thread(target=socketServerTTS)
	tSocketServerTTS.daemon = True
	tSocketServerTTS.start()

	tSocketServerAndroid = threading.Thread(target=socketServerAndroid, args=(tray, chatMain, TTS,))
	tSocketServerAndroid.daemon = True
	tSocketServerAndroid.start()

	if gPriceChecker_Is_On is True:
		PriceCheckerThread = threading.Thread(target=PriceChecker)
		PriceCheckerThread.daemon = True
		PriceCheckerThread.start()

	ssBot = threading.Thread(target=SS_OfferChecker)
	ssBot.daemon = True
	ssBot.start()

	from bot.pingRouter import PingMonitor
	ping_monitor_instance = PingMonitor()
	PingRouter = threading.Thread(target=ping_monitor_instance.ping_router)
	PingRouter.daemon = True
	PingRouter.start()


def start_threads_tts():
	t7 = threading.Thread(target=hotkey_listener)
	t7.daemon = True
	t7.start()


def Gmail_Checker():
    global Gmailprocess  # Use the global process variable
    script_path = "GmailChecker.py"
    Gmailprocess = subprocess.Popen(["python", script_path]) 
	# to kill process: Schat("StartSleepBar2")

someValue = True
if __name__ == "__main__":
	TTS = TTS()
	root = ttk.Window()
	tray = IconTray(root)
	chatMain = ttkgui(root, tray, TTS, someValue) 
	start_threads()
	start_threads_tts()
	Gmail_Checker()



	root.mainloop()