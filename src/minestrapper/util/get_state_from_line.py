import re
from states import ServerState

# These regex statements were vibe coded 🤤: 
# "[HH:MM:SS] [Thread/Level]:"
LOG_PREFIX = re.compile(r"^\[\d{2}:\d{2}:\d{2}\] \[[^\]]+\]: ")
# "Playername joined the game"
PLAYER_JOINED_REGEX = r"^[^\s]+ joined the game"

def __strip_prefix(line: str) -> str:
    return LOG_PREFIX.sub("", line, count=1)

def get_state_from_line(line: str):
    msg = __strip_prefix(line)

    state_table = {
        msg.startswith("Done ("): ServerState.RUNNING,
        msg.startswith("Stopping the server"): ServerState.STOPPING,
        msg.startswith("Server empty for 60 seconds, pausing"): ServerState.PAUSED,
        re.match(PLAYER_JOINED_REGEX, msg): ServerState.RUNNING
    }

    new_state = None
    for condition in state_table:
        new_state_value = state_table[condition]
        if condition:
            new_state = new_state_value
            break

    return new_state
