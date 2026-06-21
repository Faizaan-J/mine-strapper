import os
import sys

import ctypes

from typing import TYPE_CHECKING

from .state_styles.state_styles import StateStyle

if TYPE_CHECKING:
    from ..server import Server

FEATURES = {
    "state_styles": {
        "class": StateStyle,
        "enabled_by_default": True
    }
}

def handle_built_in_features(server: "Server"):
    for feature_name, feature_info in FEATURES.items():
        target_feature = server.config_handler.get_config()["features"].get(feature_name)
        if target_feature is None: continue

        if target_feature.get("feature_enabled", feature_info["enabled_by_default"]):
            feature_class = feature_info["class"]
            feature_instance = feature_class(server)
            feature_instance.run()
