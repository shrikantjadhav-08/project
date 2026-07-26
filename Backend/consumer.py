from product import view_product


# -------------------- CONSUMER (GUEST) MENU --------------------

def consumer_menu():

    while True:

        print("\n========== GUEST MENU ==========")
        print("1. View Available Products")
        print("2. Back to Main Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":
            view_product()

        elif choice == "2":
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid Choice! Please Try Again.")
