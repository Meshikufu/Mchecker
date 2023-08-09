from playsound import playsound
import time, datetime
import win32gui, win32con, win32api, win32console
import pystray
import PIL.Image


class IconTray():
	def __init__(self, root):
		self.root = root
		self.image = PIL.Image.open('pic/web.png')
		self.current_icon = 'web'


		self.icon_list_alarm = ['pic/alert.png', 'pic/alert2.png']
		self.icon_list_idle = ['pic/web.png']

		self.icon_idle = True
		
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
			self.root.deiconify()
		elif str(item) == "hide app":
			self.root.withdraw()
		elif str(item) == "Exit":
			self.root.destroy()

	def change_icon(self, new_icon_path):
		self.icon.icon = PIL.Image.open(new_icon_path)
		self.current_icon = new_icon_path
		self.icon.update_menu()

	def action(self, icon, item):
		self.root.deiconify()
		self.icon_idle = True
		time.sleep(0.1)
		self.change_icon(self.icon_list_idle[0])
	
	def dynamic_icon_alert(self):
		if self.icon_idle == True:
			self.icon_idle = False
			while not self.icon_idle:
				for alarm in self.icon_list_alarm:
					if self.icon_idle == True:
						break
					self.change_icon(alarm)
					time.sleep(0.3)


#	def dynamic_icon_alert(self):
#		if self.icon_idle == True:
#			self.icon_idle = False
#			while True:
#				for alarm in self.icon_list_alarm:
#					if self.icon_idle == False:
#						self.change_icon(alarm)
#						time.sleep(0.3)
#					elif self.icon_idle == True:
#						break








#	def dynamic_icon_alert_function(self):
#		#if self.icon_idle == False:
#		#	self.icon_idle = True
#		#	time.sleep(0.35)
#		self.icon_idle = False
#
#		method = 2
#
#		if method == 1:
#			while True:
#				if self.icon_idle == True:
#					break
#				self.change_icon('pic/alert.png')
#				time.sleep(0.3)
#				if self.icon_idle == True:
#					break
#				self.change_icon('pic/alert2.png')
#				time.sleep(0.3)
#
#		if method == 2:
#			while not self.icon_idle:
#				for alarm in self.icon_list_alarm:
#					if self.icon_idle == True:
#						break
#					self.change_icon(alarm)
#					time.sleep(0.3)


					

#todo why this shit not working???
#	def dynamic_icon_alert(self):
#		if self.icon_idle == False:
#			self.icon_idle = True
#			#self.change_icon(self.icon_list_alarm[0])
#			#print("first pass")
#			time.sleep(0.35)
#		self.icon_idle = False
#		self.icon_list_alarm = ['pic/alert.png', 'pic/alert2.png']
#		while True:
#			for alarm in self.icon_list_alarm:
#				if self.icon_idle == True:
#					#self.change_icon(self.icon_list_idle[0])
#					break
#				self.change_icon(alarm)
#				time.sleep(0.3)



