from typing import Callable


class Listener:
    @classmethod
    def listen(self, callback: Callable[[str], None]) -> None:
        """
        Calls callback with the monitor name when the monitor changes.
        """
        raise NotImplementedError("Please implement listen.")
