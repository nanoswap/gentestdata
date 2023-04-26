import uuid
import random


num_users = 100
min_wallet_size = 0
max_wallet_size = 1000000
max_ticks = 100

# Create user id's with mock nano wallets
users = [uuid.uuid4() for _ in range(num_users)]
wallets = {
    user: random.randint(min_wallet_size, max_wallet_size)
    for user in users
}
