import threading
from typing import Self


class WalletActivity(threading.Thread):
    """Thread for randomly depositing or withdrawing from accounts."""

    thread_id: int
    name: str

    def __init__(self: Self, thread_id: int, name: str) -> None:
        """Construct."""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self: Self) -> None:
        """Start thread."""
        print("Starting " + self.name)
        print("Exiting " + self.name)
