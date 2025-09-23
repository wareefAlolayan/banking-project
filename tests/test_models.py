import unittest
from models import Account

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
