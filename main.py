import uuid
import random
import asyncio
import logging
import sys

from ipfsclient.ipfs import Ipfs
from bizlogic.loan.writer import LoanWriter
from bizlogic.application import LoanApplicationWriter
from bizlogic.vouch import VouchWriter

from src.threads.accept_loan_offer import AcceptLoanOffer
from src.threads.create_application import CreateApplication
from src.threads.create_loan_offer import CreateLoanOffer
from src.threads.create_payment import CreatePayment
from src.threads.create_vouch import CreateVouch
from src.threads.wallet_activity import WalletActivity
from src.threads.withdraw_application import WithdrawApplication

from src.mock import wallets
from pandas import Series
import matplotlib.pyplot as plt


ipfsclient = Ipfs()
max_ticks = 100

log = logging.getLogger(__name__)
logging.basicConfig(filename=f'logs/{__name__}.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def main() -> None:
    """Execute threads."""

    # Check initial conditions
    wallets_before = Series(wallets, index=wallets.keys())

    # Run simulation
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(
        AcceptLoanOffer(1, 'accept-loan', max_ticks).run(),
        CreateApplication(2, 'create-application', max_ticks).run(),
        CreateLoanOffer(3, 'create-loan-offer', max_ticks).run(),
        CreatePayment(4, 'create-payment', max_ticks).run(),
        CreateVouch(5, 'create-vouch', max_ticks).run(),
        WalletActivity(6, 'wallet-activity', max_ticks).run(),
        WithdrawApplication(7, 'withdraw-application', max_ticks).run()
    ))
    loop.close()

    # Check conditions after simulation
    wallets_after = Series(wallets, index=wallets.keys())

    plt.plot(wallets_before, color='red')
    plt.plot(wallets_after, color='blue')
    plt.show()


if __name__ == "__main__":
    main()
