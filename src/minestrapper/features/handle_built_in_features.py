from typing import TYPE_CHECKING

from .state_styles.state_styles import get_colored_text

if TYPE_CHECKING:
    from ..server import Server

def handle_built_in_features(server: "Server"):
    if server.config_handler.get_config()['features']['state_styles']["feature_enabled"]["enabled"]:
        @server.add_line_transformer
        def state_styles_transformer(line: str):
            return get_colored_text(line, server.server_state)