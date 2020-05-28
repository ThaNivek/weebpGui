from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog

import os
import ttkthemes as tk
import math
import time
import win32api
import shutil
import webbrowser
import subprocess

from threading import Thread

def callback(url):
    webbrowser.open_new(url)

root = tk.ThemedTk()
root.title("Animated Background (Gui for Weebp)")
root.iconbitmap("icon.ico")
root.get_themes()
root.set_theme("breeze")
root.geometry("500x350")
root.minsize(350,300)
root.resizable(True,True)

infoBarText = StringVar()
infoBarText.set("Welcome User.")
linkMessage = StringVar()
linkMessage.set("This programm is based of @Francesco149's CLI Weebp project (THIS IS A LINK)")
screenSelected = IntVar()

configPath = ""

usedResolution = 0.0

linkToCreator = Label(root,fg="#1e00ff",textvariable=linkMessage,anchor = W,relief = FLAT)
linkToCreator.pack(side = TOP,fill=X)
linkToCreator.bind("<Button-1>", lambda e: callback("https://github.com/Francesco149/weebp"))

frame = Frame(root,relief = FLAT)
frame.pack(side= TOP,expand=1, fill=BOTH,padx = 5)

def on_help():
    tkinter.messagebox.showinfo("Animated Background","Just a simple GUI version of Francesco149's weebp with Icon by Flaticon: https://www.flaticon.com/free-icon/customer-support_1086581?term=customize&page=1&position=1\nmade by Nivek")

def on_file_open():
    infoBarText.set("Opening file dialog.")
    file_to_load = tkinter.filedialog.askopenfilename(initialdir=os.getcwd(), title="Select a Video File.",filetypes=(("WMV Files","*.wmv"),("All files","*.*")))
    if file_to_load == "":
        infoBarText.set("File operation was canceled by User.")
    else:
        infoBarText.set("Adding animation to list.")
        basename = os.path.basename(file_to_load)
        filename, extension = os.path.splitext(basename)
        bgdir = os.getcwd() + "\\Backgrounds\\"
        fileDir = bgdir + "\\" + filename
        if os.path.isdir(bgdir):
            os.mkdir(fileDir)
        else:
            os.mkdir(bgdir)
            os.mkdir(fileDir)
        shutil.copy(file_to_load,fileDir + "\\animation" + extension)
        f = open(fileDir + "\\config.txt","w+")
        f.write("animation" + extension)
        f.close()
        getAnimations()

menubar = Menu(root)
root.config(menu = menubar)

subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label="File",menu = subMenu)
subMenu.add_command(label="Open File",command=on_file_open)
subMenu.add_command(label="Exit",command = root.destroy)

subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Help",menu = subMenu)
subMenu.add_command(label="About", command=on_help)


path_ = ""
pathFolder = ""

def on_select(evt):
    global path_
    global configPath
    global pathFolder
    try:
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        path_ = os.getcwd() + "\\Backgrounds\\" + value
        pathFolder = path_
        configPath = path_ + "\\config.txt"
        f = open(path_ + "\\config.txt","r")
        path_ = path_ + "\\" + f.readline()
        f.close()
        infoBarText.set("Animation Loaded.")        
    except FileNotFoundError as e:
        infoBarText.set("This animation is corrupt.")
    except IndexError as e:
        infoBarText.set("There are no animations. Import an Animation with File/Open File")

listbox = Listbox(frame)
listbox.bind("<<ListboxSelect>>", on_select)
listbox.pack(side=LEFT,padx=10,pady=5,expand=1,fill=BOTH)

def getAnimations():
    listbox.delete(0,"end")
    for(path,dirs,files) in os.walk(os.curdir + "\\Backgrounds\\"):
        for i in range(len(dirs)):
            listbox.insert([i],dirs[i])
        break

getAnimations()

frame1 = Frame(frame,relief=FLAT)
frame1.pack(side=RIGHT,padx=5,pady=5,anchor = N)

def on_btn1_click():
    try:
        os.system("taskkill /F /IM mpv.exe")
        global path_
        global configPath
        if os.path.isfile(configPath):
            f = open("localConfig","w")
            basename = os.path.basename(pathFolder)
            f.write(basename)
            f.close()
            process = subprocess.Popen(["weebp-0.6.1-library\\wp.exe", "id"],close_fds=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
            stdout,stderr = process.communicate()
            id_ = stdout.decode("utf-8")
            os.system("weebp-0.6.1-library\wp-headless.exe run \"" + os.getcwd() + "\\weebp-0.6.1-library\\mpv.exe\" --wid=" + id_ + " \"" + path_ + "\" --loop=inf --player-operation-mode=pseudo-gui --force-window=yes --no-audio --input-ipc-server=\\.\pipe\mpvsocket")
            subprocess.call(["weebp-0.6.1-library\wp-headless.exe","mv --wait --class mpv -x " + str(usedResolution)])
            subprocess.call(["weebp-0.6.1-library\wp-headless.exe","add --wait --fullscreen --class mpv"])
            #-x " + str(usedResolution) + "
            infoBarText.set("Animation set.")
        else:
            infoBarText.set("No animation selected/it's corrupt or non existent")
    except Exception as e:
        infoBarText.set("An unexpected error ocurred please contact the developer.")
        f = open("errorLog.txt","w+")
        f.write(str(e))
        f.close()

def on_btn4_click():
    try:
        global path_
        global configPath
        if os.path.isfile(configPath):
            f = open("localConfig","w")
            basename = os.path.basename(pathFolder)
            f.write(basename)
            f.close()
            process = subprocess.Popen(["weebp-0.6.1-library\\wp.exe", "id"],close_fds=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
            stdout,stderr = process.communicate()
            id_ = stdout.decode("utf-8")
            os.system("weebp-0.6.1-library\wp-headless.exe run \"" + os.getcwd() + "\\weebp-0.6.1-library\\mpv.exe\" --wid=" + id_ + " \"" + path_ + "\" --loop=inf --player-operation-mode=pseudo-gui --force-window=yes --no-audio --input-ipc-server=\\.\pipe\mpvsocket")
            subprocess.call(["weebp-0.6.1-library\wp-headless.exe","mv --wait --class mpv -x " + str(usedResolution)])
            subprocess.call(["weebp-0.6.1-library\wp-headless.exe","add --wait --fullscreen --class mpv"])
            #-x " + str(usedResolution) + "
            infoBarText.set("Animation set.")
        else:
            infoBarText.set("Cannot set. Animation corrupt")
    except Exception as e:
        infoBarText.set("An unexpected error ocurred please contact the developer.")
        f = open("errorLog.txt","w+")
        f.write(str(e))
        f.close()

def on_btn2_click():
    os.system("taskkill /F /IM mpv.exe")

def on_btn3_click():
    shutil.rmtree(pathFolder)
    getAnimations()
    infoBarText.set("Walpaper succesfully deleted")

btn1 = ttk.Button(frame1, text="Set walpaper",command=on_btn1_click)
btn1.grid(row=0,column=0)
btn4 = ttk.Button(frame1, text="Add walpaper",command=on_btn4_click)
btn4.grid(row=1,column=0)
btn2 = ttk.Button(frame1, text="Remove any walpaper", command=on_btn2_click)
btn2.grid(row=2,column=0)
btn3 = ttk.Button(frame1, text="Delete selected walpaper", command=on_btn3_click)
btn3.grid(row=3,column=0)

def on_slider_moved(val):
    global usedResolution,screenSelectedDisplay
    screenSelectedDisplay.set(math.floor(screenSelected.get()))
    usedResolution = 1920*math.floor(float(val))

frame2=Frame(frame1,relief=FLAT)
frame2.grid(row=4,column=0,pady=10)
screenSelectedDisplay = IntVar()
screenSelectedDisplay.set(1)
labelText = ttk.Label(frame2,text="Screen:")
labelText.grid(row=0,column=0)
screenLabel = ttk.Label(frame2,textvariable=screenSelectedDisplay)
screenLabel.grid(row=1,column=0)
screenSelected_ = ttk.Scale(frame2,variable=screenSelected,from_=-10, to_=10, command = on_slider_moved) # len(win32api.EnumDisplayMonitors())
screenSelected_.grid(row=2,column=0)


label = Label(root,textvariable=infoBarText,anchor = W,relief = SUNKEN)
label.pack(side = BOTTOM,fill=X)

def on_closing():
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)

try:
    if sys.argv[1] == "startup":
        root.withdraw()
        f = open("localConfig","r")
        animation = f.readline()
        f.close()
        try:
            value = animation
            path_ = os.getcwd() + "\\Backgrounds\\" + value
            pathFolder = path_
            configPath = path_ + "\\config.txt"
            f = open(path_ + "\\config.txt","r")
            path_ = path_ + "\\" + f.readline()
            f.close()
            on_btn1_click()
            infoBarText.set("Animation Loaded.")        
        except FileNotFoundError as e:
            infoBarText.set("This animation is corrupt.")
        except IndexError as e:
            infoBarText.set("There are no animations. Import an Animation with File/Open File")

        root.destroy()
except:
    pass

root.mainloop()
