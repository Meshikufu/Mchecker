from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import http.client
import socket
import time, os, json, ssl
import win32gui

from modules.AudioModules import playAudio
from modules.SocketClient import Schat
from modules.GoogleTTSv2 import TTSv2

import save.controlPanel
ProgressBarSleepDuration2 = save.controlPanel.ProgressBarSleepDuration2
MAX_LINES = save.controlPanel.MAX_LINES



def TwitchList_json():
	with open('save/twitchfilter.json') as f:
		twitch_list_json = json.load(f)
	return twitch_list_json

def refresh_twitchJson_variables(): # variables are getting refreshed but querry params are not f
    global subject_list_twitchJson, snippet_list_twitchJson, negatives_list_twitchJson, positives_list_twitchJson
    LIST = TwitchList_json()
    subject_list_twitchJson = LIST['subject_list']
    snippet_list_twitchJson = LIST['snippet_list']
    negatives_list_twitchJson = LIST['negatives_list']
    positives_list_twitchJson = LIST['positives_list']


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def load_credentials(token_path):
    if os.path.exists(token_path):
        with open(token_path, 'r') as token_file:
            creds_data = json.load(token_file)
            creds = Credentials(
                token=creds_data['access_token'],
                refresh_token=creds_data['refresh_token'],
                token_uri=creds_data['token_uri'],
                client_id=creds_data['client_id'],
                client_secret=creds_data['client_secret'],
                scopes=creds_data['scopes']
            )
            return creds
    return None

def search_emails(service, query):
    """Search for emails using the given query."""
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages

def get_email_details(service, msg_id):
    """Get the details of a specific email."""
    message = service.users().messages().get(userId='me', id=msg_id).execute()
    return message

def twitch_live_announcer():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    token_path = 'gmail_token.json'
    client_secret_path = 'client_secret.json'

    creds = load_credentials(token_path) # Load if it exists

    # If no valid credentials are available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open(token_path, 'w') as token_file:
            json.dump({
                'access_token': creds.token,
                'refresh_token': creds.refresh_token,
                'token_uri': creds.token_uri,
                'client_id': creds.client_id,
                'client_secret': creds.client_secret,
                'scopes': creds.scopes
            }, token_file)

    def extract_first_word(subject):
        words = subject.split()
        if words:
            return words[0]
        return None

    def append_to_file(file_path, data):
        append = True

        if os.path.exists(file_path): # Check the last modification time of the file
            last_modified = os.path.getmtime(file_path)
            current_time = time.time()
            time_diff = current_time - last_modified
            time_diff_minutes = time_diff / 60.0

            if time_diff_minutes < (41 * 60): # minutes after it will delete everything 
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

    def mark_as_read(service, user_id, msg_id):
        """Mark a message as read."""
        service.users().messages().modify(
            userId=user_id,
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

    def find_chrome_window(window_title):
        chrome_handle = None
        top_windows = []
        win32gui.EnumWindows(lambda hwnd, top_windows: top_windows.append((hwnd, win32gui.GetWindowText(hwnd))), top_windows)
        for hwnd, window_text in top_windows:
            if window_title in window_text:
                chrome_handle = hwnd
                break
        return chrome_handle


    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)


    while True:
        refresh_twitchJson_variables()
        query_words = subject_list_twitchJson + snippet_list_twitchJson + positives_list_twitchJson
        query_words = [f'"{word}"' if " " in word else word for word in query_words]
        query = f'label:Twitch is:unread newer_than:1d {" OR ".join(query_words)}'

        try:
            messages = search_emails(service, query)
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
            if str(e).startswith("Exception in Thread (twitch_live_announcer)"):
                print("Exception occurred in Thread (twitch_live_announcer)")
                time.sleep(10)
                continue

        if messages:
            for message in messages:
                msg_details = service.users().messages().get(userId="me", id=message["id"], format="full", metadataHeaders=None).execute()
                snippet = msg_details.get('snippet', '')
                headers=msg_details["payload"]["headers"]
                subject= [i['value'] for i in headers if i["name"]=="Subject"] 
                subject = subject[0]

                print(subject)
                print(snippet)
                snippet = snippet.lower()

                mark_as_read(service, 'me', message['id'])

                stream_username = extract_first_word(subject)
                stream_link = f"https://www.twitch.tv/{stream_username}"
                if stream_link in open("temp/lastLink.txt").read():
                    pass
                else:
                    append_to_file("temp/lastLink.txt", stream_link)
                    append_to_file("temp/lastName.txt", stream_username)

                # clean up snippet
                start_keyword = "is live!"
                end_keyword = "streaming"
                start_index = snippet.find(start_keyword)
                if start_index != -1:
                    snippet = snippet[start_index:]
                    second_index = snippet.find(start_keyword, start_index + 1)
                    if start_index != -1:
                        snippet = snippet[second_index:]
                    snippet = stream_username + " " + snippet
                    end_index = snippet.find(end_keyword)
                    if end_index != -1:
                        snippet = snippet[:end_index]

                # filter block / adding words
                change_icon = True
                subjectTTS = subject.replace("_", "")
                matched_keywords_filter = []
                if any(keyword.lower() in snippet for keyword in negatives_list_twitchJson):
                    subjectTTS = "Potentially shit. " + subjectTTS
                    change_icon = False
                for keyword in positives_list_twitchJson:
                    if keyword.lower() in snippet:
                        matched_keywords_filter.append(keyword.capitalize() + ".")
                if matched_keywords_filter:
                    subjectTTS += " ".join(matched_keywords_filter)
                    subjectTTS = subjectTTS[:-1]
                    subjectTTS += " stream"

                print(stream_username)
                if find_chrome_window(stream_username) is None:
                    if change_icon == False: 
                        time.sleep(1)
                    elif change_icon == True:
                        Schat("change_icon_alert")
                        time.sleep(1)
                    Schat(snippet)
                    TTSv2(subjectTTS)
                else:
                    playAudio('gun.mp3')
                    time.sleep(1)
                    continue

        message = "StartSleepBar2"
        Schat(message)
        time.sleep(ProgressBarSleepDuration2 + 0.1)