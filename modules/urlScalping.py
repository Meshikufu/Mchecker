import requests
from bs4 import BeautifulSoup
import time, datetime
import json


from modules.GoogleTTS import tts

import modules.controlPanel
sleep_duration = modules.controlPanel.sleep_duration
sleep_duration2 = modules.controlPanel.sleep_duration2
MAX_LINES = modules.controlPanel.MAX_LINES


class urlScalping():
	def __init__(self, tray, chatMain):
		self.chatMain = chatMain
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

				try:
					response = requests.get(url)
					
				except requests.exceptions.ConnectionError as e:
					print("Error: Failed to establish a connection. Check your internet connection and try again.")
					print("Exception:", e)
					time.sleep(10)
					continue  # Skip to the next iteration
				except Exception as e:
					if str(e).startswith("Exception in thread Thread-3 (manga_checker)"):
						print("Exception occurred in thread Thread-3 (manga_checker)")
						time.sleep(10)
						continue


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
					self.chatMain.add_log_message(log_message)
					self.chatMain.add_log_message("")
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
				self.chatMain.add_log_message("")
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
				self.chatMain.start_sleep_bar()
