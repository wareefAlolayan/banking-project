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
            pass