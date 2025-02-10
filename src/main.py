import time
import pyautogui
import pydirectinput
import window
import game
import config


last_input = 0

def sleep(seconds):

    time.sleep(seconds)

def main():
    print("[namakemono] Welcome to the Namakemono!")

    print("Before we start, make sure you're at the main menu.")
    print("="*50)
    input("If you're at the main menu, press Enter to continue...")

    print("Starting in 5 seconds... tab to the game")

    sleep(5)

    last_input = 0

    while True:
        game_state = game.get_game_state()
        print(f"Game state: {game_state}")



        if game_state == "home":
            playbtn_loc = config.get_button_location("play_button")
            window.click_location(playbtn_loc)
            sleep(1)

            mode_select_loc = config.get_button_location("mode_select")
            window.click_location(mode_select_loc)
            sleep(1)

            ai_mode_loc = config.get_button_location("ai_button")
            window.click_location(ai_mode_loc)
            sleep(1)

            start_button_loc = config.get_button_location("start_button")
            window.click_location(start_button_loc)
            sleep(1)
        elif game_state == "end-screen":
            window.click_match("again.png", threshold=0.6)
        elif game_state == "in-game":
            if time.time() - last_input > 3:
                game.send_random_input()
                last_input = time.time()


        sleep(1)



if __name__ == "__main__":
    main()

