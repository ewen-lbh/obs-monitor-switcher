from typing import NamedTuple


class ConnectionConfig(NamedTuple):
    """
    Configuration for connecting to OBS.


    ```toml
    [connection]
    host = "localhost"
    port = 4455
    password = ""
    ```
    """

    host: str
    port: int
    password: str


class OBSConfig(NamedTuple):
    """
    Configuration for OBS.
    Leave `scene` empty to change all scenes.


    ```toml
    [obs]
    scenes = ["Stream"]
    ```
    """

    scenes: list[str]


class MonitorConfig(NamedTuple):
    """
    Configuration for a monitor.


    ```toml
    [monitors.DVI-D-1]
    show = "Right monitor"
    hide = "Left monitor"
    ```
    """

    show: str
    hide: str


class Config(NamedTuple):
    """
    An example TOML configuration represented by this class:


    ```toml
    window_manager = "hyprland"

    [connection]
    host = "localhost"
    port = 4455
    password = ""

    [obs]
    scene = "Stream"

    [monitors.DVI-D-1]
    show = "Right monitor"
    hide = "Left monitor"

    [monitors.HDMI-A-1]
    show = "Left monitor"
    hide = "Right monitor"
    ```
    """

    window_manager: str

    connection: ConnectionConfig
    obs: OBSConfig
    monitors: dict[str, MonitorConfig]

    @classmethod
    def from_toml_file(cls, path: str) -> "Config":
        import toml

        with open(path) as f:
            return cls.from_dict(toml.load(f))

    @classmethod
    def from_dict(cls, toml: dict) -> "Config":
        if not toml["window_manager"]:
            raise ValueError("window_manager is required")

        if not toml["connection"]:
            raise ValueError("connection is required")

        if not toml["obs"]:
            raise ValueError("obs is required")

        if not toml["monitors"]:
            raise ValueError("specify at least one monitor rule")

        return cls(
            window_manager=toml["window_manager"],
            connection=ConnectionConfig(**toml["connection"]),
            obs=OBSConfig(**toml["obs"]),
            monitors={k: MonitorConfig(**v) for k, v in toml["monitors"].items()},
        )
