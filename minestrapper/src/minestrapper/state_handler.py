from enum import Enum
from typing import Callable

class ServerState(Enum):
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"

class StateHandler:
    def __init__(self, initial_state: ServerState):
        self.__server_state = initial_state
        self.state_callbacks: dict[ServerState | None, list[Callable]] = {}

    def set(self, state: ServerState):
        if (state == self.__server_state):
            return
        
        self.__server_state = state

        for callback in self.state_callbacks.get(state, []):
            callback()

        for callback in self.state_callbacks.get(None, []):
            callback()

    def on_state_change(self, function: Callable, state: ServerState | None = None) -> Callable:
        def decorator():
            if state is None or self.get() == state:
                function()

        if (state is not None and not isinstance(state, ServerState)):
            raise NameError(f"State {state} is not a valid server state")

        if state not in self.state_callbacks:
            self.state_callbacks[state] = []
        self.state_callbacks[state].append(function)

        decorator() # Call the function immediately if we're already in the correct state
        return decorator

    def get(self) -> ServerState:
        return self.__server_state
