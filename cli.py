from models import Bank

def main():
    bank = Bank()
    bank.load_from_csv()
    logged_in = False
    while True:
        if logged_in == False:
            print('Bank System')
            print('1) Login')
            print('2) Add customer')
            print('3) Exit')
            choice = input('your choice: ').strip()
            if choice == '1':
                try:
                    cid = input('account id: ')
                    pw = input('password: ')
                    customer = bank.authenticate(cid, pw)
                    logged_in = True
                except ValueError as e:
                    print(e)
            elif choice == '2':
                try:
                    first = input('first name: ')
                    last = input('last name: ')
                    pw = input('password: ')
                    open_chk = input('open checking? (y/n): ').lower() 
                    open_sav = input('open savings? (y/n): ').lower() 
                    ic = int(input('initial checking : '))
                    isv = int(input('initial savings : '))
                    newc = bank.add_customer(first, last, pw, open_chk == 'y' , open_sav== 'y', ic, isv)
                    print(f'created new custome , customer id : {newc.account_id}')
                except ValueError as e:
                    print(e)


            elif choice == '3':
                print('bye')
                break
            else:
                print('invalid option')
        elif logged_in == True:
            print(f'Welcome {customer.full_name}')
            if customer.checking != None:
                cb = customer.checking.balance
            else:
                cb = 'none'
            if customer.savings.balance != None:
                sb = customer.savings.balance  
            else:
                sb = 'none'
                
            print(f'checking: {cb}   savings: {sb}')
            print('1) Deposit')
            print('2) withdraw')
            print('3) Transfer between your accounts')
            print('4) Transfer to different customer')
            print('5) Logout')
            choice = input('your choice: ').strip()
            try:
                if choice == '1':
                    kind = input('account (checking/savings): ').lower()
                    amt = int(input('amount: '))
                    newb = bank.deposit(customer, kind, amt)
                    bank.save_to_csv()
                    print(f'done, new {kind} balance: {newb}')

                elif choice == '2':
                    kind = input('account (checking/savings): ').lower()
                    amt = int(input('amount: '))
                    newb = bank.withdraw(customer, kind, amt)
                    bank.save_to_csv()
                    print(f'done, new {kind} balance: {newb}')

                elif choice == '3':
                    from_kind = input('from? (checking/savings): ').lower()
                    to_kind   = input('to?   (checking/savings): ').lower()
                    amt = int(input('amount: '))
                    bank.transfer_self(customer, from_kind, to_kind, amt)
                    bank.save_to_csv()
                    print('transfer done')

                elif choice == '4':
                    from_kind = input('from? (checking/savings): ').lower()
                    to_id   = input('to? account id: ')
                    to_kind = input('to kind? (checking/savings): ').lower()
                    amt = int(input('amount: '))
                    bank.transfer_to_customer(customer, from_kind, to_id, to_kind, amt)
                    bank.save_to_csv()
                    print('transfer done')

                elif choice == '5':
                    pass
                else:
                    print('invalid option')

            except Exception as e:
                print(e)
