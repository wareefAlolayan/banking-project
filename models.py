
class Account ():
    def __init__(self, kind, balance=0):
        self.kind = kind # check or save"
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        pass

    def withdraw(self, amount):
        pass

#'monday standup'
class Customer ():
    def __init__(self , id , first_name , last_name , password , checking_balance , savings_balance):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.checking = Account("checking", checking_balance)
        self.savings = Account("savings", savings_balance)

    @property
    def full_name(self):
        return f"{self.first} {self.last}"
