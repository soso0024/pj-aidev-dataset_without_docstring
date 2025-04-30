class User:
    def __init__(self, id: int, name: str, balance: float):
        self.id = id
        self.name = name
        self.balance = balance

    def debit(self, amount: float):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        return self.balance

    def credit(self, amount: float):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.balance += amount
        return self.balance
