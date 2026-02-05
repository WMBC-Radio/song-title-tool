# initial version by Will C. 2-5-2026 for the spring 2026 semester.
# specical thanks to the engineering team and whoever invented the casette i suppose

from tkinter import *
import subprocess
# 4 checkboxes, each with a button next to them and the final one having a text input box next to it.
# checkbox determines if we write to the output file with playerctl from Spotify, Chrome/youtube, vlc, or the text of the text input box.

def write_to_file(song_info):
    with open("output.txt", "w") as f:
        f.write(song_info)
    # print repeatedly on same line, not new lines
    print(f"\rWritten to file: {song_info}", end='')
# determine valid players to use. output of playerctl --list-all, and we will filter with playerctl --player="NAME" metadata --format "{{ artist }} - {{ title }}"
valid_players = ["spotify", "chrome", "vlc","vivaldi"]

def query_players():

    players = []
    try:
        result = subprocess.run(["playerctl", "--list-all"], capture_output=True, text=True)
        print(f"playerctl output: {result.stdout}")
        for line in result.stdout.splitlines():
            line = line.strip()
            line = line.split('.')[0]
            print(f"Checking player: {line}")
            if line in valid_players:
                players.append(line)
            if line not in valid_players:
                print(f"Player {line} is not in valid players list.")
    except Exception as e:
        print(f"Error querying players: {e}")
    return players 

active_players = query_players()

# make a call to playerctl to get the current song info for a given player 
def get_song_info(player):
    try:
        result = subprocess.run(["playerctl", "--player", player, "metadata", "--format", "{{ artist }} - {{ title }}"], capture_output=True, text=True)
        song_info = result.stdout.strip()
        print(f"Song info for {player}: {song_info}")
        return song_info
    except Exception as e:
        print(f"Error getting song info for {player}: {e}")
        return ""
def w_devtest():
    for p in active_players:
        print(f"Active player: {p}")
        print(get_song_info(p))

# gui setup
root = Tk()
root.title("Music Info Writer")
root.geometry("400x500")
# root.configure(bg="black")
#if checkbox is toggled, we write when playerctl returns a different song than last time 
last_song = ""
selected_player = "" 

# style the root more:
# root.configure(bg="#a5a5a5")
# border?

root.configure(highlightbackground="black", highlightthickness=2)
# make font bigger
root.option_add("*Font", "Helvetica 16")


def update_song_info():
    global last_song
    song_info = ""
    if spotify_var.get() and "spotify" in active_players:
        song_info = get_song_info("spotify")
    elif chrome_var.get() and "chrome" in active_players:
        song_info = get_song_info("chrome")
    elif vlc_var.get() and "vlc" in active_players:
        song_info = get_song_info("vlc")
    elif custom_var.get():
        song_info = custom_entry.get().strip()
    
    if song_info and song_info != last_song:
        write_to_file(song_info)
        last_song = song_info
    root.after(5000, update_song_info)  # check every 5 seconds

# only one selected at a time, so we use checkbuttons but enforce only one selection
def on_checkbutton_toggle(var):
    if var == spotify_var:
        chrome_var.set(False)
        vlc_var.set(False)
        custom_var.set(False)
    elif var == chrome_var:
        spotify_var.set(False)
        vlc_var.set(False)
        custom_var.set(False)
    elif var == vlc_var:
        spotify_var.set(False)
        chrome_var.set(False)
        custom_var.set(False)
    elif var == custom_var:
        spotify_var.set(False)
        chrome_var.set(False)
        vlc_var.set(False)
    update_song_info()
# radio buttons with labels next to, and a text input box next to the final one
spotify_var = BooleanVar()
chrome_var = BooleanVar()
vlc_var = BooleanVar()
custom_var = BooleanVar()
# title
title_label = Label(root, text="WMBC's Title Tool!", font=("Helvetica", 24, "bold"))
title_label.pack(pady=20)

#t
header_label = Label(root, text="Select the current music source:", font=("Helvetica", 18))
header_label.pack(pady=20)


spotify_check = Checkbutton(root, text="Spotify", variable=spotify_var)
spotify_check.bind("<Button-1>", lambda e: on_checkbutton_toggle(spotify_var))

chrome_check = Checkbutton(root, text="Chrome/YouTube", variable=chrome_var)
chrome_check.bind("<Button-1>", lambda e: on_checkbutton_toggle(chrome_var))

vlc_check = Checkbutton(root, text="VLC", variable=vlc_var)
vlc_check.bind("<Button-1>", lambda e: on_checkbutton_toggle(vlc_var))

custom_check = Checkbutton(root, text="Custom Song Name:", variable=custom_var)
custom_check.bind("<Button-1>", lambda e: on_checkbutton_toggle(custom_var))

custom_entry = Entry(root)


#label extra
# plz format in format of: Artist - title
bonus_label = Label(root, text="For custom song name, please format as: Artist - Title", font=("Helvetica", 16,))


# center boxes on the screen
spotify_check.pack(pady=10)
chrome_check.pack(pady=10)
vlc_check.pack(pady=10)

#custom on same line as text input boxes
custom_check.pack(pady=20) 
custom_entry.pack(pady=20)

bonus_label.pack(pady=10)
# start the update loop
root.after(1000, update_song_info)
root.mainloop() 

