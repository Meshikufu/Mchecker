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
import sys
import os
import pystray
import PIL.Image
import time
from tqdm import tqdm

#os.chdir('C:/Users/Kufu/Desktop/pyprojects/MangaChecker')


def icon_tray():
    image = PIL.Image.open('power.png')
    win = win32gui.GetForegroundWindow()
    def on_clicked(icon, item):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if str(item) == "open console":
            win32gui.ShowWindow(win, win32con.SW_SHOW)
        elif str(item) == "hide console":
            win32gui.ShowWindow(win, win32con.SW_HIDE)
            win32api.SetConsoleCtrlHandler(lambda x: True, True)
        elif str(item) == "Exit":
            icon.stop()  
            os._exit(0)

    icon = pystray.Icon("power", image)
    icon.menu = pystray.Menu(
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


manga_dict = {
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


def manga_checker(manga_dict):
    while True:        
        for key in manga_dict:
            url = manga_dict[key]["url"].format(manga_dict[key]["chapter"])
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            scalping = soup.find_all('div', {'class': 'c4-small'}) + soup.find_all('h2', {'class': 'manga-name'}) + soup.find_all('div', {'class': 'd-block'})

            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if "Oops! We can't find this page." in str(scalping):
                print(key, "chapter number", manga_dict[key]["chapter"], "is yet not out =====", current_time)
            elif key.lower() in str(scalping).lower():    
                print(key, "Chapter number", manga_dict[key]["chapter"],  "IS OUT")
                playsound('sound2.mp3')
                manga_dict[key]["chapter"] += 1  # increment the current chapter number by 1
            else:
                print(key, "Chapter number", manga_dict[key]["chapter"],  "IS OUT       ERROR")
                playsound('sound2.mp3')
                manga_dict[key]["chapter"] += 1  # increment the current chapter number by 1    
        
        print("  checking again...")
        time.sleep(1)
        duration = 20 * 60
        for i in tqdm(range(duration), desc=f"  in {int(duration/60)} minutes", bar_format='{l_bar}{bar}|'):
            time.sleep(1)
        print("        ")
        time.sleep(duration)
        with open("data.txt", 'w') as file:
            for key in manga_dict:
                file.write(manga_dict[key]["data_name"] + "=" + str(manga_dict[key]["chapter"]) + "\n")

        

#########################
t1 = threading.Thread(target=manga_checker, args=(manga_dict,))
t2 = threading.Thread(target=icon_tray)

t1.start()
t2.start()

t1.join()
t2.join()
