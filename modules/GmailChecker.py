from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

import http.client
import socket
import time, os, json, ssl, re, html
import win32gui

from modules.AudioModules import playAudio
from modules.SocketClient import Schat
from modules.GoogleTTSv2 import TTSv2
from modules.logger import error_logger

import save.controlPanel
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

            lines = []
            if append and os.path.exists(file_path):
                with open(file_path, "r") as file:
                    lines = file.readlines()

            lines = [line for line in lines if line.strip() != data] # remove match if exists
            lines.append(data + "\n")

            if len(lines) > MAX_LINES: # Number of maximum links
                lines = lines[1:]

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

    def removeEmojiFromText(text):
        # Emoji ranges taken from https://unicode.org/Public/emoji/13.1/emoji-sequences.txt
        emoji_pattern = re.compile(
            "["
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+"
        )
        return emoji_pattern.sub(r' ', text)
    
    def cleanSnippet(message):
        #if "is live as a guest on" in message:
        start_keyword = "is live!"

        start_indices = [i for i in range(len(message)) if message.startswith(start_keyword, i)]
        if len(start_indices) >= 2:
            second_occurrence = start_indices[1] + len(start_keyword)
            message = message[second_occurrence:].strip()

        if not start_indices: ### guest 
            start_keyword = "stream!"
            index = message.find("stream!")
            message = message[index + len("stream!"):]
            print(start_indices)

        end_index = message.rfind("streaming")
        if end_index == -1:
            end_index = message.rfind("watch now or click this link:")
        print(f'end_index is:{end_index}')
        if end_index != -1:
            message = message[:end_index].strip()

        return message


    # Build the Gmail service
    service = build('gmail', 'v1', credentials=creds)

    ProgressBarSleepDuration2 = save.controlPanel.ProgressBarSleepDuration2

    while True:
        try:
            refresh_twitchJson_variables()
            query_words = subject_list_twitchJson + snippet_list_twitchJson + positives_list_twitchJson
            query_words = [f'"{word}"' if " " in word else word for word in query_words]
            query = f'label:Twitch is:unread newer_than:1d {" OR ".join(query_words)}'

            try:
                messages = search_emails(service, query)
            except ssl.SSLEOFError as e:
                print("SSL EOF Error occurred. Retrying...")
                time.sleep(3)
                continue
            except http.client.RemoteDisconnected as remote_disconnected_error:
                print("Remote Disconnected Error occurred. Retrying...")
                time.sleep(3)
                continue
            except socket.gaierror as gai_error:
                print("getaddrinfo failed. Retrying...")
                time.sleep(3)
                continue
            except Exception as e:
                if str(e).startswith("Exception in Thread (twitch_live_announcer)"):
                    print("Exception occurred in Thread (twitch_live_announcer)")
                    time.sleep(3)
                    continue

            if messages:
                for message in messages:
                    msg_details = service.users().messages().get(userId="me", id=message["id"], format="full", metadataHeaders=None).execute()
                    snippet = msg_details.get('snippet', '')
                    snippet = html.unescape(snippet)
                    headers=msg_details["payload"]["headers"]
                    subject= [i['value'] for i in headers if i["name"]=="Subject"] 
                    subject = subject[0]

                    print(subject)
                    print(snippet)
                    snippet = snippet.lower()

                    mark_as_read(service, 'me', message['id'])

                    stream_username = extract_first_word(subject)
                    stream_link = f"https://www.twitch.tv/{stream_username}"

                    append_to_file("temp/lastLink.txt", stream_link)
                    append_to_file("temp/lastName.txt", stream_username)

                    snippet = cleanSnippet(snippet)

                    # filter block / adding words
                    change_icon = True
                    matched_keywords_filter = []
                    negatives = []
                    positives = []
                    if any(keyword.lower() in snippet for keyword in negatives_list_twitchJson):
                        negatives.append("Potentially shit. ")
                        change_icon = False
                    for keyword in positives_list_twitchJson:
                        if keyword.lower() in snippet:
                            matched_keywords_filter.append(keyword.capitalize())
                    if matched_keywords_filter:
                        positives += matched_keywords_filter
                    
                    print(positives)
                    print(negatives)

                    if find_chrome_window(stream_username) is None:
                        if change_icon == False: 
                            time.sleep(1)
                        elif change_icon == True:
                            Schat("change_icon_alert")
                            time.sleep(1)

                        snippet = snippet.replace("_", " ")
                        snippet = removeEmojiFromText(snippet)
                        snippetCleanupPatterns = [r'\s*!\w+', r'\s*#\w+', r'\s*\|+\s*', r'\s*\-+\s*', r'[^\x00-\x7F]', r'\btts\b', r'\b\d+bits\b', r'\s+'] # '!word' '#word' '|' '-' 'any non english' 'num+bits' 'remove word "bits"' 'only single space'
                        for pattern in snippetCleanupPatterns:
                            snippet = re.sub(pattern, ' ', snippet)

                        if positives:
                            if snippet.endswith(" "):
                                snippet = snippet[:-1]
                            if snippet.endswith("!"):
                                pass
                            else:
                                snippet += '. '
                            for word in positives:
                                snippet += " " + word
                            snippet += " stream!"
                        if negatives:
                            print("test")
                            print(snippet)
                            print(negatives)
                            snippet = str(negatives) + str(snippet)

                        snippet = f'{stream_username} is live! ' + snippet
                        Schat(snippet)
                        TTSv2(snippet)
                    else:
                        playAudio('gun.mp3')
                        time.sleep(1)
                        continue

            message = "StartSleepBar2"
            Schat(message)
            if ProgressBarSleepDuration2 <= 5:
                ProgressBarSleepDuration2 = 5
            time.sleep(ProgressBarSleepDuration2 + 0.1)
        except Exception as e:
            print(e)
            TTSv2("Gmail broke!")

            error_logger()