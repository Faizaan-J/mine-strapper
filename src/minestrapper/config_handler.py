import os
import json
from enum import Enum

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

def dict_to_key_value(dictionary: dict) -> str:
    key_value_string = ""
    for key, value in dictionary.items():
        key_value_string += f"{key}={value}\n"
    return key_value_string

class ConfigHandler:
    def __init__(self, path: str):
        self.path = path
        self.config_json = os.path.join(self.path, "/minestrapper/config.json")
        self.server_properties_file = os.path.join(self.path, "server.properties")

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
        with open(self.server_properties_file, 'w') as f:            
            f.write(dict_to_key_value(self.__server_properties))