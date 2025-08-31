def verify_pin_decorator(func):
    def wrapper(self, *args, **kwargs):
        pin_input = self.get_int_value("🐍 Enter your PIN: ")
        if pin_input == self.pin:
            return func(self, *args, **kwargs)
        else:
            print("❌ Invalid PIN!")
            return None
    return wrapper

class Bank_v1:
    bank_name = "Slytherin Wizarding Bank"
    branch_manager = "Salazar Slytherin"
    rate_of_interest = 5.5
    branch_name = "Hogwarts"

    def __init__(self, customer_name, customer_age, account_number, pin, balance=0):
        self.customer_name = customer_name
        self.customer_age = customer_age
        self.account_number = account_number
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"✅ {self.customer_name} deposited {amount}. Current balance: {self.balance}")

    def customer_details(self):
        print(f"👤 Name: {self.customer_name}, Age: {self.customer_age}, "
              f"Account: {self.account_number}, Balance: {self.balance}, Branch: {self.branch_name}")

    @classmethod
    def bank_details(cls):
        print(f"🏦 Bank: {cls.bank_name}, Branch: {cls.branch_name}, Interest: {cls.rate_of_interest}%, Bank Manager : {cls.branch_manager}")

    @verify_pin_decorator
    def withdraw(self):
        amount = self.get_int_value("🐍 Enter withdrawal amount: ")
        if amount <= self.balance:
            self.balance -= amount
            print(f"💸 Withdrawal successful. New balance: {self.balance}")
        else:
            print("❌ Insufficient balance.")


    @verify_pin_decorator
    def check_balance(self):
        print(f"💰 Current balance: {self.balance}")


    def verify_pin(self, pin_input):
        return pin_input == self.pin

    @staticmethod
    def get_int_value(prompt="Enter a number: "):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("Invalid input.")


class Bank_v2(Bank_v1):
    branch_name = "Diagon Alley Branch"
    branch_manager = "Severus Snape"
    rate_of_interest = 5.1
    mobile_number = "+123 123123123"

    def __init__(self, customer_name, customer_age, account_number, pin, balance=0):
        super().__init__(customer_name, customer_age, account_number, pin, balance)

    def customer_details(self):
        super().customer_details()
        print(f"PIN: ${self.pin}")

    @classmethod
    def bank_details(cls):
        super().bank_details()
        print(f"Mobile: {cls.mobile_number}")

