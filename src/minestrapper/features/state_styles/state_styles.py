from typing import TYPE_CHECKING, Callable

from minestrapper.util.ansi_colors import ANSI_COLORS
from minestrapper.state_handler import ServerState

if TYPE_CHECKING:
    from ....minestrapper.config_handler import ConfigHandler

class StateStyle:
    def __init__(self, config_handler: 'ConfigHandler'):
        self.config_handler = config_handler
        self.config = self.config_handler.get_config()['features']['state_styles']["styles"]

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
