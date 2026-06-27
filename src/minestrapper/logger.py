import os
import threading

from enum import Enum
from pathlib import Path
from datetime import datetime

from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import ANSI

from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .server import Server

class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class Logger:
    def __init__(self, server: "Server"):
        self.server = server
        self.line_transformers: list[Callable[[str], str]] = []

        logs_folder = Path(server.path) / "logs"
        logs_folder.mkdir(parents=True, exist_ok=True)
        self.log_file = logs_folder / "latest.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        self.minestrapper_log_file = logs_folder / "latest-minestrapper.log"
        self.minestrapper_log_file.parent.mkdir(parents=True, exist_ok=True)
        self.minestrapper_log_file.touch(exist_ok=True)
        with open(self.minestrapper_log_file, "w", encoding="utf-8") as log:
            log.write("")

        self.info("Initialized Minestrapper Logger successfully.")

    def add_line_transformer(self, transformer: Callable[[str], str]):
        self.line_transformers.append(transformer)
        return transformer
    
    def __write_line_log(self, line: str):
        with open(self.minestrapper_log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def print_with_transformation(self, message: str):
        for transformer in self.line_transformers:
            message = transformer(message)

        print_formatted_text(ANSI(message))

    def forwarded_log(self, message: str):
        self.print_with_transformation(message)
        self.__write_line_log(message)

    def log(self, level: LogLevel, *message: str):
        timestamp = f"[{datetime.now().strftime('%H:%M:%S')}]"
        log_level_label = f"[Minestrapper/{level.value}]:"
        full_line = f"{timestamp} {log_level_label} {' '.join(message)}"

        self.print_with_transformation(full_line)
        self.__write_line_log(full_line)

    def publish_minestrapper_log(self):
        with open(self.minestrapper_log_file, "r", encoding="utf-8") as f:
            minestrapper_log_content = f.read()
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(minestrapper_log_content)
        self.info("Published Minestrapper log to latest.log.")

    def info(self, *message: str):
        self.log(LogLevel.INFO, *message)

    def warning(self, *message: str):
        self.log(LogLevel.WARNING, *message)

    def error(self, *message: str):
        self.log(LogLevel.ERROR, *message)
