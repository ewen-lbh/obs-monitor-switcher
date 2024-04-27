from collections.abc import Iterable
from obsws_python import ReqClient

from obs_monitor_switcher.config import OBSConfig


def scene_item_id(obs: ReqClient, scene: str, item: str) -> str:
    return obs.get_scene_item_id(scene, item).scene_item_id

def selected_scenes(obs: ReqClient, config: OBSConfig) -> Iterable[str]:
    try:
        # FIXME
        scenes = [ s['sceneName'] for s in obs.get_scene_list().scenes ]
    except:
        scenes = []
    for scene in scenes:
        if scene in config.scenes or not config.scenes:
            yield scene


def hide_scene_item(obs: ReqClient, config: OBSConfig, item: str):
    for scene in selected_scenes(obs, config):
        try:
            obs.set_scene_item_enabled(scene, scene_item_id(obs, scene, item), False)
        except: 
            pass


def show_scene_item(obs: ReqClient, config: OBSConfig, item: str):
    for scene in selected_scenes(obs, config):
        try:
            obs.set_scene_item_enabled(scene, scene_item_id(obs, scene, item), True)
        except: 
            pass
