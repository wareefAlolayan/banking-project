
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

class Customer ():
    def __init__(self , account_id , first_name , last_name , password , open_checking=False , open_savings=False, checking_balance=0 , savings_balance=0):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.active = True
        self.overdrafts = 0
        if open_checking :
            self.checking = Account('checking', checking_balance) 
        else:
            self.checking = None
        if open_savings :
            self.savings  = Account('savings',  savings_balance) 
        else:
            self.savings = None
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    #create account later if it is set to none
    def open_account(self, kind , initial=0):
        pass
     # for login
    def verify_password(self, pw):
        pass
    
    #does the customer have the kind of account he wants to perform operations on?
    def has_account(self, kind):
        pass
    
    # to use account obj for when depositing or withdrawing
    def get_account(self, kind):
        pass

    def deactivate(self):
        self.active = False
    def reactivate(self):
        self.active = True


class Bank:
   pass