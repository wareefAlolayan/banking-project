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
                pass

            elif choice == '3':
                pass
            else:
                print('invalid option')
        elif logged_in == True:
            pass