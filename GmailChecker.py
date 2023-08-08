
import time, os
import ssl
from simplegmail import Gmail
from simplegmail.query import construct_query
import http.client
import socket, threading

#from modules.GoogleTTS import tts
from modules.SocketClient import Schat
from modules.SocketClient import Schat2

import modules.controlPanel
sleep_duration2 = modules.controlPanel.sleep_duration2
MAX_LINES = modules.controlPanel.MAX_LINES

from save.twitchfilter import negatives_list
from save.twitchfilter import positives_list
from save.twitchfilter import positives_list_drinking
from save.twitchfilter import positives_list_collab
from save.twitchfilter import positives_list_irl


class GmailChecker():
	def __init__(self):
		self.gmail = Gmail()
		self.construct_query = construct_query

		self.icon_idle = True
		self.trigger_thread = None

		from save.twitchfilter import subject_list
		from save.twitchfilter import snippet_list

		self.subject_list = subject_list
		self.snippet_list = snippet_list

		self.query_params = {
			"labels": ["Twitch"],
			"exact_phrase": subject_list + snippet_list + positives_list,
			"newer_than": (22, "hour"),
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


		unread_eraser_iterations = 120#480 * 3
		gmail_progressbar_duration = sleep_duration2
		unread_eraser = gmail_progressbar_duration * unread_eraser_iterations + gmail_progressbar_duration
		unread_eraser_base = gmail_progressbar_duration * unread_eraser_iterations
		# unread_eraser logic

		#restarted = True

		#print(threading.active_count())
		#print(threading.enumerate())

		#while True:
			#print(f"START unread_eraser: {unread_eraser}")
		while True:
			try:
				self.messages = ""
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

						

				### filter logic
				change_icon = True

				snippet_lower = message.snippet.lower()

				message.subject = message.subject.replace("_", " ")
				message2 = f"{message.subject}."

				matched_keywords_filter = []

				# Check if any keyword from negatives_list is present in snippet_lower
				if any(keyword.lower() in snippet_lower for keyword in negatives_list):
					matched_keywords_filter.append("Potentially shit ")
					change_icon = False
					print("change_icon = False")

				# Check if any keyword from positives_list is present in snippet_lower
				for keyword in positives_list:
					if keyword.lower() in snippet_lower:
						matched_keywords_filter.append(keyword.capitalize() + ".")

				# Join the matched keywords with space separators and append to message2
				if matched_keywords_filter:
					message2 += " ".join(matched_keywords_filter)
					message2 = message2[:-1]
					message2 += " stream"

				elif not matched_keywords_filter:
					message2 = message2.replace(".", "")
				#self.TTS.tts(message2)
				#TTSgmail = threading.Thread(target=self.TTS.tts, args=(message2,))
				#TTSgmail.start()
				print(message2)
				message2 = message2.replace(".", "    !")
				message2 = "$tts " + message2
				Schat2(message2)
				if change_icon == False: 
					time.sleep(1)

				elif change_icon == True:
					#dynamic_icon = threading.Thread(target=self.tray.dynamic_icon_alert)
					#dynamic_icon.start()
					#self.tray.change_icon('pic/alert.png')
					#print(threading.active_count())
					#print(threading.enumerate())

					time.sleep(1)
		



			# unread_eraser logic
			unread_eraser = unread_eraser - gmail_progressbar_duration
			if unread_eraser == 0:
				unread_eraser = unread_eraser_base
			if unread_eraser == unread_eraser_base:
				#if restarted == False:
				#	#print(threading.active_count())
				#	#print(threading.enumerate())
				#	message = "RestartGmailChecker"
				#	Schat(message)
				#	message = '$tts Restarting GmailChecker'
				#	Schat(message)
				#	print("restarting GmailChecker")
				#	break
				#	
				#restarted = False

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

				#time.sleep(sleep_duration2)


			#print("")
			#print(threading.active_count())
			#print(threading.enumerate())
			time.sleep(2)
			#self.chatMain.start_sleep_bar2()

def start_gmail_checker():
	gmail_checker = GmailChecker()  # Gmail API 
	t4 = threading.Thread(target=gmail_checker.twitch_live_announcer)
	t4.daemon = True
	t4.start()

if __name__ == "__main__":
	start_gmail_checker()