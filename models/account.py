class Account(object):
    def __init__(self, name, account_number, initial_amount, user_id):
        self.name = name
        self.no = account_number
        self.balance = initial_amount
        self.user_id = user_id

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise RuntimeError('Amount greater than available balance.')
        self.balance -= amount

    def dump(self):
        return "Account: {0}, no: {1}, balance: {2}".format(self.name, self.no, self.balance)