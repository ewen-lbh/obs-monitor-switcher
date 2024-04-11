# OBS Monitor Switcher

Hides and shows sources on an OBS scene depending on the active monitor.

Uses websockets to communicate with both your window manager (only [Hyprland](https://hyprland.org) is supported at the moment, see [Implementing new listeners](#implementing-new-listeners)) and OBS.

## Requirements

Requires OBS to have Websocket support. 

### Arch Linux

For Arch Linux users, as of now, the `obs-studio` package in the official repositories does not have Websocket support. You can use the `obs-studio-git` package from the AUR instead. [source](https://wiki.archlinux.org/title/Open_Broadcaster_Software#Global_shortcuts_in_KDE_not_working)

## Installation

### With [pipx](https://pipx.pypa.io/)

```bash
pipx install git+https://github.com/ewen-lbh/obs-monitor-switcher
```

### Manually

Requires [Poetry](https://python-poetry.org/)

```bash
git clone https://github.com/ewen-lbh/obs-monitor-switcher
cd obs-monitor-switcher
poetry shell
poetry install
```

## Usage

See [Configuration](#configuration) to create the `config.toml` file.

```bash
obs-monitor-switcher config.toml
```

## Configuration is done through a TOML file:

An example configuration file is available at [`example-config.toml`](./example-config.toml).

```toml
window_manager = "hyprland" # only "hyprland" is supported at the moment


[connection]
# OBS websocket parameters. See Tools > Websocket Server Settings in OBS

host = "localhost" # the IP address, or localhost if OBS is running on the same machine
port = 4455
password = "" # use an empty string if authentication is disabled

[obs]
scene = "Stream" # The name of the scene to use

# The automation rules.
# Each rule is a section with the name `monitors.<monitor_name>`.
# and contains two properties: `show` and `hide`.
# Below is an example for a dual monitor setup.

[monitors.DVI-D-1]
# When the monitor "DVI-D-1" is active...
show = "Right monitor" # show the source named "Right monitor"
hide = "Left monitor" # hide the source named "Left monitor"

[monitors.HDMI-A-1]
# When the monitor "HDMI-A-1" is active...
show = "Left monitor" # show the source named "Left monitor"
hide = "Right monitor" # hide the source named "Right monitor"
```

## Contributing

### Implementing new listeners

Just create a new file in `obs_monitor_switcher/listeners/` that implements the `obs_monitor_switcher.core.Listener` interface.

Then, register your listener by adding it to the `listeners` dict in `obs_monitor_switcher/listeners/__init__.py`.

The key should be the name of the window manager, and the value should be the listener class.

That key corresponds to the value of `window_manager` in the configuration file.
