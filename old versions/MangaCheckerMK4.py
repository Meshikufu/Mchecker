from flask import Flask
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import time
import datetime
import threading
import win32gui
import win32con
import win32api
import win32console
import sys
import os
import pystray
import PIL.Image
import time
from tqdm import tqdm
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk


os.chdir('C:\Users\Kufu\Desktop\Mchecker')


class Mathtest():
    def mmath(self):
        big = 23
        small = 3
        if big >= small:
            print("success")
            gui.add_log_message("test.")

class gui:
    def __init__(self, master):
        self.master = master


        self.frame = ttk.Frame(self.master)
        self.frame.pack(side=TOP)

        self.mt = Mathtest()
        self.b1 = ttk.Button(self.frame, text="Button 1", bootstyle=SUCCESS, command=self.mt.mmath)
        self.b1.pack(side=LEFT, padx=5, pady=10)

        self.b2 = ttk.Button(self.frame, text="Button 2", bootstyle=WARNING)
        self.b2.pack(side=LEFT, padx=5, pady=10)

        self.b3 = ttk.Button(self.frame, text="Button 3", bootstyle=WARNING)
        self.b3.pack(side=LEFT, padx=5, pady=10)

        self.gui = ttk.Text(self.master, height=15, width=70)
        self.gui.pack(side=LEFT, fill=ttk.BOTH, expand=True)
        
        #self.add_log_message("Starting program...")
        #self.add_log_message("Loading data...")
        #self.add_log_message("Done.")

    def add_log_message(self, msg):
        self.gui.insert(ttk.END, msg + '\n')
        self.gui.see(ttk.END)

def icon_tray():
    image = PIL.Image.open('power.png')
    win = win32gui.GetForegroundWindow()
    console = win32console.GetConsoleWindow()
    win32gui.ShowWindow(console ,0)
    win32api.SetConsoleCtrlHandler(lambda x: True, True)  
    
    def on_clicked(icon, item):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if str(item) == "open console":
            win32gui.ShowWindow(console, win32con.SW_SHOW)
        elif str(item) == "hide console":
            win32gui.ShowWindow(console ,0)
            win32api.SetConsoleCtrlHandler(lambda x: True, True)     
        elif str(item) == "open app":
            win32gui.ShowWindow(win, win32con.SW_SHOW)
            win32gui.ShowWindow(console, win32con.SW_SHOW)
            win32gui.ShowWindow(console ,0)
            win32api.SetConsoleCtrlHandler(lambda x: True, True)
        elif str(item) == "hide app":
            win32gui.ShowWindow(win, win32con.SW_HIDE)
            win32api.SetConsoleCtrlHandler(lambda x: True, True)      
        elif str(item) == "Exit":
            icon.stop()  
            os._exit(0)

    icon = pystray.Icon("power", image)
    icon.menu = pystray.Menu(
        pystray.MenuItem("open app", on_clicked),
        pystray.MenuItem("hide app", on_clicked),
        pystray.MenuItem("open console", on_clicked),
        pystray.MenuItem("hide console", on_clicked),
        pystray.MenuItem("Exit", on_clicked)
    )       
    icon.run() 

with open('data.txt', 'r') as file:
            for line in file:
                key, value = line.split('=')
                key = key.strip()
                value = value.strip()
                exec(f"{key} = {value}")


class urlScalping():
    def __init__(self):
        self.manga_dict = {
            "Chainsaw man": {
                "url": "https://mangareader.to/read/chainsaw-man-96/en/chapter-{}",
                "chapter": chainsaw_man_chapter,
                "data_name": "chainsaw_man_chapter"
            },
            "one-punch man": {
                "url": "https://mangareader.to/read/onepunch-man-40/en/chapter-{}",
                "chapter": one_punch_man_chapter,
                "data_name": "one_punch_man_chapter"
            },
            "Meiou-sama": {
                "url": "https://mangareader.to/read/meiou-sama-ga-tooru-no-desu-yo-58998/en/chapter-{}",
                "chapter": meiou_sama_chapter,
                "data_name": "meiou_sama_chapter"
            }
        }

    def manga_checker(self):
        while True:
            for key in self.manga_dict:
                url = self.manga_dict[key]["url"].format(self.manga_dict[key]["chapter"])
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                scalping = soup.find_all('div', {'class': 'c4-small'}) + soup.find_all('h2', {'class': 'manga-name'}) + soup.find_all('div', {'class': 'd-block'})

                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if "Oops! We can't find this page." in str(scalping):
                    print(key, "chapter number", self.manga_dict[key]["chapter"], "is yet not out =====", current_time)
                    log_message1 = f"{key} chapter number {self.manga_dict[key]['chapter']} is yet not out ===== {current_time}"
                    gui.add_log_message(log_message1)
                elif key.lower() in str(scalping).lower():
                    print(key, "Chapter number", self.manga_dict[key]["chapter"],  "IS OUT")
                    log_message2 = f"{key} Chapter number {self.manga_dict[key]['chapter']} IS OUT"
                    gui.add_log_message(log_message2)
                    playsound('sounds/sound2.mp3')
                    self.manga_dict[key]["chapter"] += 1  # increment the current chapter number by 1
                else:
                    print(key, "Chapter number", self.manga_dict[key]["chapter"],  "scalping ERROR")
                    log_message3 = f"{key} Chapter number {self.manga_dict[key]['chapter']} scalping ERROR"
                    gui.add_log_message(log_message3)
                    playsound('sounds/sound2.mp3')
                    self.manga_dict[key]["chapter"] += 1  # increment the current chapter number by 1

            print("  checking again...")
            print("  in 20 mintues...")
            gui.add_log_message("waiting 20 minutes until next check...")
            gui.add_log_message("")
            time.sleep(1)
            duration = 20 * 60
            for i in tqdm(range(duration), desc=f"  in {int(duration/60)} minutes", bar_format='{l_bar}{bar}|'):
                time.sleep(1)
            print("        ")
            time.sleep(duration)
            with open("data.txt", 'w') as file:
                for key in self.manga_dict:
                    file.write(self.manga_dict[key]["data_name"] + "=" + str(self.manga_dict[key]["chapter"]) + "\n")


def start_threads():
    t1 = threading.Thread(target=urlScalping().manga_checker)
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=icon_tray)
    t2.daemon = True
    t2.start()


if __name__ == "__main__":
    root = ttk.Window()
    gui = gui(root)
    start_threads()
    root.mainloop()


                     
        




#def start_threads():
#    us = urlScalping()
#    t1 = threading.Thread(target=us.manga_checker, args=(self.manga_dict,))
#    t1.daemon = True
#    t1.start()
#
#    t2 = threading.Thread(target=icon_tray)
#    t2.daemon = True
#    t2.start()
#
#if __name__ == "__main__":
#    root = ttk.Window()
#    gui = gui(root)
#    start_threads()
#    root.mainloop()
#