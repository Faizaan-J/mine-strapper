from typing import Callable

from minestrapper.util.ansi_colors import ANSI_COLORS
from minestrapper.states import ServerState

def get_new_print_method_from_state(state : ServerState) -> Callable[[str], None]:
    map = {
        ServerState.STARTING: ANSI_COLORS["yellow"],
        ServerState.RUNNING: ANSI_COLORS["green"],
        ServerState.STOPPING: ANSI_COLORS["red"],
        ServerState.STOPPED: ANSI_COLORS["bright_red"],
    }

    color = map.get(state, ANSI_COLORS["reset"])
    def color_text(*args, **kwargs):
        text = " ".join(str(arg) for arg in args)
        print(f"{color}{text}{ANSI_COLORS['reset']}", **kwargs)
    
    return color_text