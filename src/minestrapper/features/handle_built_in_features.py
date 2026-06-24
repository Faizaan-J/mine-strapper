import os
import sys

from typing import TYPE_CHECKING

from .state_styles.state_styles import StateStyle
from .server_resource_pack.server_resource_pack import ServerResourcePack

if TYPE_CHECKING:
    from ..server import Server

FEATURES = {
    "state_styles": {
        "class": StateStyle,
        "enabled_by_default": True
    },
    "server_resource_pack": {
        "class": ServerResourcePack,
        "enabled_by_default": False
    }
}

def handle_built_in_features(server: "Server"):
    for feature_key, feature_info in FEATURES.items():
        target_feature = server.config_handler.get_config()["features"].get(feature_key)
        if target_feature is None: continue

        if target_feature.get("feature_enabled", feature_info["enabled_by_default"]):
            feature_class = feature_info["class"]
            feature_instance = feature_class(server)
            server.logger.info(f"Feature '{feature_instance.name}' has been started.")
            try:
                feature_instance.run()
            except Exception as e:
                server.logger.error(f"An error occurred while running the feature '{feature_instance.name}': {e}")
