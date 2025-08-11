import tkinter as tk
import fnmatch
import os
from pygame import mixer

canvas = tk.Tk()
canvas.title("VibeShift")
canvas.geometry("650x500")
canvas.config(bg='black')

mixer.init()

happy_path = "/Users/abhilash/Desktop/music player/happy"
sad_path ="/Users/abhilash/Desktop/music player/sad"
chill_path = "/Users/abhilash/Desktop/music player/chill"
pattern = "*.mp3"

current_path = happy_path  

prev_img = tk.PhotoImage(file="prev_img.png")
stop_img = tk.PhotoImage(file="stop_img.png")
play_img = tk.PhotoImage(file="play_img.png")
pause_img = tk.PhotoImage(file="pause_img.png")
next_img = tk.PhotoImage(file="next_img.png")

is_paused = False
is_stopped = False

def load_songs(path):
    """Clear listbox and load songs from given path"""
    global current_path
    current_path = path
    listBox.delete(0, 'end')
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, pattern):
            listBox.insert('end', filename)

def select():
    global is_paused, is_stopped
    is_paused =False
    is_stopped =False
    current_song = listBox.get("anchor")
    label.config(text=current_song)
    mixer.music.load(os.path.join(current_path, current_song))
    mixer.music.play()
    check_song_end()

def stop():
    global is_stopped
    mixer.music.stop()
    is_stopped =True
    listBox.select_clear('active')

def play_next():
    global is_paused, is_stopped
    is_paused = False
    is_stopped = False
    next_song = listBox.curselection()
    next_song = next_song[0] + 1 if next_song else 0
    if next_song >= listBox.size():

        next_song = 0
    song_name = listBox.get(next_song)
    label.config(text=song_name)
    mixer.music.load(os.path.join(current_path, song_name))
    mixer.music.play()
    listBox.select_clear(0, 'end')
    listBox.activate(next_song)
    listBox.select_set(next_song)
    check_song_end()

def play_prev():
    global is_paused, is_stopped
    is_paused = False
    is_stopped = False
    prev_song = listBox.curselection()
    prev_song = prev_song[0] - 1 if prev_song else listBox.size() - 1
    song_name = listBox.get(prev_song)
    label.config(text=song_name)
    mixer.music.load(os.path.join(current_path, song_name))
    mixer.music.play()
    listBox.select_clear(0, 'end')
    listBox.activate(prev_song)
    listBox.select_set(prev_song)
    check_song_end()

def pause_song():
    global is_paused
    if not is_paused:
        mixer.music.pause()
        is_paused =True
    else:
        mixer.music.unpause()
        is_paused =False

def check_song_end():
    if is_stopped:
        return
    if not mixer.music.get_busy() and not is_paused:
        play_next()
    else:
        canvas.after(1000, check_song_end)

mood_frame = tk.Frame(canvas, bg="black")
mood_frame.pack(pady=10)

tk.Button(mood_frame, text="😊 Happy", font=("Arial", 12, "bold"), bg="yellow", command=lambda: load_songs(happy_path)).pack(side='left', padx=10)
tk.Button(mood_frame, text="😢 Sad", font=("Arial", 12, "bold"), bg="lightblue", command=lambda: load_songs(sad_path)).pack(side='left', padx=10)
tk.Button(mood_frame, text="😎 Chill", font=("Arial", 12, "bold"), bg="lightgreen", command=lambda: load_songs(chill_path)).pack(side='left', padx=10)

listBox = tk.Listbox(canvas, fg="cyan", bg="white", width=150, font=("Arial", 14))
listBox.pack(padx=15, pady=15)

label = tk.Label(canvas, text='', bg='black', fg='yellow', font=("Arial", 18, "bold"))
label.pack(pady=15)

btn_frame = tk.Frame(canvas, bg="black")
btn_frame.pack(pady=10)

prev_frame = tk.Frame(btn_frame, bg="black")
prev_frame.pack(side='left', padx=10)
prevButton = tk.Button(prev_frame, image=prev_img, bg='black', borderwidth=0, command=play_prev)
prevButton.pack()
tk.Label(prev_frame, text="Prev", bg='black', fg='white', font=("Arial", 10)).pack()

stop_frame = tk.Frame(btn_frame, bg="black")
stop_frame.pack(side='left', padx=10)
stopButton = tk.Button(stop_frame, image=stop_img, bg="black", borderwidth=0, command=stop)
stopButton.pack()
tk.Label(stop_frame, text="Stop", bg='black', fg='white', font=("Arial", 10)).pack()

play_frame = tk.Frame(btn_frame, bg="black")
play_frame.pack(side='left', padx=10)
playButton = tk.Button(play_frame, image=play_img, bg='black', borderwidth=0, command=select)
playButton.pack()
tk.Label(play_frame, text="Play", bg='black', fg='white', font=("Arial", 10)).pack()

pause_frame = tk.Frame(btn_frame, bg="black")
pause_frame.pack(side='left', padx=10)
pauseButton = tk.Button(pause_frame, text="pause", image=pause_img, bg='black', borderwidth=0, command=pause_song)
pauseButton.pack()
tk.Label(pause_frame, text="Pause", bg='black', fg='white', font=("Arial", 10)).pack()

next_frame = tk.Frame(btn_frame, bg="black")
next_frame.pack(side='left', padx=10)
nextButton = tk.Button(next_frame, image=next_img, bg='black', borderwidth=0, command=play_next)
nextButton.pack()
tk.Label(next_frame, text="Next", bg='black', fg='white', font=("Arial", 10)).pack()

load_songs(happy_path)

canvas.mainloop()