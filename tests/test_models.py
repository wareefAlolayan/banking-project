import unittest
from models import Account, Customer , Bank

# class TestAccount(unittest.TestCase):
#     def setUp(self):
#         self.acc = Account("checking", 100)

#     def test_deposit_increases_balance(self):
#         self.acc.deposit(50)
#         self.assertEqual(self.acc.balance, 150)

#     def test_withdraw_decreases_balance(self):
#         self.acc.withdraw(40)
#         self.assertEqual(self.acc.balance, 60)

#     def test_deposit_must_be_positive(self):
#         with self.assertRaises(ValueError):
#             self.acc.deposit(0)
#         with self.assertRaises(ValueError):
#             self.acc.deposit(-10)

#     def test_withdraw_must_be_positive(self):
#         with self.assertRaises(ValueError):
#             self.acc.withdraw(0)
#         with self.assertRaises(ValueError):
#             self.acc.withdraw(-5)

#     def test_can_go_negative_bank_handles_rules_later(self):
#         self.acc.withdraw(150)  # 100 - 150 = -50
#         self.assertEqual(self.acc.balance, -50)

#     def test_sequence_of_ops(self):
#         self.acc.deposit(25)    # 125
#         self.acc.withdraw(20)   # 105
#         self.acc.deposit(15)    # 120
#         self.assertEqual(self.acc.balance, 120)


# class TestCustomer(unittest.TestCase):
#     def setUp(self):
#         # checking only
#         self.c1 = Customer("1", "war", "moh", "ohjb",open_checking=True, open_savings=False,checking_balance=100)
#         #savings only
#         self.c2 = Customer("2", "jo", "le", "fvbj", open_checking=False, open_savings=True,savings_balance=50)
    
#     def test_verify_password(self):
#         self.assertTrue(self.c1.verify_password('ohjb'))
#         self.assertFalse(self.c1.verify_password('wrong'))
#         self.assertTrue(self.c2.verify_password('fvbj'))
#         self.assertFalse(self.c2.verify_password('wrong'))
#     def test_has_account(self):
#         self.assertTrue(self.c1.has_account('checking'))
#         self.assertFalse(self.c1.has_account('savings'))
#         self.assertTrue(self.c2.has_account('savings'))
#         self.assertFalse(self.c2.has_account('checking'))
#         with self.assertRaises(ValueError):
#             self.c1.has_account('xx')
#     def test_get_account(self):
#         acc = self.c1.get_account('checking')
#         self.assertIsInstance(acc, Account) #ref : geeksforgeeks
#         self.assertEqual(acc.balance, 100)
#         with self.assertRaises(ValueError):
#             self.c1.get_account('savings')
#         with self.assertRaises(ValueError):
#             self.c1.get_account('xx')
#     def test_open_account(self):
#         self.c1.open_account('savings', initial=25)
#         self.assertTrue(self.c1.has_account('savings'))
#         self.assertEqual(self.c1.get_account('savings').balance, 25)
#         with self.assertRaises(ValueError):
#             self.c1.open_account('savings', initial=10)
#         with self.assertRaises(ValueError):
#             self.c1.open_account('xx', initial=10)

class TestBankCSV(unittest.TestCase):
    def test_load_from_csv_basic(self):
        bank = Bank()            
        bank.load_from_csv()
        self.assertEqual(bank.customers, 'x' )