from typing import Callable

from minestrapper.util.ansi_colors import ANSI_COLORS
from minestrapper.states import ServerState

def get_colored_text(text: str, state: ServerState) -> str:
    map = {
        ServerState.STARTING: ANSI_COLORS["yellow"],
        ServerState.RUNNING: ANSI_COLORS["green"],
        ServerState.STOPPING: ANSI_COLORS["red"],
        ServerState.STOPPED: ANSI_COLORS["bright_red"],
    }

    color = map.get(state, ANSI_COLORS["reset"])
    
    return f"{color}{text}{ANSI_COLORS['reset']}"