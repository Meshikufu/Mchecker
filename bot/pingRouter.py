import subprocess
import os
import time
from datetime import datetime
import sqlite3
import pygame
from modules.SocketClient import Schat
import save.controlPanel

pygame.mixer.init()

class PingMonitor:
    def __init__(self):
        self.router_ip = save.controlPanel.router_ip
        self.success = None
        self.success_google = None
        self.success_youtube = None
        self.success_reddit = None
        self.google_result = None
        self.youtube_result = None
        self.reddit_result = None
        self.sleepTimer = None

    def play_bell_sound(self):
        sound_folder = "sounds"
        sound_file = "bell.wav"
        sound_path = os.path.join(sound_folder, sound_file)

        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    def record_ping_result(self, success, error_message, ping_result, success_google, success_youtube, success_reddit, ethernetDown):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Create a new SQLite connection and cursor
        conn = sqlite3.connect('bot/ping_results.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ping_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                destination TEXT,
                success INTEGER,
                error_message TEXT,
                ping_result TEXT,
                google INTEGER,
                youtube INTEGER,
                reddit INTEGER,
                ethernetDown INTEGER
            )
        ''')
        conn.commit()

        cursor.execute('''
            INSERT INTO ping_results (timestamp, destination, success, error_message, ping_result, google, youtube, reddit, ethernetDown)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (current_time, self.router_ip, success, error_message, ping_result, success_google, success_youtube, success_reddit, ethernetDown))
        conn.commit()

        # Close the SQLite connection
        conn.close()

    def ping_router(self):
        print("Starting pingRouter")

        while True:
            try:
                try:
                    self.counting = 0
                    self.success_google = 0
                    self.success_youtube = 0
                    self.success_reddit = 0

                    # Move the loop inside the try block
                    result = subprocess.run(["ping", self.router_ip, "-n", "1", "-w", "1000", "-l", "32"],
                                            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    self.google_result = subprocess.run(["ping", "google.com", "-n", "1", "-w", "1000", "-l", "16"],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    self.youtube_result = subprocess.run(["ping", "youtube.com", "-n", "1", "-w", "1000", "-l", "16"],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    self.reddit_result = subprocess.run(["ping", "reddit.com", "-n", "1", "-w", "1000", "-l", "16"],
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                    # Find the line starting with "Reply from"
                    reply_line = next((line for line in result.stdout.split('\n') if line.startswith("Reply from")), None)

                    if reply_line:
                        ping_result_line = reply_line
                        self.success = 1
                        self.counting + 1
                        error_message = None
                    elif "Destination host unreachable." in result.stdout:
                        self.success = 0
                        error_message = "Destination host unreachable"
                        ping_result_line = result.stdout
                        self.play_bell_sound()
                    else:
                        self.success = 0
                        error_message = "No valid reply line found"
                        ping_result_line = result.stdout
                        self.play_bell_sound()

                    # Check the success of pinging Google, YouTube, and Reddit
                    self.success_google = 1 if "Reply from" in self.google_result.stdout else 0
                    self.success_youtube = 1 if "Reply from" in self.youtube_result.stdout else 0
                    self.success_reddit = 1 if "Reply from" in self.reddit_result.stdout else 0

                    self.counting = self.counting + self.success_google + self.success_youtube + self.success_reddit
                    if self.counting >= 2:
                        ethernetDown = False
                    elif self.counting == 0:
                        ethernetDown = True
                    else:
                        ethernetDown = True


                    # Record the ping results in the database
                    self.record_ping_result(self.success, error_message, ping_result_line, self.success_google, self.success_youtube, self.success_reddit, ethernetDown)

                    self.sleepTimer = 1

                except subprocess.CalledProcessError as e:
                    self.counting = 0
                    #self.play_bell_sound() 
                    # Access attributes that are guaranteed to be defined
                    
                    try:
                        google_result = "EMPTY"
                        google_result = subprocess.run(["ping", "google.com", "-n", "1", "-w", "1000", "-l", "16"],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    except Exception as e1:
                        continue
                    try:
                        youtube_result = "EMPTY"
                        youtube_result = subprocess.run(["ping", "youtube.com", "-n", "1", "-w", "1000", "-l", "16"],
                                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    except Exception as e2:
                        continue
                    try:
                        reddit_result = "EMPTY"
                        reddit_result = subprocess.run(["ping", "reddit.com", "-n", "1", "-w", "1000", "-l", "16"],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    except Exception as e3:
                        continue
                    
                    success_google = 1 if "Reply from" in google_result.stdout else 0
                    success_youtube = 1 if "Reply from" in youtube_result.stdout else 0
                    success_reddit = 1 if "Reply from" in reddit_result.stdout else 0

                    self.counting = self.counting + success_google + success_youtube + success_reddit

                    if self.counting >= 2:
                        ethernetDown = False
                        Schat(f"FAKE Router ping problems (date: {current_time})")
                    elif self.counting == 0:
                        ethernetDown = True
                        self.play_bell_sound()
                        Schat(f"Router ping problems (date: {current_time})")
                        Schat("change_icon_alert")
                    else:
                        ethernetDown = True
                        self.play_bell_sound()
                        Schat(f"Router ping problems (date: {current_time})")
                        Schat("change_icon_alert")

                    # self.play_bell_sound()
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    #Schat(f"Router ping problems (date: {current_time})")
                    #Schat("change_icon_alert")

                    # Record the failed ping result in the database with additional details
                    self.record_ping_result(0, str(e), e.stdout, google_result.stdout, youtube_result.stdout, reddit_result.stdout, ethernetDown)

                    self.sleepTimer(0.2)
            except Exception as e:
                continue

            time.sleep(self.sleepTimer)
