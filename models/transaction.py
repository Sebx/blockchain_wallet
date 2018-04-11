class Transaction(object):
    def __init__(self, id, amount, souce_account_id, destination_account_id, timestamp):
        self.id = id
        self.amount = amount
        self.souce_account_id = souce_account_id
        self.destination_account_id = destination_account_id
        self.timestamp = timestamp
    
    def dump(self):
        return "Transaction: {0}, Source account: {1}, Detination account: {2} amount: {3}, Date: {4}" \
        .format(self.id, self.souce_account_id, self.destination_account_id, self.amount, self.timestamp.strftime("%y-%m-%d-%H-%M"))