import threading

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from pathlib import Path

from minestrapper.features.feature import Feature

from typing import TYPE_CHECKING

from minestrapper.features.server_resource_pack.path_resolver import resolve_server_path
if TYPE_CHECKING:
    from ....minestrapper.server import Server

from .address_validator import get_clean_address

import hashlib

class ServerResourcePack(Feature):
    def __init__(self, server: "Server"):
        super().__init__(
            "Server Resource Pack", 
            "Makes a http server to serve a custom resource pack for your Minecraft Server and adds the link it to server.properties", 
            server
        )

        self.config = self.server.config_handler.get_config()['features']['server_resource_pack']

        self.path = resolve_server_path(self.config["path"], self.server.path)
        self.ip, self.port = get_clean_address(self.config.get("ip", ""), self.config.get("port", ""))

    def get_sha1(self, file_path: Path) -> str:
        sha1 = hashlib.sha1()

        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                sha1.update(chunk)

        return sha1.hexdigest()

    def start_resource_pack_server(self):
        file_path = self.path
        server_instance = self.server
        
        class ResourcePackRequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                server_instance.log_line(f"Resource Pack Server: {format % args}")

            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Length", str(os.path.getsize(file_path)))
                self.end_headers()
                
                with open(file_path, "rb") as resource_pack_file:
                    chunk = resource_pack_file.read(65536)
                    while chunk:
                        self.wfile.write(chunk)
                        chunk = resource_pack_file.read(65536)
                    
        server = HTTPServer((self.ip, self.port), ResourcePackRequestHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()

        return server

    def run(self):
        self.resource_pack_server = self.start_resource_pack_server()
        resource_pack_url = f"http://{self.ip}:{self.port}/"

        self.server.log_line(f"Started resource pack server at {resource_pack_url}.")
        self.server.config_handler.set_server_properties("resource-pack", resource_pack_url)
        self.server.config_handler.set_server_properties("resource-pack-sha1", self.get_sha1(self.path))
