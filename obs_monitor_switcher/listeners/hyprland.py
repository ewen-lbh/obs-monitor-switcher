import os
from pathlib import Path
import socket
from obs_monitor_switcher.core import Listener


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
