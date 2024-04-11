import sys

from obsws_python import ReqClient as OBSClient

from obs_monitor_switcher.listeners import listeners
from obs_monitor_switcher.config import Config
from obs_monitor_switcher.obs import hide_scene_item, show_scene_item

config = Config.from_toml_file(sys.argv[1])


def main():
    obs = OBSClient(**config.connection._asdict())
    listener = listeners.get(config.window_manager)

    if not listener:
        print(f"Window manager {config.window_manager!r} is not supported yet.")

    def callback(monitor: str) -> None:
        actions = config.monitors.get(monitor)
        if not actions:
            print(f"Monitor {monitor} not found in config, doing nothing")
            return

        print(f"Monitor is {monitor}, hiding {actions.hide} and showing {actions.show}")
        if actions.hide:
            show_scene_item(obs, config.obs, actions.hide)
        if actions.show:
            hide_scene_item(obs, config.obs, actions.show)

    listener.listen(callback)


if __name__ == "__main__":
    main()
