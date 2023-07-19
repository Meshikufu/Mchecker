
import time, os
import ssl
from simplegmail import Gmail
from simplegmail.query import construct_query
import http.client
import socket

from modules.GoogleTTS import tts
from modules.Schatboxsendmessage import Schatboxsendmessage
from modules.Schatboxsendmessage import Schat2

import modules.constrolPanel
sleep_duration2 = modules.constrolPanel.sleep_duration2
MAX_LINES = modules.constrolPanel.MAX_LINES

class GmailChecker():
	def __init__(self, tray, chatMain):
		self.chatMain = chatMain
		self.tray = tray
		self.gmail = Gmail()
		self.construct_query = construct_query

		from save.TwtichVariables import subject_list
		from save.TwtichVariables import snippet_list

		self.subject_list = subject_list
		self.snippet_list = snippet_list

		self.query_params = {
			"labels": ["Twitch"],
			"exact_phrase": subject_list + snippet_list,
			"newer_than": (21, "hour"),
			"unread": True
		}

		self.query_params_clear = {
			"labels": ["Twitch"],
			"newer_than": (2, "day"),
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
			if time_diff_minutes < (21 * 60): # minutes after it will delete everything 
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
		HOST = socket.gethostname()
		PORT = 1235


		unread_eraser_iterations = 120
		gmail_progressbar_duration = sleep_duration2
		unread_eraser = gmail_progressbar_duration * unread_eraser_iterations + gmail_progressbar_duration
		unread_eraser_base = gmail_progressbar_duration * unread_eraser_iterations
		# unread_eraser logic

		while True:
			try:
				self.messages = self.gmail.get_messages(query=self.construct_query(self.query_params))
			except ssl.SSLEOFError as e:
				print("SSL EOF Error occurred. Retrying...")
				time.sleep(10)
				continue
			except http.client.RemoteDisconnected as remote_disconnected_error:
				print("Remote Disconnected Error occurred. Retrying...")
				time.sleep(10)
				continue
			except socket.gaierror as gai_error:
				print("getaddrinfo failed. Retrying...")
				time.sleep(10)
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
				if "#ad" in message.snippet:
					tts(f"{message.subject} . Sellout stream")

					message2 = (f"{message.subject} #Sellout stream")
					Schat2(message2)

				else:
					tts(message.subject)

					message2 = (message.subject)
					Schat2(message2)

				time.sleep(10)

			# unread_eraser logic
			unread_eraser = unread_eraser - gmail_progressbar_duration
			if unread_eraser == 0:
				unread_eraser = unread_eraser_base
			if unread_eraser == unread_eraser_base:
				try:
					self.messages = self.gmail.get_messages(query=self.construct_query(self.query_params_clear))
				except ssl.SSLEOFError as e:
					print("SSL EOF Error occurred. Retrying...")
					time.sleep(10)
					continue
				except http.client.RemoteDisconnected as remote_disconnected_error:
					print("Remote Disconnected Error occurred. Retrying...")
					time.sleep(10)
					continue
				except socket.gaierror as gai_error:
					print("getaddrinfo failed. Retrying...")
					time.sleep(10)
					continue
				except Exception as e:
					if str(e).startswith("Exception in thread Thread-4 (twitch_live_announcer)"):
						print("Exception occurred in thread Thread-4 (twitch_live_announcer)")
						time.sleep(10)
						continue
				for message in self.messages:
					# Mark the message as read or perform other actions as needed
					message.mark_as_read()


			self.chatMain.start_sleep_bar2()