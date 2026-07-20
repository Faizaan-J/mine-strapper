from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..server import Server

class Feature:
    def __init__(self, name: str, description: str, server: "Server"):
        self.name = name
        self.description = description
        self.server = server

    def run(self):
        raise NotImplementedError("Feature must implement the run method")