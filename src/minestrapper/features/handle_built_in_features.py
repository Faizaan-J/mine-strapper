from typing import TYPE_CHECKING

from .state_styles.state_styles import get_new_print_method_from_state

if TYPE_CHECKING:
    from ..server import Server

def handle_built_in_features(server: "Server"):
    if server.config_handler.get_config()['features']['state_styles']["feature_enabled"]["enabled"]:
        @server.on_state_change
        def update_print_method():
            server.printMethod = get_new_print_method_from_state(server.server_state)