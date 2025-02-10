"""
Namakemono - Window Management Module
===================================

This module handles window-related operations using the Win32 API.
It provides functionality to interact with game windows and processes.

Author: rfct0r
License: MIT
"""

import win32gui
import cv2
import pyautogui, pydirectinput
import PIL
import os, numpy as np


def get_focused_window():
    """


    Get the handle of the currently focused window.

    Returns:
        int: The handle of the currently focused window.
    """
    return win32gui.GetForegroundWindow()

def get_window_position(window_handle):
    """
    Get the position of the specified window. We will use this to calculate the position of the buttons, relative to the window.
    """
    window_rect = win32gui.GetWindowRect(window_handle)
    x = window_rect[0]
    y = window_rect[1]
    width = window_rect[2] - window_rect[0]
    height = window_rect[3] - window_rect[1]
    return (x, y, width, height)



def screenshot(window_handle):
    """

    Take a screenshot of the specified window.

    Args:
        window_handle (int): The handle of the window to screenshot.
    """

    window_rect = win32gui.GetWindowRect(window_handle)
    x = window_rect[0]
    y = window_rect[1]
    width = window_rect[2] - window_rect[0]
    height = window_rect[3] - window_rect[1]

    scr = pyautogui.screenshot(region=(x, y, width, height))
    return scr


def take_and_open_screenshot():
    """
    Take a screenshot of the currently focused window and open it in PIL.
    """
    window_handle = get_focused_window()
    scr = screenshot(window_handle)
    scr.show()

def find_on_screen_cv2(image_path, threshold=0.8, debug=False):
    """
    Find an image on the screen using both color and grayscale template matching.
    """
    window = get_focused_window()

    window_title = win32gui.GetWindowText(window)
    if "Marvel Rivals" not in window_title:
        return None

    scr = screenshot(window)
    scr = cv2.cvtColor(np.array(scr), cv2.COLOR_RGB2BGR)

    image_path = os.path.join(os.path.dirname(__file__), "images", image_path)

    img = cv2.imread(image_path)
    if img is None:
        print(f"Failed to load template image: {image_path}")
        return None

    res_color = cv2.matchTemplate(scr, img, cv2.TM_CCOEFF_NORMED)

    scr_gray = cv2.cvtColor(scr, cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res_gray = cv2.matchTemplate(scr_gray, img_gray, cv2.TM_CCOEFF_NORMED)

    max_val_color = np.max(res_color)
    max_val_gray = np.max(res_gray)

    res = res_color if max_val_color > max_val_gray else res_gray
    loc = np.where(res >= threshold)

    if len(loc[0]) > 0:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        width = img.shape[1]
        height = img.shape[0]

        center_x = max_loc[0] + width//2
        center_y = max_loc[1] + height//2
        center = (center_x, center_y)

        if debug:
            cv2.rectangle(scr, max_loc, (max_loc[0] + width, max_loc[1] + height), (0, 255, 0), 2)
            cv2.circle(scr, center, 5, (0, 0, 255), -1)

            # Add confidence score to debug output
            print(f"Match confidence: {max_val:.2f} ({'color' if max_val_color > max_val_gray else 'grayscale'})")

            cv2.imshow('Match Found', scr)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        window_rect = get_window_position(window)
        screen_coords = (
            window_rect[0] + center_x,
            window_rect[1] + center_y
        )

        return screen_coords

    else:
        if debug:
            print(f"No match found. Best confidence - Color: {max_val_color:.2f}, Grayscale: {max_val_gray:.2f}")
        return None

def click_match(image_path, threshold=0.8, debug=False):
    """
    Click on the center of the image found on the screen.
    """
    location = find_on_screen_cv2(image_path, threshold=threshold, debug=debug)
    if location:
        pydirectinput.moveTo(location[0], location[1])
        pydirectinput.click()

def click_location(location, base_width=1920, base_height=1080):
    """
    Click on the specified location, scaled according to the window size.

    Args:
        location (tuple): (x, y) coordinates based on base resolution
        base_width (int): Base width the coordinates were calculated for (default: 1920)
        base_height (int): Base height the coordinates were calculated for (default: 1080)
    """
    window = get_focused_window()
    window_rect = get_window_position(window)

    scale_x = window_rect[2] / base_width
    scale_y = window_rect[3] / base_height

    scaled_x = int(location[0] * scale_x)
    scaled_y = int(location[1] * scale_y)

    pydirectinput.moveTo(window_rect[0] + scaled_x, window_rect[1] + scaled_y)
    pydirectinput.click()
