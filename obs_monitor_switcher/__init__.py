import os
import socket
import sys
from pathlib import Path
from typing import Callable

import toml
from obsws_python import ReqClient as OBSClient

config = toml.load(sys.argv[1])

print(f"Using config: {config}")


def hyprland_websocket_path():
    return str(
        Path("/tmp/hypr") / os.getenv("HYPRLAND_INSTANCE_SIGNATURE") / ".socket2.sock"
    )


def scene_item_id(obs, scene, item):
    return obs.get_scene_item_id(scene, item).scene_item_id


def hide_scene_item(obs, scene, item):
    obs.set_scene_item_enabled(scene, scene_item_id(obs, scene, item), False)


def show_scene_item(obs, scene, item):
    obs.set_scene_item_enabled(scene, scene_item_id(obs, scene, item), True)


# maps monitor names to tuples: [item to show, item to hide]
# config = {
#     "DVI-D-1": ("Right monitor", "Left monitor"),
#     "HDMI-A-1": ("Left monitor", "Right monitor"),
# }


class Listener:
    @classmethod
    def listen(self, callback: Callable[[str], None]) -> None:
        """
        Calls callback with the monitor name when the monitor changes.
        """
        raise NotImplementedError("Please implement listen.")


class HyprlandListener(Listener):
    @staticmethod
    def socket_path():
        return (
            Path("/tmp/hypr")
            / os.getenv("HYPRLAND_INSTANCE_SIGNATURE")
            / ".socket2.sock"
        )

    @classmethod
    def listen(self, callback):
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.connect(str(self.socket_path()))
            while True:
                op, detail, *_ = sock.recv(1024).decode("utf-8").strip().split(">>")
                if op == "focusedmon":
                    monitor = detail.split(",")[0]
                    callback(monitor)


listeners = {"hyprland": HyprlandListener}


def main():
    print(f"Connecting to OBS with connection {config['connection']}")
    obs = OBSClient(**config["connection"])

    scene = config["obs"]["scene"]
    print(f"Targetting scene {scene}")

    listener = listeners.get(config["window_manager"])
    print(f"Using listener {listener}")
    if not listener:
        print(f"Window manager {config['window_manager']} is not supported yet.")

    def callback(monitor: str) -> None:
        actions = config["monitors"].get(monitor)
        if not actions:
            print(f"Monitor {monitor} not found in config, doing nothing")
            return

        to_show = actions.get("show")
        to_hide = actions.get("hide")

        print(f"Monitor is {monitor}, hiding {to_hide} and showing {to_show}")
        if to_show:
            show_scene_item(obs, scene, to_show)
        if to_hide:
            hide_scene_item(obs, scene, to_hide)

    listener.listen(callback)


if __name__ == "__main__":
    main()
