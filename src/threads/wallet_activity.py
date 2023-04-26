from typing import Self
import logging
import asyncio
import random
from src.mock import User, Wallet

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

withdraw_chance = 0.1
deposit_chance = 0.1


class WalletActivity():
    """Thread for randomly depositing or withdrawing from accounts."""

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
        log.debug("Starting " + self.name)
        while self.tick_count < self.max_ticks:
            self.tick_count += 1
            log.debug("Running " + self.name)
            await self.tick()
            await asyncio.sleep(0)  # allow the event loop to switch to another function  # noqa: E501

        log.debug("Exiting " + self.name)

    async def tick(self: Self) -> None:
        """Iterate."""
        rand = random.random()
        rand -= withdraw_chance
        if rand < 0:
            user = await User.get_random()
            balance = await Wallet.balance(user)
            withdraw = await WalletActivity.how_much_to_withdraw(balance)
            await Wallet.withdraw(user, withdraw)
            return

        rand -= deposit_chance
        if rand < 0:
            user = await User.get_random()
            deposit = await WalletActivity.how_much_to_deposit()
            await Wallet.deposit(user, deposit)
            return

    @staticmethod
    async def how_much_to_withdraw(balance: int) -> int:
        return random.randint(0, balance)

    @staticmethod
    async def how_much_to_deposit() -> int:
        return random.randint(0, 1000000)
