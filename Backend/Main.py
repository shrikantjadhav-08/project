from login import login
from supplier import supplier_menu
from product import view_product
from product import product_menu
from inventory import inventory_menu
from sales import sales_menu
from reports import reports_menu
from consumer import consumer_menu   
from login import add_users  
from ai_chat import ai_assistant

# -------------------- ADMIN MENU --------------------

def admin_menu():
    while True:
        print("\n===== CLOTHING INVENTORY MANAGEMENT SYSTEM =====")
        print("1. Supplier Management")
        print("2. Product Management")
        print("3. Inventory Management")
        print("4. Sales Management")
        print("5. Reports")
        print("6. Add User")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            supplier_menu()

        elif choice == "2":
            product_menu()

        elif choice == "3":
            inventory_menu()

        elif choice == "4":
            sales_menu()

        elif choice == "5":
            reports_menu()

        elif choice == "6":
             add_users()

        elif choice == "7":
            print("Logged Out Successfully...")
            break
        else:
            print("Invalid Choice!")


# -------------------- USER MENU --------------------

def user_menu():
    while True:
        print("\n===== CUSTOMER MENU =====")
        print("1. View Products")
        print("2. Purchase Product")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_product()

        elif choice == "2":
            sales_menu()

        elif choice == "3":
            print("Logged Out Successfully...")
            break

        else:
            print("Invalid Choice!")


# -------------------- MAIN MENU --------------------

def main():

    while True:

        print("\n" + "=" * 50)
        print("   CLOTHING INVENTORY MANAGEMENT SYSTEM")
        print("=" * 50)

        print("1. Login")
        print("2. Consumer (Guest)")
        print("3. AI Assistant ")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            role = login()

            if role == "admin":
                admin_menu()

            elif role == "user":
                user_menu()

            else:
                print("Login Failed...")

        elif choice == "2":
            consumer_menu()

        elif choice == "3":
            ai_assistant()


        elif choice == "4":
            print("Thank You For Visiting.")
            break

        else:
            print("Invalid Choice!")


if __name__ == "__main__":
    main()
