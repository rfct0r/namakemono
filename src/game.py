import window
import time
import random
import pydirectinput

import config

possible_heroes = [
    "hulk",
    "groot",
    "thor"
]

def is_home():

    home_loc = window.find_on_screen_cv2("lobby/home.png")
    play_loc = window.find_on_screen_cv2("lobby/playbtn.png")
    start_loc = window.find_on_screen_cv2("lobby/start.png")
    change_loc = window.find_on_screen_cv2("lobby/change-hero.png")

    if home_loc or play_loc or start_loc or change_loc:
        return True
    else:
        return False

def is_hero_select():
    hero_select_loc = window.find_on_screen_cv2("heroselect.png")
    if hero_select_loc:
        return True
    else:
        return False

def is_in_game():
    healthbar_loc = window.find_on_screen_cv2("healthbar.png")
    crosshair_loc = window.find_on_screen_cv2("crosshair.png")

    if healthbar_loc and crosshair_loc:
        return True
    else:

        return False

def is_end_screen():
    again_loc = window.find_on_screen_cv2("again.png")
    if again_loc:
        return True
    else:
        return False


def get_game_state():
    """

    Get the current game state.

    """
    home = is_home()
    hero_select = is_hero_select()
    end_screen = is_end_screen()

    # until i think of something better
    in_game = not home and not hero_select and not end_screen


    if home:
        return "home"
    elif hero_select:
        random_hero = random.choice(possible_heroes)
        hero_loc = config.get_hero_location(random_hero)
        window.click_location(hero_loc)

        time.sleep(1)

        select_loc = config.get_button_location("hero_select")
        window.click_location(select_loc)

        return "hero-select"
    elif in_game:
        return "in-game"
    elif end_screen:
        return "end-screen"
    else:
        return "unknown"



def click_hero_select():
    """
    Click on the hero select button.
    """

    # get a random hero from the possible_heroes list
    random_hero = random.choice(possible_heroes)
    window.click_match(random_hero)

    # wait for the hero to be selected
    time.sleep(1)

    # click on the start button
    window.click_match("confirm.png")

def send_random_input():
    """
    Send a random input to the game.
    """
    possible_inputs = ["w", "a", "s", "d"]
    random_input = random.choice(possible_inputs)

    pydirectinput.press(random_input)

