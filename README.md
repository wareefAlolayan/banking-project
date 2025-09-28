# Banking With Python

Terminal app to manage simple bank customers, accounts, and money movement. Data is stored in `data/bank.csv`.

## Overview

- Add customers (checking, savings, or both)
- Login with account ID + password  
  - If the customer is **inactive**, they can still log in but use  **deposit-only** to fix their balance
- Deposit / Withdraw
- Transfer (self) and Transfer (to another customer)
- Overdraft protection with fee, floor, and deactivation
- Changes are saved back to `data/bank.csv` after successful actions
-----------------------

The app loads data/bank.csv at start and saves after actions like deposit/withdraw/transfer/add customer.
## Features

- **Customers**

    - Create new customer with optional checking/savings and starting balances

    - Active / deactivated status and an overdraft counter

    - Open account later

- **Login & Menus**

    - Normal users: Deposit, Withdraw, Transfer (self), Transfer (to another), Open account, Logout

    - Inactive users: Deposit and Logout only (used to bring balances back to >= 0)

- **Transactions**

    - Deposit: amount > 0; if the customer was inactive and all existing accounts are now >= 0, they are reactivated and overdrafts reset to 0

    - Withdraw: amount > 0; account must exist; overdraft rules enforced

    - Transfer (self): between checking/savings

    - Transfer (to another): send to another customer’s account

- **Overdraft Protection**

    - $35 fee when a withdrawal crosses from >= 0 to < 0

    - While already negative, a single withdrawal can’t exceed $100

    - Hard floor at −$100 (after amount + possible fee)

    - Deactivate on the 2nd overdraft

    - Reactivation: after a deposit brings all accounts to >= 0 (and overdraft count resets to 0)

## Project Structure
- data/bank.csv
- cli.py          # terminal interface 
- models.py       # Account, Customer, Bank (logic: overdraft, transfers, CSV load/save)
- tests/          # unit tests 

## Program Flow (quick)

1. Startup

    - Create Bank and call load_from_csv()

    - For each CSV row, build a Customer with optional Accounts:

        - Empty balance cell means that account doesn’t exist 

        - active status of customers stored as 'true'/'false' in CSV , converted to bool

        - overdrafts loaded as int

2. Admin menu (before login)

    - Add customer → Bank.add_customer() (IDs are last+1) + save_to_csv()

    - Login → Bank.authenticate() (inactive allowed; password required)

    - Exit

3. Customer menu (after login)

    - If active → Deposit / Withdraw / Transfer (self) / Transfer (to another) / Open account / Logout

    - If inactive → Deposit only / Logout

    - After each successful action → save_to_csv()

## Code I’m Proud Of (withdraw + overdraft)
```python
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

    # fee only if crossing into negative
    fee_applies = (start >= 0 and (start - amount) < 0)
    final_w = start - amount - (self.overdraft_fee if fee_applies else 0)

    # never below the floor
    if final_w < self.floor:
        raise ValueError(f'withdrawal would exceed floor {self.floor}')

    acnt.withdraw(amount)
    if fee_applies:
        self.record_overdraft(customer, acnt)  
    return acnt.balance

def record_overdraft(self, customer, account):
        account.withdraw(self.overdraft_fee)
        customer.overdrafts = int(customer.overdrafts) + 1
        if customer.overdrafts >= 2:
            customer.deactivate()
```



## What I Learned

Turning requirements into small checks (fee trigger, negative limit, floor, deactivation)

Separating UI (CLI input + error printing) from logic (Bank raises exceptions and enforces rules)

dealing with CSV 

Testing the tricky parts

## Future Improvements

    - Transaction history CSV

    - Password strength checks
