import uuid
import random
import asyncio
import logging
import sys

from ipfsclient.ipfs import Ipfs
from bizlogic.loan.writer import LoanWriter
from bizlogic.application import LoanApplicationWriter
from bizlogic.vouch import VouchWriter

from threads.accept_loan_offer import AcceptLoanOffer
from threads.create_application import CreateApplication
from threads.create_loan_offer import CreateLoanOffer
from threads.create_payment import CreatePayment
from threads.create_vouch import CreateVouch
from threads.wallet_activity import WalletActivity
from threads.withdraw_application import WithdrawApplication


ipfsclient = Ipfs()
max_ticks = 100

log = logging.getLogger(__name__)
logging.basicConfig(filename=f'logs/{__name__}.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def main() -> None:
    """Execute threads."""
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


if __name__ == "__main__":
    main()
