# config.py
import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "window_geometry": None,
    "right_panel_width": 250,
    "zoom_factor": 1.0,
    "open_external": True,  # True = separate windows, False = in-game browser
    "tool_window_geometry": [200, 200, 900, 700],  # x, y, width, height
    "theme": "dark_pastel"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Ensure all default keys exist
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                
                # Convert geometry values to integers if they exist
                if config.get("window_geometry") and isinstance(config["window_geometry"], list):
                    config["window_geometry"] = [int(x) for x in config["window_geometry"]]
                if config.get("tool_window_geometry") and isinstance(config["tool_window_geometry"], list):
                    config["tool_window_geometry"] = [int(x) for x in config["tool_window_geometry"]]
                
                # Ensure numeric values are correct type
                if "zoom_factor" in config:
                    config["zoom_factor"] = float(config["zoom_factor"])
                if "right_panel_width" in config:
                    config["right_panel_width"] = int(config["right_panel_width"])
                    
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

def get_config_value(key, default=None):
    """Get a single config value"""
    config = load_config()
    return config.get(key, default)

def set_config_value(key, value):
    """Set a single config value"""
    config = load_config()
    config[key] = value
    save_config(config)