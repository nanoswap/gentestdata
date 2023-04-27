from typing import Self
import logging
import asyncio
import random
from ipfsclient.ipfs import Ipfs
from src import utils
import pandas as pd
from src.mock import User, Wallet

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

withdraw_chance = 0.2
ipfsclient = Ipfs()


class WithdrawApplication():
    """Thread for randomly withdrawing loan applications."""

    thread_id: int
    name: str
    max_ticks: int
    tick_count: int

    def __init__(
            self: Self,
            thread_id: int,
            name: str,
            max_ticks: int) -> None:
        """Construct."""
        self.thread_id = thread_id
        self.name = name
        self.log = log
        self.max_ticks = max_ticks
        self.tick_count = 0

    async def run(self: Self) -> None:
        """Start thread."""
        log.info("Starting " + self.name)
        while self.tick_count < self.max_ticks:
            self.tick_count += 1
            log.info("Running " + self.name)
            await self.tick()
            await asyncio.sleep(0)  # allow the event loop to switch to another function  # noqa: E501

        log.info("Exiting " + self.name)

    async def tick(self: Self) -> None:
        """Iterate."""
        rand = random.random()
        rand -= withdraw_chance
        if rand < 0:
            pass
