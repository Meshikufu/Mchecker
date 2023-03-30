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

os.chdir('C:/Users/Kufu/Desktop/pyprojects/MangaChecker')
##################################################################################
def icon_tray():
    image = PIL.Image.open('power.png')
    win = win32gui.GetForegroundWindow()
    def on_clicked(icon, item):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if str(item) == "open console":
            win32gui.ShowWindow(win, win32con.SW_SHOW)
            #print(f"console was opened at the: {current_time}")
        elif str(item) == "hide console":
            win32gui.ShowWindow(win, win32con.SW_HIDE)
            win32api.SetConsoleCtrlHandler(lambda x: True, True)
            #print(f"console was hidden at the: {current_time}")
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


def read_data_txt():
    filename = "data.txt"
    with open(filename, 'r') as file:
        content = file.read()
    lines = content.split("\n")
    chainsaw_man_chapter = int(lines[0].split('=')[1].strip())
    one_punch_man_chapter = int(lines[1].split('=')[1].strip())
    meiou_sama_chapter = int(lines[2].split('=')[1].strip())
    #print(content)
    return chainsaw_man_chapter, one_punch_man_chapter, meiou_sama_chapter


def manga_checker():
    chainsaw_man_chapter, one_punch_man_chapter, meiou_sama_chapter = read_data_txt()
    while True:

        not_found = "Oops! We can't find this page."
        amount_of_manga = 2
        opm = "One-Punch Man"
        cm = "Chainsaw Man"
        ms = "Meiou-sama"

        def url_plus():
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = soup.find_all('div', {'class': 'c4-small'}) + soup.find_all('h2', {'class': 'manga-name'})
            return titles

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        url = f"https://mangareader.to/read/chainsaw-man-96/en/chapter-{chainsaw_man_chapter}"
        titles = url_plus()
        for title in titles:
            if not_found in title.text:
                print(f"    {cm} chapter number {chainsaw_man_chapter} is yet not out ===== {current_time}")
            elif cm in title.text:
                print(f"    {cm} Chapter number {chainsaw_man_chapter} IS OUT")
                playsound('sound2.mp3')
                chainsaw_man_chapter += 1  # increment the current chapter number by 1

        url = f"https://mangareader.to/read/onepunch-man-40/en/chapter-{one_punch_man_chapter}"
        titles = url_plus()
        for title in titles:
            if not_found in title.text:
                print(f"    {opm} chapter number {one_punch_man_chapter} is yet not out ===== {current_time}")
            elif opm in title.text:
                print(f"    {opm} Chapter number {one_punch_man_chapter} IS OUT")
                playsound('sound2.mp3')
                one_punch_man_chapter += 1  # increment the current chapter number by 1 

        url = f"https://mangareader.to/read/meiou-sama-ga-tooru-no-desu-yo-58998/en/chapter-{meiou_sama_chapter}"
        titles = url_plus()
        for title in titles:
            if not_found in title.text:
                print(f"    {ms} chapter number {meiou_sama_chapter} is yet not out ===== {current_time}")
            elif ms in title.text:
                print(f"    {ms} Chapter number {meiou_sama_chapter} IS OUT")
                playsound('sound2.mp3')
                meiou_sama_chapter += 1  # increment the current chapter number by 1 


        print("        checking again...in "+ str(int(40*60/amount_of_manga/60)) +" minutes...")
        time.sleep(40*60/amount_of_manga)
        with open("data.txt", 'w') as file:
            file.write(f"chainsaw_man_chapter = {chainsaw_man_chapter}\n")          
            file.write(f"one_punch_man_chapter = {one_punch_man_chapter}\n")    
            file.write(f"meiou_sama_chapter = {meiou_sama_chapter}\n")    
###################################################
title_thread = threading.Thread(target=manga_checker)
title_thread.start()

t2 = threading.Thread(target=icon_tray)
t2.start()

title_thread.join()
t2.join()
