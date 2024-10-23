import pyautogui
import json
import time

game_found = False
hero_picked = False


backup_hero_portrait = 'backup.png'  

def start_game():
    global game_found
    print('Starting game..')
    image_path = 'playbutton.png'
    end_time = time.time() + 10
    
    while time.time() < end_time:
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=0.7)
            if location is not None:
                print('Game started')
                center = pyautogui.center(location)
                pyautogui.doubleClick(center)
                pyautogui.doubleClick(center)
                accept_game()
                return
            else:
                print('Image not found, retrying...')
                time.sleep(1)
        except Exception as e:
            print(f'Scanning..: {e}')
            time.sleep(1)
    
    print('Failed to find the image within the time limit.')

def accept_game():
    global game_found
    print('Waiting to accept game...')
    accept_button = 'Accept.png'
    start_time = time.time()
    
    while True:
        try:
            accept_location = pyautogui.locateOnScreen(accept_button, confidence=0.6)
            if accept_location is not None:
                print('Game accepted')
                center = pyautogui.center(accept_location)
                pyautogui.doubleClick(center)
                pyautogui.doubleClick(center)
                pyautogui.doubleClick(center)
                game_found = True
                return
            else:
                print('Accept button not found, retrying...')
                time.sleep(1)
        except Exception as e:
            print(f'Scanning... {e}')
            time.sleep(1)
        
        if time.time() - start_time > 600: 
            print('Failed to accept within 10 minutes or game not found.')
            break


def pick_selected():
    global hero_picked
    hero_portrait = 'test.png'
    pick_time = time.time() + 10
    
    if game_found:  
        while time.time() < pick_time:
            try:
                hero_location = pyautogui.locateOnScreen(hero_portrait, confidence=0.6)
                if hero_location is not None:
                    hero_center = pyautogui.center(hero_location)
                    pyautogui.doubleClick(hero_center)
                    pyautogui.doubleClick(hero_center)
                    hero_picked = True
                    print('Primary hero picked successfully')
                    return
                else:
                    print('Primary hero possibly banned or not found, retrying...')
                    time.sleep(1)
            except Exception as e:
                print(f'Scanning... {e}')
                time.sleep(1)

       
        print('Trying to pick backup hero...')
        while time.time() < pick_time:
            try:
                backup_hero_location = pyautogui.locateOnScreen(backup_hero_portrait, confidence=0.6)
                if backup_hero_location is not None:
                    backup_hero_center = pyautogui.center(backup_hero_location)
                    pyautogui.doubleClick(backup_hero_center)
                    pyautogui.doubleClick(backup_hero_center)
                    hero_picked = True
                    print('Backup hero picked successfully')
                    return
                else:
                    print('Backup hero also not found, retrying...')
                    time.sleep(1)
            except Exception as e:
                print(f'Scanning... {e}')
                time.sleep(1)
                
    print('Failed to pick any hero.')
    
start_game()
print('Game found:', game_found)
