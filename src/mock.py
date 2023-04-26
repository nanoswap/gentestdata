import uuid
import random


num_users = 100
min_wallet_size = 0
max_wallet_size = 1000000

# Create user id's with mock nano wallets
users = [str(uuid.uuid4()) for _ in range(num_users)]
wallets = {
    user: random.randint(min_wallet_size, max_wallet_size)
    for user in users
}


class User():
    @staticmethod
    async def get_random() -> str:
        return random.choice(users)

class Wallet():
    @staticmethod
    async def deposit(user: str, amount: int) -> None:
        wallets[user] += amount

    @staticmethod
    async def withdraw(user: str, amount: int) -> None:
        wallets[user] -= amount

    @staticmethod
    async def balance(user: str) -> int:
        return wallets[user]
