import os
import ctypes

from typing import TYPE_CHECKING, Callable

from minestrapper.features.feature import Feature
from minestrapper.util.ansi_colors import ANSI_COLORS
from minestrapper.state_handler import ServerState

if TYPE_CHECKING:
    from ....minestrapper.server import Server

class StateStyle(Feature):
    def __init__(self, server: "Server", ):
        super().__init__("State Styles", "Provides colored text and titles for different server states", server)
        self.config = self.server.config_handler.get_config()['features']['state_styles']["styles"]

    def get_colored_text(self, text: str, state: ServerState) -> str:
        map = {
            ServerState.STARTING: ANSI_COLORS.get(self.config["starting"]["color"], ANSI_COLORS["reset"]),
            ServerState.RUNNING: ANSI_COLORS.get(self.config["running"]["color"], ANSI_COLORS["reset"]),
            ServerState.STOPPING: ANSI_COLORS.get(self.config["stopping"]["color"], ANSI_COLORS["reset"]),
            ServerState.STOPPED: ANSI_COLORS.get(self.config["stopped"]["color"], ANSI_COLORS["reset"]),
            ServerState.PAUSED: ANSI_COLORS.get(self.config["paused"]["color"], ANSI_COLORS["reset"]),
        }

        color = map.get(state, ANSI_COLORS["reset"])
        
        return f"{color}{text}{ANSI_COLORS['reset']}"
    
    def get_title(self, state: ServerState) -> str:
        map = {
            ServerState.STARTING: self.config["starting"].get("title", "Starting"),
            ServerState.RUNNING: self.config["running"].get("title", "Running"),
            ServerState.STOPPING: self.config["stopping"].get("title", "Stopping"),
            ServerState.STOPPED: self.config["stopped"].get("title", "Stopped"),
            ServerState.PAUSED: self.config["paused"].get("title", "Paused"),
        }

        return map.get(state, "Unknown")
    
    def run(self):
        @self.server.add_line_transformer
        def state_styles_transformer(line: str):
            return self.get_colored_text(line, self.server.state_handler.get())
        
        @self.server.state_handler.on_state_change
        def set_terminal_title():
            title = self.get_title(self.server.state_handler.get())
            if (os.name == "nt"):
                ctypes.windll.kernel32.SetConsoleTitleW(title)
            else:
                sys.stdout.write(f'\x1b]0;{title}\x07')
                sys.stdout.flush()
