import unittest
from models import Account, Customer , Bank

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.acc = Account("checking", 100)

    def test_deposit_increases_balance(self):
        self.acc.deposit(50)
        self.assertEqual(self.acc.balance, 150)

    def test_withdraw_decreases_balance(self):
        self.acc.withdraw(40)
        self.assertEqual(self.acc.balance, 60)

    def test_deposit_must_be_positive(self):
        with self.assertRaises(ValueError):
            self.acc.deposit(0)
        with self.assertRaises(ValueError):
            self.acc.deposit(-10)

    def test_withdraw_must_be_positive(self):
        with self.assertRaises(ValueError):
            self.acc.withdraw(0)
        with self.assertRaises(ValueError):
            self.acc.withdraw(-5)

    def test_can_go_negative_bank_handles_rules_later(self):
        self.acc.withdraw(150)  # 100 - 150 = -50
        self.assertEqual(self.acc.balance, -50)

    def test_sequence_of_ops(self):
        self.acc.deposit(25)    # 125
        self.acc.withdraw(20)   # 105
        self.acc.deposit(15)    # 120
        self.assertEqual(self.acc.balance, 120)


class TestCustomer(unittest.TestCase):
    def setUp(self):
        # checking only
        self.c1 = Customer("1", "war", "moh", "ohjb",open_checking=True, open_savings=False,checking_balance=100)
        #savings only
        self.c2 = Customer("2", "jo", "le", "fvbj", open_checking=False, open_savings=True,savings_balance=50)
    
    def test_verify_password(self):
        self.assertTrue(self.c1.verify_password('ohjb'))
        self.assertFalse(self.c1.verify_password('wrong'))
        self.assertTrue(self.c2.verify_password('fvbj'))
        self.assertFalse(self.c2.verify_password('wrong'))
    def test_has_account(self):
        self.assertTrue(self.c1.has_account('checking'))
        self.assertFalse(self.c1.has_account('savings'))
        self.assertTrue(self.c2.has_account('savings'))
        self.assertFalse(self.c2.has_account('checking'))
        with self.assertRaises(ValueError):
            self.c1.has_account('xx')
    def test_get_account(self):
        acc = self.c1.get_account('checking')
        self.assertIsInstance(acc, Account) #ref : geeksforgeeks
        self.assertEqual(acc.balance, 100)
        with self.assertRaises(ValueError):
            self.c1.get_account('savings')
        with self.assertRaises(ValueError):
            self.c1.get_account('xx')
    def test_open_account(self):
        self.c1.open_account('savings', initial=25)
        self.assertTrue(self.c1.has_account('savings'))
        self.assertEqual(self.c1.get_account('savings').balance, 25)
        with self.assertRaises(ValueError):
            self.c1.open_account('savings', initial=10)
        with self.assertRaises(ValueError):
            self.c1.open_account('xx', initial=10)

# class TestBankCSV(unittest.TestCase):
    # def test_load_from_csv_basic(self):  #only used once to prove load is working
    #     bank = Bank()            
    #     x=bank.load_from_csv()
    #     res=[]
    #     for c in x:
    #         bc = c.checking.balance if c.checking else None
    #         bs = c.savings.balance if c.savings else None
    #         res.append((c.account_id, c.first_name, c.last_name, c.password,bc, bs, c.active, int(c.overdrafts)))
    #     expected_customers = [('10001','suresh','sigera','juagw362',1000,10000,True,0),('10002','james', 'taylor','idh36%@#FGd',10000,10000,True,0),('10003','melvin','gordon','uYWE732g4ga1',2000,20000,True,0),('10004','stacey','abrams','DEU8_qw3y72$',2000,20000,True,0),('10005','jake',  'paul',  'd^dg23g)@', 100000,100000, True, 0),('10006','w','w','w',-37,None, False, 2),('10007','w','w','w',-37,None,False, 2)]
    #     self.assertEqual(res, expected_customers)
    # def test_save_to_csv_basic(self): #only used once to prove save is working
    #     bank = Bank()            
    #     bank.load_from_csv() #proven to work
    #     bank.add_customer('a','b','c',True, True, 10, 20) #proven to work
    #     bank.save_to_csv() #testing this
    #     bank2 = Bank()
    #     x=bank2.load_from_csv() #reloading to see if saved correctly 
    #     res=[]
    #     for c in x:
    #         bc = c.checking.balance if c.checking else None
    #         bs = c.savings.balance if c.savings else None
    #         res.append((c.account_id, c.first_name, c.last_name, c.password,bc, bs, c.active, int(c.overdrafts)))
    #     expected_customers = [('10001','suresh','sigera','juagw362',1000,10000,True,0),('10002','james', 'taylor','idh36%@#FGd',10000,10000,True,0),('10003','melvin','gordon','uYWE732g4ga1',2000,20000,True,0),('10004','stacey','abrams','DEU8_qw3y72$',2000,20000,True,0),('10005','jake',  'paul',  'd^dg23g)@', 100000,100000, True, 0),('10006','w','w','w',-37,None, False, 2),('10007','w','w','w',-37,None,False, 2),('10008','a','b','c',10,20,True,0)]
    #     self.assertEqual(res, expected_customers)

class TestBankCore(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.bank.load_from_csv()
    def test_find_customer(self):
        c = self.bank.find_customer('10001')
        self.assertIsInstance(c, Customer)
        self.assertEqual(c.first_name, 'suresh')
        self.assertEqual(c.last_name, 'sigera')
        self.assertEqual(c.checking.balance, 1000)
        self.assertEqual(c.savings.balance, 10000)
        with self.assertRaises(ValueError):
            self.bank.find_customer('99999')
    # def test_add_customer(self):
    #     newc = self.bank.add_customer('a', 'b', 'c', True, True, 500, 1000)
    #     self.assertIsInstance(newc, Customer)
    #     self.assertEqual(newc.first_name, 'a')
    #     self.assertEqual(newc.last_name, 'b')
    #     self.assertTrue(newc.has_account('checking'))
    #     self.assertTrue(newc.has_account('savings'))
    #     self.assertEqual(newc.get_account('checking').balance, 500)
    #     self.assertEqual(newc.get_account('savings').balance, 1000)
    def test_authnticate(self):
        c = self.bank.authenticate('10001', 'juagw362')
        self.assertIsInstance(c, Customer)
        self.assertEqual(c.first_name, 'suresh')
        with self.assertRaises(ValueError):
            self.bank.authenticate('10001', 'wrongpassword')
        with self.assertRaises(ValueError):
            self.bank.authenticate('99999', 'somepassword')
    # def test_withdraw(self):
    #     self.c = self.bank.find_customer('10001')
    #     self.bank.withdraw(self.c,'checking',200) #1000-200=800
    #     self.assertEqual(self.c.checking.balance, 800) #normal
    #     with self.assertRaises(ValueError):
    #         self.bank.withdraw(self.c, 'checking', 0) #withdrwa not >0
    #     self.c = self.bank.find_customer('10006')
    #     with self.assertRaises(ValueError):
    #         self.bank.withdraw(self.c, 'savings', 10) #no savings account
    #     self.c = self.bank.find_customer('10007')
    #     with self.assertRaises(ValueError):
    #         self.bank.withdraw(self.c, 'checking', 10000) #overdrafts =2
    # def test_transfer_self(self):
    #     self.c = self.bank.find_customer('10001')
    #     self.bank.transfer_self(self.c, 'checking', 'savings', 500) #1000-500=500 , 10000+500=10500
    #     self.assertEqual(self.c.checking.balance, 500)
    #     self.assertEqual(self.c.savings.balance, 10500)
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_self(self.c, 'checking', 'savings', 0) #transfer not >0
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_self(self.c, 'checking', 'savings', 600) #not sufficient funds
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_self(self.c, 'checking', 'checking', 10) #same account
    #     c2 = self.bank.find_customer('10002')
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_self(c2, 'savings', 'checking', 10) #no from account
    #     c3 = self.bank.find_customer('10006')
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_self(c3, 'checking', 'savings', 10) #no to account
    #     c3 = self.bank.find_customer('10007')
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_self(c3, 'savings', 'checking', 10) #account deactivated
    # def test_transfer_other(self):
    #     c1 = self.bank.find_customer('10001')
    #     c2 = self.bank.find_customer('10002')
    #     self.bank.transfer_to_customer(c1, 'checking', '10002', 'checking', 500) #1000-500=500 , 10000+500=10500
    #     self.assertEqual(c1.checking.balance, 500)
    #     self.assertEqual(c2.checking.balance, 10500)
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c1, 'checking', '10002', 'checking', 0) #transfer not >0
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c1, 'checking', '10002', 'checking', 600) #not sufficient funds
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c1, 'checking', '10001', 'checking', 10) #same customer
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c1, 'checking', '99999', 'checking', 10) #to customer not found
    #     c3 = self.bank.find_customer('10002')
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c3, 'checking', '10002', 'checking', 10) #no from account
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c1, 'checking', '10002', 'savings', 10) #to has no savings account
    #     c5 = self.bank.find_customer('10007')
    #     with self.assertRaises(ValueError):
    #         self.bank.transfer_to_customer(c5, 'checking', '10002', 'checking', 10) #from account deactivated
    # def test_reactivate(self):
    #     c = self.bank.find_customer('10007')
    #     self.bank.reactivate(c)
    #     self.assertTrue(c.active)
    #     self.assertEqual(c.overdrafts, 0)
    #     c2 = self.bank.find_customer('10006')
    # def test_record_overdraft(self):
    #     c = self.bank.find_customer('10006')
    #     self.bank.record_overdraft(c, c.checking)
    #     self.assertEqual(c.overdrafts, 1)
    #     self.bank.record_overdraft(c,c.checking) #should be deactivated now
    #     self.assertEqual(c.overdrafts, 2)
    #     self.assertEqual(c.active, False) 



#commented tests are either can be used once (csv) or would change the csv file (add customer) or depened on current state of csv (transfer self , transfer other , withdraw ,record overdraft , reactivate)
#DONE