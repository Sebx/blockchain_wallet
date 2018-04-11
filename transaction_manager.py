from random import randint
import datetime
from models.account import Account
from models.transaction import Transaction

class TransactionManager:
    def __init__(self, users):
        self.transactions = []
        self.users = users
        # Accounts for the users
        self.accounts = [Account("Salary account {0}".format(user.name), randint(1000, 9000), 1000, user.id) for user in users]
        
    def apply_transaction(self, index, amount, sender_account_no, destination_account_no):
        date = datetime.datetime.now()
        sender_account = next(iter([account for account in self.accounts if account.no == sender_account_no]), None)
        destination_account = next(iter([account for account in self.accounts if account.no == destination_account_no]), None)

        if(sender_account != None and destination_account != None):
            transaction = Transaction(index, amount, sender_account.no, destination_account.no, date)
            self.transactions.append(transaction)
    
            sender_account.withdraw(amount)
            destination_account.deposit(amount)

    def report_accounts(self):
        return [account.dump() for account in self.accounts]
        
    def report_transactions(self):
        return  [transaction.dump() for transaction in self.transactions]