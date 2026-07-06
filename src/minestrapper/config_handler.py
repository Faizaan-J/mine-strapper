from typing import TYPE_CHECKING

import os
import json
from enum import Enum

if TYPE_CHECKING:
    from .server import Server

class FileType(Enum):
    CONFIG = "config"
    SERVER_PROPERTIES = "server_properties"

def key_value_to_dict(unpacked_string: list) -> dict:
    dict = {}

    for line in unpacked_string:
        key_value = line.strip().split('=')
        if len(key_value) == 2:
            dict[key_value[0]] = key_value[1]

    return dict

class ConfigHandler:
    def __init__(self, server: "Server"):
        self.server = server
        self.config_json = os.path.join(server.path, "minestrapper", "config.json")
        self.server_properties_file = os.path.join(server.path, "server.properties")

    def __open(self, file_type: FileType):
        if file_type == FileType.CONFIG:
            self.__config = json.load(open(self.config_json, 'r'))
        elif file_type == FileType.SERVER_PROPERTIES:
            with open(self.server_properties_file, 'r') as f:
                self.__server_properties = key_value_to_dict(f.readlines())

    def get_config(self):
        self.__open(FileType.CONFIG)
        return self.__config
    
    def get_server_properties(self):
        self.__open(FileType.SERVER_PROPERTIES)
        return self.__server_properties
    
    def set_server_properties(self, key : str, value : str):
        self.__open(FileType.SERVER_PROPERTIES)
        self.__server_properties[key] = value
        
        with open(self.server_properties_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        key_found = False
        for index, line in enumerate(lines):
            line = line.strip()

            if (line.startswith("#") or "=" not in line):
                continue
            
            current_key, _ = line.split("=", 1)

            if (current_key == key):
                key_found = True
                lines[index] = f"{key}={value}\n"
                break
            
        if (not key_found):
            new_line = f"{key}={value}"
            lines.append(f"{new_line}\n")
            self.server.logger.warning(f"Property '{key}' not found in server.properties. Appended line: '{new_line}'")

        with open(self.server_properties_file, "w", encoding="utf-8") as f:
            f.writelines(lines)
