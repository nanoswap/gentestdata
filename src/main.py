import uuid
import random
import threading
from typing import Self

from ipfsclient.ipfs import Ipfs
from bizlogic.loan.writer import LoanWriter
from bizlogic.application import LoanApplicationWriter
from bizlogic.vouch import VouchWriter

ipfsclient = Ipfs()
num_users = 100

# Create user id's with mock nano wallets
users = [uuid.uuid4() for _ in range(num_users)]
accounts = {user: random.randint(0, 1000000) for user in users}


class WalletActivity(threading.Thread):
    """Thread for randomly depositing or withdrawing from accounts."""

    thread_id: int
    name: str
    counter: int

    def __init__(self: Self, thread_id: int, name: str, counter: int) -> None:
        """Construct."""
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self: Self) -> None:
        """Start thread."""
        print("Starting " + self.name)
        print("Exiting " + self.name)

# Thread for randomly creating vouches between users

# Thread for randomly creating/withdrawing loan applications

# Thread for randomly creating loan offers

# Thread for randomly accepting loan offers

# Thread for randomly making loan payments

# Clean up: delete everything
