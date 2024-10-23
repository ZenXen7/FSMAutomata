import pyautogui
import time
import threading
import tkinter as tk
from tkinter import messagebox


START_GAME = 'START_GAME'
ACCEPT_GAME = 'ACCEPT_GAME'
PICK_HERO = 'PICK_HERO'
EXIT = 'EXIT'

state = START_GAME
game_found = False
hero_picked = False

primary_hero = 'test.png'
backup_heroes = ['backup1.png', 'backup2.png']


status_var = None

def locate_image(image, confidence=0.7, timeout=10):
    
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            location = pyautogui.locateOnScreen(image, confidence=confidence)
            if location is not None:
                return pyautogui.center(location)
            time.sleep(1)
        except Exception as e:
            update_status(f'Error locating image {image}: {e}')
    return None

def start_game():
    global state, game_found
    update_status('Attempting to start game...')
    play_button = 'playbutton.png'
    play_location = locate_image(play_button, confidence=0.7, timeout=10)
    
    if play_location:
        update_status('Game start button found, starting game...')
        pyautogui.doubleClick(play_location)
        pyautogui.doubleClick(play_location)
        game_found = True
        state = ACCEPT_GAME
        fsm_loop()
    else:
        update_status('Failed to find the game start button.')
        state = EXIT

def accept_game():
    global state, game_found
    update_status('Waiting to accept game...')
    accept_button = 'Accept.png'
    accept_location = locate_image(accept_button, confidence=0.6, timeout=30)
    
    if accept_location:
        update_status('Accept button found, accepting game...')
        pyautogui.doubleClick(accept_location)
        pyautogui.doubleClick(accept_location)
        game_found = True
        state = PICK_HERO
        fsm_loop()
    else:
        update_status('Failed to accept the game within the time limit.')
        state = EXIT

def pick_hero():
    global state, hero_picked
    update_status('Attempting to pick hero...')
    
   
    primary_location = locate_image(primary_hero, confidence=0.6, timeout=10)
    
    if primary_location:
        update_status('Primary hero found, picking hero...')
        pyautogui.doubleClick(primary_location)
        pyautogui.doubleClick(primary_location)
        hero_picked = True
        state = EXIT
        return
    
   
    update_status('Primary hero not found, attempting to pick backup heroes...')
    for backup_hero in backup_heroes:
        backup_location = locate_image(backup_hero, confidence=0.6, timeout=10)
        if backup_location:
            update_status(f'Backup hero {backup_hero} found, picking hero...')
            pyautogui.doubleClick(backup_location)
            pyautogui.doubleClick(backup_location)
            hero_picked = True
            state = EXIT
            return
    
    update_status('Failed to pick any hero, exiting...')
    state = EXIT

def fsm_loop():
    
    global state
    if state == START_GAME:
        start_game()
    elif state == ACCEPT_GAME:
        accept_game()
    elif state == PICK_HERO:
        pick_hero()
    else:
        update_status('Invalid state, exiting...')
        state = EXIT

    update_status('Exiting program...')

def update_status(message):
  
    status_var.set(message)
    print(message)

def start_game_thread():
   
    threading.Thread(target=start_game).start()

def accept_game_thread():
   
    threading.Thread(target=accept_game).start()

def pick_hero_thread():
    
    threading.Thread(target=pick_hero).start()


def create_gui():
    global status_var

    window = tk.Tk()
    window.title("Game Automation FSM")

 
    status_var = tk.StringVar()
    status_label = tk.Label(window, textvariable=status_var, font=('Helvetica', 14), wraplength=400, height=4)
    status_label.pack(pady=10)

  
    start_button = tk.Button(window, text="Start Game", command=start_game_thread, width=20, height=2)
    start_button.pack(pady=5)

    accept_button = tk.Button(window, text="Accept Game", command=accept_game_thread, width=20, height=2)
    accept_button.pack(pady=5)

  
    pick_button = tk.Button(window, text="Pick Hero", command=pick_hero_thread, width=20, height=2)
    pick_button.pack(pady=5)

  
    exit_button = tk.Button(window, text="Exit", command=window.quit, width=20, height=2)
    exit_button.pack(pady=20)

  
    update_status("Ready")

  
    window.mainloop()


create_gui()
