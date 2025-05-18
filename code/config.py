import json

def load_config():
    with open("config_max.json") as config_file:
        return json.load(config_file)
