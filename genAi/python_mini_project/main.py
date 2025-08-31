from bank_system import Bank_v1, Bank_v2

def main():
    print("🐍 ===== Welcome to Slytherin Wizarding Bank =====")

    customers = {
        987654321: Bank_v1("Tom Riddle", 16, 987654321, 4321, 10000),
        123456789: Bank_v2("Draco Malfoy", 21, 123456789, 1234, 50000),
    }

    while True:
        acc_no = Bank_v1.get_int_value("🐍 Enter Account Number or 0 to exit: ")
        
        if acc_no in customers: 
            customer = customers[acc_no]
            entered_pin = Bank_v1.get_int_value("🐍 Enter your PIN: ")
            if customer.verify_pin(entered_pin): 
                print(f"\n🐍 Welcome, {customer.customer_name}!")
                # Customer menu loop
                while True:
                    print("\n📌 Menu:")
                    print("1. Customer Details")
                    print("2. Bank Details")
                    print("3. Deposit")
                    print("4. Withdraw")
                    print("5. Check Balance")
                    
                    print("0. Logout")

                    choice = Bank_v1.get_int_value("🐍 Enter your choice: ")

                    if choice == 1:
                        customer.customer_details()
                    elif choice == 2:
                        customer.bank_details()
                    elif choice == 3:
                        amount = Bank_v1.get_int_value("🐍 Enter amount to deposit: ")
                        customer.deposit(amount)
                    elif choice == 4:
                        customer.withdraw()
                    elif choice == 5:
                        customer.check_balance()
                    elif choice == 0:
                        print(f"🐍 Logging out {customer.customer_name}...")
                        break
                    else:
                        print("❌ Invalid choice, try again!")
            else:
                print("❌ Invalid PIN! Try again.")
        elif acc_no == 0:
            print("🐍 👋 Thank you for banking with Slytherin Wizarding Bank!")
            break
        else:
            print("❌ Account not found!")
            
if __name__ == "__main__":
    main()