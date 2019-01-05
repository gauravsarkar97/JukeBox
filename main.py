import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk
from pygame import mixer
from mutagen.mp3 import MP3

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

# Menubar
menubar = Menu(root)
root.config(menu=menubar)

# The sub-menu
submenu = Menu(menubar, tearoff=0)

root.title("Juke Box")
root.iconbitmap(r'images/melody.ico')
# root.geometry('400x400')

# Status bar
statusbar = ttk.Label(root, text="Welcome to Juke Box", relief=SUNKEN, anchor=W, font='Times 12 bold')
statusbar.pack(side=BOTTOM, fill=X)

leftftrame = Frame(root)
leftftrame.pack(side=LEFT, padx=20)

playlistbox = Listbox(leftftrame)
playlistbox.pack()

playlist = []  # Array that contains full path + filename


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)


def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


addBtn = ttk.Button(leftftrame, text=' + Add', command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    try:
        selected_song = playlistbox.curselection()
        selected_song = int(selected_song[0])  # Type-casting to int, otherwise it returns a tuple
        playlistbox.delete(selected_song)
        playlist.pop(selected_song)
    except:
        tkinter.messagebox.showerror('Juke Box', "Please select a song & then press -Del")


delBtn = ttk.Button(leftftrame, text=' - Del', command=del_song)
delBtn.pack(side=LEFT)

rightframe = Frame(root)
rightframe.pack()

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe, text="Total Time : --:--")
lengthlabel.pack(pady=5)

currenttimelabel = ttk.Label(topframe, text="Current Time : --:--", relief=GROOVE)
currenttimelabel.pack(pady=5)

mixer.init()  # initializing the mixer

menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="Exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo('About Juke Box',
                                "Our very own Music Player \nSupports .mp3 and .wav files \nCopyright @gauravsarkar97")


submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About Us", command=about_us)


def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    min, sec = divmod(total_length, 60)
    min = round(min)
    sec = round(sec)
    timeformat = '{:02d}:{:02d}'.format(min, sec)
    lengthlabel['text'] = "Total Length : " + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            min, sec = divmod(t, 60)
            min = round(min)
            sec = round(sec)
            timeformat = '{:02d}:{:02d}'.format(min, sec)
            currenttimelabel['text'] = "Current Time : " + timeformat
            time.sleep(1)
            t -= 1


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])  # Type-casting to int, otherwise it returns a tuple
            play_it = playlist[selected_song]  # Getting the full path of the selected song
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music : " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('Juke Box', "No song(s) selected.\nPlease Open & select songs")


def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)


muted = FALSE


def mute_music():  # Mute & Unmute Functionality
    global muted
    if muted:
        muted = FALSE
        volumeBtn.configure(image=volumePhoto)
        mixer.music.set_volume(0.5)
        scale.set(50)
        statusbar['text'] = "Music Unmuted"
    else:
        muted = TRUE
        volumeBtn.configure(image=mutePhoto)
        mixer.music.set_volume(0)
        scale.set(0)
        statusbar['text'] = "Music Muted"


# Adding a midle frame
middleframe = Frame(rightframe)
middleframe.pack(pady=20, padx=5)

# Buttons
playPhoto = PhotoImage(file='images/play.png')
playBtn = ttk.Button(middleframe, image=playPhoto, command=play_music)  # play button
playBtn.grid(row=0, column=0, padx=10)

pausePhoto = PhotoImage(file='images/pause.png')
pauseBtn = ttk.Button(middleframe, image=pausePhoto, command=pause_music)  # pause button
pauseBtn.grid(row=0, column=1, padx=10)

stopPhoto = PhotoImage(file='images/stop.png')
stopBtn = ttk.Button(middleframe, image=stopPhoto, command=stop_music)  # stop button
stopBtn.grid(row=0, column=2, padx=10)

# Adding a bottom frame
bottomframe = Frame(rightframe)
bottomframe.pack(pady=30, padx=30)

rewindPhoto = PhotoImage(file='images/rewind.png')
rewindBtn = ttk.Button(bottomframe, image=rewindPhoto, command=rewind_music)  # Rewind button
rewindBtn.grid(row=0, column=0, pady=10)

volumePhoto = PhotoImage(file='images/speaker.png')
mutePhoto = PhotoImage(file='images/mute.png')
volumeBtn = ttk.Button(bottomframe, image=volumePhoto, command=mute_music)  # Rewind button
volumeBtn.grid(row=0, column=1, pady=10, padx=30)

# Volume Scale
scale = ttk.Scale(bottomframe, from_=0, to_=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)  # setting default value
mixer.music.set_volume(0.5)
scale.grid(row=0, column=2, pady=10)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)  # Override close button

root.mainloop()
