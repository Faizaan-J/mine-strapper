import os
import sys

import ctypes

from typing import TYPE_CHECKING

from .state_styles.state_styles import StateStyle

if TYPE_CHECKING:
    from ..server import Server

def handle_built_in_features(server: "Server"):
    if server.config_handler.get_config()['features']['state_styles']["feature_enabled"]["enabled"]:
        state_style = StateStyle(server.config_handler)
        @server.add_line_transformer
        def state_styles_transformer(line: str):
            return state_style.get_colored_text(line, server.state_handler.get())
        
        @server.state_handler.on_state_change
        def set_terminal_title():
            title = state_style.get_title(server.state_handler.get())
            if (os.name == "nt"):
                ctypes.windll.kernel32.SetConsoleTitleW(title)
            else:
                sys.stdout.write(f'\x1b]0;{title}\x07')
                sys.stdout.flush()