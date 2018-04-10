class Account(object):
    def __init__(self, name, account_number, initial_amount, user):
        self.name = name
        self.no = account_number
        self.balance = initial_amount
        self.user = user

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise RuntimeError('Amount greater than available balance.')
        self.balance -= amount

    def dump(self):
        s = '%s, %s, balance: %s' % (self.name, self.no, self.balance)
        print s