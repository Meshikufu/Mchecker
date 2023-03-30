from flask import Flask
import requests
from bs4 import BeautifulSoup
from playsound import playsound
import time, datetime
import threading
import win32gui, win32con, win32api, win32console
import sys, os
import pystray
import PIL.Image
from tqdm import tqdm
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import pygame
import speech_recognition as sr
from gtts import gTTS
import webbrowser
import keyboard
import pyperclip, pyautogui, sqlite3, queue, tempfile


with open('data.txt') as f:
    data = f.read().splitlines()

url_list = []
key_list = []
value_list = []

for line in data:
    url_list.append(line)
    
    # get key
    start = line.find("read/") + 5
    end = line.find("-", start)
    end = line.find("-", end+1)
    #end = line.find("-", end+1)
    key = line[start:end].replace("-", " ")
    key_list.append(key)
    
    # get value
    start = line.rfind("chapter-") + len("chapter-")
    value = line[start:]
    value_list.append(value)

print("url_list:")
print(url_list)
print("key_list:")
print(key_list)
print("value_list:")
print(value_list)