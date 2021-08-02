
import sys
import pathlib
import os
global tooltip_path, config_path



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# tooltip_path = resource_path("TooltipDescription.json")
# config_path = resource_path("config.json")
tooltip_path = "TooltipDescription.json"
config_path = "config.json"
