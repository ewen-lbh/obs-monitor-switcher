# OBS Monitor Switcher

Hides and shows sources on an OBS scene depending on the active monitor.

Uses websockets to communicate with both your window manager (only [Hyprland](https://hyprland.org) is supported at the moment) and OBS.

## Installation

For now, installation is manual (and requires [Poetry](https://python-poetry.org/)):

```bash
git clone https://github.com/ewen-lbh/obs-monitor-switcher
cd obs-monitor-switcher
poetry install
```

## Usage

See [Configuration](#configuration) to create the `config.toml` file.

```bash
poetry shell
poetry install
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
