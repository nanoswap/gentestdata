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
num_users = 100
min_wallet_size = 0
max_wallet_size = 1000000
execution_duration = 10
max_ticks = 100

log = logging.getLogger(__name__)
logging.basicConfig(filename=f'logs_{__name__}.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

# Create user id's with mock nano wallets
users = [uuid.uuid4() for _ in range(num_users)]
wallets = {user: random.randint(min_wallet_size, max_wallet_size) for user in users}

threads = [
    AcceptLoanOffer(1, 'accept-loan', log, max_ticks),
    CreateApplication(2, 'create-application', log, max_ticks),
    CreateLoanOffer(3, 'create-loan-offer', log, max_ticks),
    CreatePayment(4, 'create-payment', log, max_ticks),
    CreateVouch(5, 'create-vouch', log, max_ticks),
    WalletActivity(6, 'wallet-activity', log, max_ticks),
    WithdrawApplication(7, 'withdraw-application', log, max_ticks)
]


async def main():
    """Execute threads."""
    tasks = [asyncio.create_task(thread.run()) for thread in threads]
    asyncio.gather(*tasks)

asyncio.gather(main())
sys.stdout.flush()
sys.stderr.flush()
