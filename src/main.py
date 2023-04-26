import uuid
import random

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

# Create user id's with mock nano wallets
users = [uuid.uuid4() for _ in range(num_users)]
wallets = {user: random.randint(0, 1000000) for user in users}

threads = [
    AcceptLoanOffer(1, 'accept-loan'),
    CreateApplication(2, 'create-application'),
    CreateLoanOffer(3, 'create-loan-offer'),
    CreatePayment(4, 'create-payment'),
    CreateVouch(5, 'create-vouch'),
    WalletActivity(6, 'wallet-activity'),
    WithdrawApplication(7, 'withdraw-application')
]

# Start Threads
for thread in threads:
    thread.run()

# Clean up: delete everything
# TODO
