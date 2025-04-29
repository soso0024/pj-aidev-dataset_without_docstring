from datetime import datetime

class Order:
    def __init__(self, user_id: int, amount: float):
        self.user_id = user_id
        self.amount = amount
        self.timestamp = datetime.utcnow()

    def summary(self):
        return f"Order for user {self.user_id}: ${self.amount:.2f} at {self.timestamp.isoformat()}"

