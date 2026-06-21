import os
import sys

import ctypes

from typing import TYPE_CHECKING

from .state_styles.state_styles import StateStyle

if TYPE_CHECKING:
    from ..server import Server

def handle_built_in_features(server: "Server"):
    if server.config_handler.get_config()['features']['state_styles']["feature_enabled"]["enabled"]:
        state_style_feature = StateStyle(server)
        state_style_feature.run()