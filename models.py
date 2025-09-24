import csv
class Account ():
    def __init__(self, kind, balance=0):
        self.kind = kind # check or save
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        amount = int(amount)
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self._balance += amount

    def withdraw(self, amount):
        amount = int(amount)
        if amount <= 0:
            raise ValueError("amount must be > 0")
        self._balance -= amount

class Customer ():
    def __init__(self , account_id , first_name , last_name , password , open_checking=False , open_savings=False, checking_balance=0 , savings_balance=0):
        self.account_id = account_id
        self.frst_name = first_name
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
        return f'{self.frst_name} {self.last_name}'
    
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
    def __init__(self):
        self.csv_path='data/bank.csv'    
        self.customers = []      
        #overdraft policy
        self.overdraft_fee = 35 
        self.floor = -100  #final balance cant go under this
        self.negative_withdraw_limit = 100
    def load_from_csv(self):
        with open(self.csv_path, 'w' , newline='') as file:
            reader = csv.DictWriter(file)
            for row in reader:
                account_id = row['account_id']
                first = row['frst_name']   
                last = row['last_name']
                pw = row['password']
                balance_checking = row['balance_checking']
                balance_savings = row['balance_savings']

                #check if account exist or not 
                open_checking = balance_checking != ''
                open_savings  = balance_savings != ''
            
                if balance_checking :
                    balance_checking = int(balance_checking)
                else:
                    balance_checking = 0
                if balance_savings :
                    balance_savings = int(balance_savings)
                else:
                    balance_savings = 0

                customer = Customer(
                    account_id, first, last, pw,
                    open_checking=open_checking,
                    open_savings=open_savings,
                    checking_balance=balance_checking,
                    savings_balance=balance_savings,
                )
                self.customers.append(customer)
    def save_to_csv(self):
        rows = [['account_id', 'frst_name', 'last_name', 'password', 'balance_checking', 'balance_savings']]

        for c in self.customers:
            bc = c.checking.balance if c.checking else ''
            bs = c.savings.balance  if c.savings  else ''
            rows.append([c.account_id, c.first_name, c.last_name, c.password, bc, bs])

        # Write all rows
        with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    #customer management methods
    def find_customer(self, account_id):
        pass

    def generate_unique_id(self):
        pass

    def add_customer(self, first_name, last_name, password,open_checking=False, open_savings=False,initial_checking=0, initial_savings=0):
        pass

    def authenticate(self, account_id, password):
        #Find customer, ensure active, verify password, return customer or raise
        pass
    
    #transaction methods
    def withdraw(self, customer, kind, amount):
        #Apply overdraft rules 
        pass

    def transfer_self(self, customer, from_kind, to_kind, amount):
        pass

    def transfer_to_customer(self, from_customer, from_kind, to_account_id, to_kind, amount):
        pass

    def deposit(self, customer, kind, amount):
        pass


    #overdraft methods
    def reactivate(self, customer):
        pass

    def record_overdraft(self, customer, account):
        pass

    def deactivate(self, customer):
        pass