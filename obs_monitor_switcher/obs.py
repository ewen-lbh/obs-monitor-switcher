from obsws_python import ReqClient

from obs_monitor_switcher.config import OBSConfig


def scene_item_id(obs: ReqClient, config: OBSConfig, item: str) -> str:
    return obs.get_scene_item_id(config.scene, item).scene_item_id


def hide_scene_item(obs: ReqClient, config: OBSConfig, item: str):
    obs.set_scene_item_enabled(config.scene, scene_item_id(obs, config, item), False)


def show_scene_item(obs: ReqClient, config: OBSConfig, item: str):
    obs.set_scene_item_enabled(config.scene, scene_item_id(obs, config, item), True)
