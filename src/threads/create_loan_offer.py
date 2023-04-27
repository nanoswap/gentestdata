from typing import Self
import logging
import asyncio
import random
import datetime
from bizlogic.loan.writer import LoanWriter
from bizlogic.loan.repayment import PaymentSchedule
from src import utils
import pandas as pd
from src.mock import User, Wallet
from ipfsclient.ipfs import Ipfs

log = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

create_chance = 0.2
ipfsclient = Ipfs()


class CreateLoanOffer():
    """Thread for randomly creating loan offers."""

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
        rand -= create_chance
        if rand > 0:
            return

        # pick random lender and borrowers
        borrower = await User.get_random()
        lender = await User.get_random()

        if borrower == lender:
            return

        # generate loan offer parameters
        lender_balance = await Wallet.balance(lender)
        principal = await CreateLoanOffer.principal(lender_balance)
        interest = await CreateLoanOffer.interest()
        duration = await CreateLoanOffer.duration()
        payments = await CreateLoanOffer.number_of_payments()
        offer_expiry_date = await CreateLoanOffer.expiry()

        # TODO: return to wallet if the offer expires
        await Wallet.withdraw(lender, principal)

        payment_schedule = PaymentSchedule.create_payment_schedule(
            amount=principal,
            interest_rate=interest,
            total_duration=pd.Timedelta(duration, unit='ns'),
            number_of_payments=payments,
            first_payment=offer_expiry_date
        )

        loan_writer = LoanWriter(
            ipfsclient,
            borrower,
            lender,
            principal,
            payment_schedule,
            offer_expiry=offer_expiry_date
        )

        loan_writer.write()

    @staticmethod
    async def principal(balance: int) -> int:
        return random.randint(0, balance)

    @staticmethod
    async def interest() -> int:
        return 1 + random.random()

    @staticmethod
    async def duration() -> int:
        return random.randint(1000, 1000000)

    @staticmethod
    async def number_of_payments() -> int:
        return random.randint(3, 20)

    @staticmethod
    async def expiry():
        days = random.randint(10, 30)
        return datetime.datetime.now() + datetime.timedelta(days=days)
