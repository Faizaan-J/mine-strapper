from pathlib import Path
import subprocess
from typing import Callable
import threading

import os

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.output.color_depth import ColorDepth

from minestrapper.util.shutdown_handler import ShutdownHandler

from .logger import Logger

from .config_handler import ConfigHandler
from .state_handler import ServerState, StateHandler

from minestrapper.util.get_state_from_line import get_state_from_line

from minestrapper.features.handle_built_in_features import handle_built_in_features

class Server:
    def __init__(self, path: str | Path):
        self.path : str = (str(path) if isinstance(path, Path) else path)
        self.config_handler : ConfigHandler = ConfigHandler(self)
        self.state_handler : StateHandler = StateHandler(ServerState.STARTING)
        self.new_line_callbacks : list[Callable] = []
        self.server_process : subprocess.Popen | None = None

        self.logger = Logger(self)
        self.session: PromptSession = PromptSession(color_depth=ColorDepth.TRUE_COLOR)

        self.shutdown_handler = ShutdownHandler(self)

        self.__stdin_lock = threading.Lock()

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

        os_specific = {}
        if (os.name == "nt"):
            os_specific["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            os_specific["start_new_session"] = True

        server_process = subprocess.Popen(
            full_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            encoding="utf-8",
            errors="replace",
            **os_specific
        )

        self.logger.info("Server process started successfully")
        return server_process

    def start_server(self):
        self.server_process = self.__start_server_process()

        def command_loop():
            while True:
                try:
                    with patch_stdout():
                        command = self.session.prompt("> ")
                except (EOFError, KeyboardInterrupt):
                    break
                
                if self.server_process is None:
                    break

                if self.server_process.poll() is not None:
                    break

                if self.server_process.stdin is None:
                    break

                self.send_command(command)
                
        self.command_thread = threading.Thread(target=command_loop, daemon=True)
        self.command_thread.start()

        def output_loop():
            assert self.server_process is not None
            if (self.server_process.stdout is not None):
                for line in self.server_process.stdout:
                    self.__on_new_line(line.strip("\n"))
       
        self.output_thread = threading.Thread(target=output_loop, daemon=True)
        self.output_thread.start()

        def try_graceful_stop(self):
            try:
                if (self.server_process and self.server_process.stdin and self.server_process.poll() is None):
                    self.send_command("stop")
                    return True
            except Exception as e:
                self.logger.error("Failed to send stop command to server: " + str(e))
                pass
            return False

        @self.shutdown_handler.on_shutdown
        def on_shutdown():
            def after_server_stopped():
                self.state_handler.set(ServerState.STOPPED)
                self.output_thread.join(timeout=5)

                if (self.session.app is not None and self.session.app.is_running):
                    self.session.app.exit()
                self.logger.publish_minestrapper_log()

            self.state_handler.set(ServerState.STOPPING)
            if (self.server_process is not None and self.server_process.stdin is not None and self.server_process.poll() is None):
                try_graceful_stop(self)

                self.server_process.wait(timeout=3)
                after_server_stopped()
            else:
                after_server_stopped()

        self.logger.info("Server started successfully")
        handle_built_in_features(self)

        def detect_server_exit():
            assert self.server_process is not None
            self.server_process.wait()
            self.logger.info("Server process has exited")
            self.shutdown_handler.request_shutdown()
        
        threading.Thread(target=detect_server_exit, daemon=True).start()

    def wait_loop(self):
        self.shutdown_handler.wait_for_shutdown_complete()
        input("Press Enter to exit...")

    def __on_new_line(self, line : str):
        new_state = get_state_from_line(line)
        if (new_state is not None and new_state != self.state_handler.get()):
            self.state_handler.set(new_state)

        self.logger.forwarded_log(line)

        if (self.new_line_callbacks):
            for callback in self.new_line_callbacks:
                callback(line)

    def on_new_line(self, function: Callable):
        self.new_line_callbacks.append(function)
        return function

    def send_command(self, command: str):
        if (self.server_process is None or self.server_process.stdin is None or self.server_process.poll() is not None):
            self.logger.warning("Cannot send command, server process is not running")
            return

        with self.__stdin_lock:
            try:
                self.server_process.stdin.write(command.strip() + "\n")
                self.server_process.stdin.flush()
            except Exception as e:
                self.logger.error("Failed to send command to server: " + str(e))
