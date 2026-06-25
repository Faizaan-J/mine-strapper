import threading

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from minestrapper.logger import LogLevel

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
            "An HTTP server to serve a custom resource pack for your Minecraft Server.", 
            server
        )

        self.config = self.server.config_handler.get_config()['features']['server_resource_pack']

        self.path = resolve_server_path(self.config["path"], self.server.path)
        self.ip, self.port = get_clean_address(self.config.get("ip", ""), self.config.get("port", ""))

    def log(self, level: LogLevel, message: str):
        self.server.logger.log(level, f"Resource Pack Server: {message}")

    def get_sha1(self, file_path: Path) -> str:
        sha1 = hashlib.sha1()

        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                sha1.update(chunk)

        return sha1.hexdigest()

    def start_resource_pack_server(self):
        file_path = self.path
        server_instance = self.server
        log_method = self.log
        
        class ResourcePackRequestHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                log_level = LogLevel.INFO
                if (len(args) >= 2):
                    try:
                        code = int(args[1])
                        if (code >= 500):
                            log_level = LogLevel.ERROR
                        elif (code >= 400):
                            log_level = LogLevel.WARNING
                    except Exception as e:
                        pass
                log_method(log_level, format % args)

            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-Type", "application/zip")
                self.send_header("Content-Length", str(os.path.getsize(file_path)))
                self.end_headers()
                
                with open(file_path, "rb") as resource_pack_file:
                    while chunk := resource_pack_file.read(65536):
                        self.wfile.write(chunk)
                    
        server = HTTPServer((self.ip, self.port), ResourcePackRequestHandler)
        threading.Thread(target=server.serve_forever, daemon=True).start()

        return server

    def run(self):
        self.resource_pack_server = self.start_resource_pack_server()
        resource_pack_url = f"http://{self.ip}:{self.port}/"

        self.server.logger.info(f"Started resource pack server at {resource_pack_url}.")
        self.server.config_handler.set_server_properties("resource-pack", resource_pack_url)
        self.server.config_handler.set_server_properties("resource-pack-sha1", self.get_sha1(self.path))
