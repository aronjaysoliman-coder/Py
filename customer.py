from datetime import datetime

class Customer:
    def __init__(self, name, birthday, sex, contact_number, email):
        self.name = name
        self.birthday = birthday
        self.sex = sex.lower()
        self.contact_number = contact_number
        self.email = email
        self.date_of_reservation = None
        self.time_of_reservation = None

    def book_reservation(self, date, time):
        self.date_of_reservation = date
        self.time_of_reservation = time

    def customer_info(self):
        print("Customer Information")
        print("_____________________")
        print(f"\nName: {self.name}")
        print(f"Birthday: {self.birthday}")
        print(f"Sex: {self.sex.capitalize()}")
        print(f"Contact Number: {self.contact_number}")
        print(f"Email: {self.email}")

        if self.date_of_reservation and self.time_of_reservation:
            print(f"Reservation Date: {self.date_of_reservation}")
            print(f"Reservation Time: {self.time_of_reservation}")
        else:
            print("Reservation: None")

    def greet_cust(self):
        title = "Mr." if self.sex == "male" else "Ms."

        if self.date_of_reservation and self.time_of_reservation:
            print(
                f"\nHello {title} {self.name}! "
                f"Your reservation is on {self.date_of_reservation} "
                f"at {self.time_of_reservation}."
            )
        else:
            print(f"\nHello {title} {self.name}! You have no reservation yet.")


Customer1 = Customer(
    "Quiel", "12-02-1999", "Male",
    "09172418091", "Quiel.Hisarza@gmail.com"
)

Customer2 = Customer(
    "Vince", "02-22-2005", "Male",
    "09918742030", "AljanlyvinceLavado@gmail.com"
)

Customer3 = Customer(
    "Anna", "06-14-2001", "Female",
    "09123456789", "anna@email.com"
)

Customer1.book_reservation("February 5, 2026", "16:00")
Customer2.book_reservation("February 14, 2026", "08:00")
Customer3.book_reservation("February 16, 2026", "08:00")

print()
Customer1.customer_info()
Customer1.greet_cust()

print()
Customer2.customer_info()
Customer2.greet_cust()

print()
Customer3.customer_info()
Customer3.greet_cust()
