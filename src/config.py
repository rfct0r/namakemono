import json
import os

config_path = os.path.join(os.path.dirname(__file__), "config.json")
with open(config_path) as f:
    config = json.load(f)

def get_button_location(button_name):
    return config["button_locations"][button_name]

def get_hero_location(hero_name):
    return config["hero_locations"][hero_name]

