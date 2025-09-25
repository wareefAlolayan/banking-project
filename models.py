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
    
    
    def open_account(self, kind , initial=0):
    #if the account doesnt exist create it with the initial balance
        if kind == 'checking':
            if self.checking == None:
                self.checking = Account('checking', initial)
            else:
                raise ValueError('checking account already exists')
        elif kind == 'savings':
            if self.savings == None:
                self.savings = Account('savings', initial)
            else:
                raise ValueError('savings account already exists')
        else:
            raise ValueError('kind must be checking or savings ')
        
     # for login
    def verify_password(self, pw):
        if pw == self.password:
            return True
        else:
            return False
    
    #does the customer have the kind of account he wants to perform operations on?
    def has_account(self, kind):
        if kind == 'checking':
            return self.checking != None
        elif kind == 'savings':
            return self.savings != None
        else:
            raise ValueError('kind must be checking or savings')
        
    # to use account obj for when depositing or withdrawing
    def get_account(self, kind):
        if kind == 'checking' and self.checking != None:
            return self.checking
        elif kind == 'savings' and self.savings != None:
            return self.savings
        elif kind == 'checking' or kind == 'savings':
            raise ValueError(f'{kind} account does not exist')
        else:
            raise ValueError('kind must be checking or savings')

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
                customer.active = ( row["active"]  == "true")
                customer.overdrafts = row["overdrafts"]
                self.customers.append(customer)


    def save_to_csv(self):
        rows = [['account_id', 'frst_name', 'last_name', 'password', 'balance_checking', 'balance_savings','active','overdrafts']]#added ,active,overdrafts

        for c in self.customers:
            bc = c.checking.balance if c.checking else ''
            bs = c.savings.balance  if c.savings  else ''
            rows.append([c.account_id, c.first_name, c.last_name, c.password, bc, bs,c.active,c.overdrafts])

        # Write all rows
        with open(self.csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    #customer management methods
    def find_customer(self, account_id):
        for c in self.customers:
            if c.account_id == str(account_id):
                return c
    def generate_unique_id(self):
        last = int(self.customers[-1].account_id) 
        return str(last + 1)

    def add_customer(self, first_name, last_name, password,open_checking=False, open_savings=False,initial_checking=0, initial_savings=0):
        new_id = self.generate_unique_id()
        customer = Customer(new_id, first_name, last_name, password,open_checking=open_checking, open_savings=open_savings,checking_balance=initial_checking, savings_balance=initial_savings)
        # default for new accounts
        customer.active = True
        customer.overdrafts = 0
        self.customers.append(customer)
        self.save_to_csv()
        
    def authenticate(self, account_id, password):
        customer = self.find_customer(account_id)
        if customer == None:
            raise ValueError('customer not found')
        if customer.active == False:
            raise ValueError('account is deactivated')
        if customer.verify_password(password) == False:
            raise ValueError('invalid password')
        return customer
    
    #transaction methods
    def withdraw(self, customer, kind, amount):
        amount = int(amount)
        if customer.active == False:
            raise ValueError('account is deactivated')
        if amount <= 0:
            raise ValueError('amount must be > 0')
        if customer.has_account(kind) == False:
            raise ValueError(f'{kind} account not found')

        acnt = customer.get_account(kind)
        start = acnt.balance

        if start < 0 and amount > self.negative_withdraw_limit:
            raise ValueError('cannot withdraw more than 100 while negative')

        fee_applies = (start >= 0 and (start - amount) < 0)
        if fee_applies:
            final_w = start - amount - self.overdraft_fee
        else:
            final_w = start - amount

        if final_w < self.floor:
            raise ValueError(f'withdrawal would exceed floor {self.floor}')
        
        acnt.withdraw(amount)
        if fee_applies:
            acnt.withdraw(self.overdraft_fee)
            customer.overdrafts += 1
            if customer.overdrafts >= 2:
                customer.deactivate()

        return acnt.balance

    def transfer_self(self, customer, from_kind, to_kind, amount):
        pass

    def transfer_to_customer(self, from_customer, from_kind, to_account_id, to_kind, amount):
        pass

    def deposit(self, customer, kind, amount):
        amount = int(amount)
        if amount <= 0:
            raise ValueError("amount must be > 0")
        if customer.has_account(kind) == False:
            raise ValueError(f"{kind} account not found")

        acnt = customer.get_account(kind)
        acnt.deposit(amount)
        # reactivate only if the account was inactive and all existing accounts are now >= 0
        if customer.active == False:
            can_reactivate = True
            if customer.checking != None and customer.checking.balance < 0:
                can_reactivate = False
            if customer.savings != None and customer.savings.balance < 0:
                can_reactivate = False
            if can_reactivate:
                customer.reactivate()
        return acnt.balance

    #overdraft methods
    def reactivate(self, customer):
        pass

    def record_overdraft(self, customer, account):
        pass

    def deactivate(self, customer):
        pass