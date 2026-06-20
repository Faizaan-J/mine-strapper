from pathlib import Path
import subprocess
from typing import Callable
import threading

from .config_handler import ConfigHandler
from .states import ServerState

from minestrapper.util.get_state_from_line import get_state_from_line

from time import sleep as wait

class Server:
    def __init__(self, path: str | Path):
        self.path : str = (str(path) if isinstance(path, Path) else path)
        self.config_handler : ConfigHandler = ConfigHandler(self.path)
        self.server_state : ServerState = ServerState.STARTING
        self.state_callbacks : dict[ServerState, list[Callable]] = {}
        self.periodic_callbacks : list[Callable] = []
        self.new_line_callbacks : list[Callable] = []
        self.server_process : subprocess.Popen | None = None

    def __start_server_process(self):
        config = self.config_handler.get_config()

        jar_path = f"{config['server']['jar_name']}.jar"

        full_command = [
            "java"
        ]
        java_args = [
            f"-Xms{config['server']['min_ram']}",
            f"-Xmx{config['server']['max_ram']}",
        ]

        if "other_args" in config['server']:
            java_args.extend(config['server']['other_args'])

        full_command.extend(java_args)
        full_command.extend([
            "-jar", jar_path, "nogui"
        ])

        server_process = subprocess.Popen(
            full_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace"
        )

        return server_process
    
    def start_server(self):
        self.server_process = self.__start_server_process()

        def loop():
            while self.server_state != ServerState.STOPPED and self.server_process is not None and self.server_process.poll() is None:
                self.__on_periodic()

                if (self.periodic_callbacks):
                    for callback in self.periodic_callbacks:
                        callback()
                wait(0.020)
                
        self.periodic_thread = threading.Thread(target=loop, daemon=True)
        self.periodic_thread.start()

        def output_loop():
            assert self.server_process is not None
            if (self.server_process.stdout is not None):
                for line in self.server_process.stdout:
                    self.__on_new_line(line)
       
        self.output_thread = threading.Thread(target=output_loop, daemon=True)
        self.output_thread.start()

        assert self.server_process is not None
        return self.server_process.wait()
    
    
    def __on_new_line(self, line : str):
        print(line, end="")

        new_state = get_state_from_line(line)
        if (new_state is not None and new_state != self.server_state):
            self.server_state = new_state

            if new_state in self.state_callbacks:
                for callback in self.state_callbacks[new_state]:
                    callback()

    def on_new_line(self, function: Callable):
        self.new_line_callbacks.append(function)
        return function

    def __on_periodic(self):
        for callback in self.periodic_callbacks:
            callback()

    def on_periodic(self, function: Callable):
        self.periodic_callbacks.append(function)

        return function
    
    def on_state_change(self, function : Callable, state: ServerState):
        def decorator():
            if self.server_state == state:
                function()

        if (not isinstance(state, ServerState)):
            raise NameError(f"State {state} is not a valid server state.")

        if state not in self.state_callbacks:
            self.state_callbacks[state] = []
        self.state_callbacks[state].append(decorator)
        return decorator
