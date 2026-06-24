from pathlib import Path
import subprocess
from typing import Callable
import threading

import os

from .logger import Logger

from .config_handler import ConfigHandler
from .state_handler import ServerState, StateHandler

from minestrapper.util.get_state_from_line import get_state_from_line

from minestrapper.features.handle_built_in_features import handle_built_in_features

from time import sleep as wait

class Server:
    def __init__(self, path: str | Path):
        self.path : str = (str(path) if isinstance(path, Path) else path)
        self.config_handler : ConfigHandler = ConfigHandler(self.path)
        self.state_handler : StateHandler = StateHandler(ServerState.STARTING)
        self.periodic_callbacks : list[Callable] = []
        self.new_line_callbacks : list[Callable] = []
        self.server_process : subprocess.Popen | None = None

        self.logger = Logger(self)

        os.chdir(self.path)

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
            while self.state_handler.get() != ServerState.STOPPED and self.server_process is not None and self.server_process.poll() is None:
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
                    self.__on_new_line(line.strip("\n"))
       
        self.output_thread = threading.Thread(target=output_loop, daemon=True)
        self.output_thread.start()

        self.logger.info("Server process started successfully.")
        handle_built_in_features(self)
    
    def wait_loop(self):
        assert self.server_process is not None
        self.server_process.wait()

        # If the server process has stopped, this code should now run.
        self.state_handler.set(ServerState.STOPPED)
        self.logger.info("Server process has stopped.")
        self.logger.publish_minestrapper_log()
        input("Press Enter to exit...")

    def __on_new_line(self, line : str):
        new_state = get_state_from_line(line)
        if (new_state is not None and new_state != self.state_handler.get()):
            self.state_handler.set(new_state)

        self.logger.forwarded_log(line)

        if self.new_line_callbacks:
            for callback in self.new_line_callbacks:
                callback(line)

    def on_new_line(self, function: Callable):
        self.new_line_callbacks.append(function)
        return function

    def __on_periodic(self):
        for callback in self.periodic_callbacks:
            callback()

    def on_periodic(self, function: Callable):
        self.periodic_callbacks.append(function)

        return function
