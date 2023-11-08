import time, os
import ssl
from simplegmail import Gmail
from simplegmail.query import construct_query
import http.client
import socket

#from modules.GoogleTTS import tts
from modules.SocketClient import Schat
#from modules.SocketClient import Schat2

import save.controlPanel
ProgressBarSleepDuration2 = save.controlPanel.ProgressBarSleepDuration2
MAX_LINES = save.controlPanel.MAX_LINES

from save.twitchfilter import negatives_list
from save.twitchfilter import positives_list


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


		Adjustment = 1
		if ProgressBarSleepDuration2 <= 1:
			Adjustment = 5
		elif ProgressBarSleepDuration2 == 2:
			Adjustment = 2.5
		elif ProgressBarSleepDuration2 == 5:
			Adjustment = 1
		elif ProgressBarSleepDuration2 == 10:
			Adjustment = 0.5
		elif ProgressBarSleepDuration2 >= 20:
			Adjustment = 0.25

		MarkAsRead_IterationNumber = 1200 * Adjustment #480 * 3
		MarkAsReadTimer = ProgressBarSleepDuration2 * MarkAsRead_IterationNumber + ProgressBarSleepDuration2
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
				message2 = message2.replace("!", "")
				message2 = message2.replace(".", "    !")
				message2 = "$tts " + message2
				Schat(message2)


				message = message.snippet
				start_keyword = "is live!"
				end_keyword = "Streaming"

				# Find the first occurrence of the start keyword
				first_start_index = message.rfind(start_keyword)
				#print(f"first_start_index: {first_start_index}")
				if first_start_index != -1:
					# Find the end keyword starting from the second start index
					end_index = message.find(end_keyword, first_start_index + len(start_keyword))
					#print(end_index)
					if end_index != -1:
						#print("1")
						extracted_text = message[first_start_index + len(start_keyword):end_index].strip()
						print(extracted_text)
						Schat(f"{stream_username}: {extracted_text}")
					elif end_index == -1:
						#end_index = 0
						#print(message)
						#print("2")
						extracted_text = message[first_start_index + len(start_keyword):].strip()
						print(extracted_text)
						Schat(f"{stream_username}: {extracted_text}")
					else:
						print("message.snipper to text box error!")
				else:
					print("Start keyword not found.")
				if change_icon == False: 
					time.sleep(1)

				elif change_icon == True:
					#dynamic_icon = threading.Thread(target=.dynamic_icon_alert)
					#dynamic_icon.start()

					#print(threading.active_count())
					#print(threading.enumerate())
					#message = "change_icon_alert"
					Schat("change_icon_alert")
					time.sleep(1)
		



			# unread_eraser logic
			MarkAsReadTimer = MarkAsReadTimer - ProgressBarSleepDuration2
		#	if MarkAsReadTimer < 30:
		#		#Iteration_result(MarkAsReadTimer)
		#		print(f"Will restart at value: 0. Current value is: {MarkAsReadTimer}")
		#		#print(MarkAsReadTimer)
			if MarkAsReadTimer == 0:
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
				message = "RestartingGmailChecker"
				print(message)
				Schat("GmailprocessNone")
				Schat(message)
				break
			#try:


			#todo FIX THIS, it is sending messages nonstop
			message = "StartSleepBar2"
			Schat(message)
			#print("sending")		
			

			#except ConnectionAbortedError:
			#	# Code to handle the ConnectionAbortedError
			#	print("Connection was aborted by the software on the host machine.")
			time.sleep(ProgressBarSleepDuration2 + 0.1)

if __name__ == "__main__":
    checker = GmailChecker()
    checker.twitch_live_announcer()