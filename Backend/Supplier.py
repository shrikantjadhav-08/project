from database import get_connection
from tabulate import tabulate


# -------------------- TABLE HEADERS --------------------

SUPPLIER_HEADERS = [
    "Supplier ID",
    "Supplier Name",
    "Contact Person",
    "Phone",
    "Email",
    "Address"
]


# -------------------- ADD SUPPLIER --------------------

def add_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_name = input("Enter Supplier Name : ")
    contact_person = input("Enter Contact Person : ")
    phone = input("Enter Phone Number : ")
    email = input("Enter Email : ")
    address = input("Enter Address : ")

    sql = """
    INSERT INTO Suppliers
    (Supplier_Name, Contact_Person, Phone, Email, Address)
    VALUES (%s,%s,%s,%s,%s)
    """

    values = (
        supplier_name,
        contact_person,
        phone,
        email,
        address
    )

    cursor.execute(sql, values)
    conn.commit()

    print("\nSupplier Added Successfully.")

    cursor.close()
    conn.close()


# -------------------- VIEW SUPPLIER --------------------

def view_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== VIEW SUPPLIER ==========")
        print("1. View All Suppliers")
        print("2. View Supplier Details")
        print("3. Back to Supplier Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            cursor.execute("""
            SELECT Supplier_ID,
                   Supplier_Name,
                   Contact_Person,
                   Phone,
                   Email,
                   Address
            FROM Suppliers
            """)

            suppliers = cursor.fetchall()

            if suppliers:

                print("\n========== SUPPLIER LIST ==========\n")

                print(
                    tabulate(
                        suppliers,
                        headers=SUPPLIER_HEADERS,
                        tablefmt="grid"
                    )
                )

            else:
                print("No Suppliers Found.")

        elif choice == "2":

            supplier_id = int(input("Enter Supplier ID : "))

            cursor.execute("""
            SELECT Supplier_ID,
                   Supplier_Name,
                   Contact_Person,
                   Phone,
                   Email,
                   Address
            FROM Suppliers
            WHERE Supplier_ID=%s
            """, (supplier_id,))

            supplier = cursor.fetchone()

            if supplier:

                print("\n========== SUPPLIER DETAILS ==========\n")

                print(
                    tabulate(
                        [supplier],
                        headers=SUPPLIER_HEADERS,
                        tablefmt="grid"
                    )
                )

            else:
                print("Supplier Not Found.")

        elif choice == "3":
            break

        else:
            print("Invalid Choice!")

    cursor.close()
    conn.close()
    # -------------------- UPDATE SUPPLIER --------------------

def update_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = int(input("Enter Supplier ID : "))

    cursor.execute(
        "SELECT * FROM Suppliers WHERE Supplier_ID=%s",
        (supplier_id,)
    )

    supplier = cursor.fetchone()

    if supplier is None:
        print("Supplier Not Found.")
        cursor.close()
        conn.close()
        return

    while True:

        print("\n========== UPDATE SUPPLIER ==========")
        print("1. Update Supplier Name")
        print("2. Update Contact Person")
        print("3. Update Phone")
        print("4. Update Email")
        print("5. Update Address")
        print("6. Save and Back")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            value = input("Enter New Supplier Name : ")

            cursor.execute(
                "UPDATE Suppliers SET Supplier_Name=%s WHERE Supplier_ID=%s",
                (value, supplier_id)
            )

        elif choice == "2":

            value = input("Enter New Contact Person : ")

            cursor.execute(
                "UPDATE Suppliers SET Contact_Person=%s WHERE Supplier_ID=%s",
                (value, supplier_id)
            )

        elif choice == "3":

            value = input("Enter New Phone Number : ")

            cursor.execute(
                "UPDATE Suppliers SET Phone=%s WHERE Supplier_ID=%s",
                (value, supplier_id)
            )

        elif choice == "4":

            value = input("Enter New Email : ")

            cursor.execute(
                "UPDATE Suppliers SET Email=%s WHERE Supplier_ID=%s",
                (value, supplier_id)
            )

        elif choice == "5":

            value = input("Enter New Address : ")

            cursor.execute(
                "UPDATE Suppliers SET Address=%s WHERE Supplier_ID=%s",
                (value, supplier_id)
            )

        elif choice == "6":

            conn.commit()
            print("Supplier Updated Successfully.")
            break

        else:

            print("Invalid Choice!")

    cursor.close()
    conn.close()

# -------------------- DELETE SUPPLIER --------------------

def delete_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    supplier_id = int(input("Enter Supplier ID to Delete : "))

    # Check if Supplier Exists
    cursor.execute(
        "SELECT * FROM Suppliers WHERE Supplier_ID=%s",
        (supplier_id,)
    )

    supplier = cursor.fetchone()

    if supplier is None:

        print("Supplier Not Found.")

        cursor.close()
        conn.close()
        return

    # Check whether any products are assigned to this supplier
    cursor.execute(
        "SELECT COUNT(*) FROM Products WHERE Supplier_ID=%s",
        (supplier_id,)
    )

    count = cursor.fetchone()[0]

    if count > 0:

        print("\nCannot delete this supplier.")
        print("One or more products are assigned to this supplier.")
        print("Please update or delete those products first.")

        cursor.close()
        conn.close()
        return

    # Display Supplier Details
    print("\n========== SUPPLIER DETAILS ==========\n")

    print(
        tabulate(
            [supplier],
            headers=SUPPLIER_HEADERS,
            tablefmt="grid"
        )
    )

    confirm = input("\nAre you sure you want to delete this supplier? (Y/N) : ")

    if confirm.upper() == "Y":

        cursor.execute(
            "DELETE FROM Suppliers WHERE Supplier_ID=%s",
            (supplier_id,)
        )

        conn.commit()

        print("Supplier Deleted Successfully.")

    else:

        print("Delete Cancelled.")

    cursor.close()
    conn.close()
    # -------------------- SEARCH SUPPLIER --------------------

def search_supplier():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== SEARCH SUPPLIER ==========")
        print("1. Search by Supplier ID")
        print("2. Search by Supplier Name")
        print("3. Search by Contact Person")
        print("4. Search by Phone")
        print("5. Search by Email")
        print("6. Back")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            sql = "SELECT * FROM Suppliers WHERE Supplier_ID=%s"
            value = int(input("Enter Supplier ID : "))

        elif choice == "2":

            sql = "SELECT * FROM Suppliers WHERE Supplier_Name=%s"
            value = input("Enter Supplier Name : ")

        elif choice == "3":

            sql = "SELECT * FROM Suppliers WHERE Contact_Person=%s"
            value = input("Enter Contact Person : ")

        elif choice == "4":

            sql = "SELECT * FROM Suppliers WHERE Phone=%s"
            value = input("Enter Phone Number : ")

        elif choice == "5":

            sql = "SELECT * FROM Suppliers WHERE Email=%s"
            value = input("Enter Email : ")

        elif choice == "6":

            cursor.close()
            conn.close()
            return

        else:

            print("Invalid Choice!")
            continue

        cursor.execute(sql, (value,))
        suppliers = cursor.fetchall()

        if suppliers:

            print("\n========== SEARCH RESULT ==========\n")

            print(
                tabulate(
                    suppliers,
                    headers=SUPPLIER_HEADERS,
                    tablefmt="grid"
                )
            )

        else:

            print("No Supplier Found.")


# -------------------- SUPPLIER MENU --------------------

def supplier_menu():

    while True:

        print("\n========== SUPPLIER MANAGEMENT ==========")
        print("1. Add Supplier")
        print("2. View Supplier")
        print("3. Update Supplier")
        print("4. Delete Supplier")
        print("5. Search Supplier")
        print("6. Back to Main Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            add_supplier()

        elif choice == "2":

            view_supplier()

        elif choice == "3":

            update_supplier()

        elif choice == "4":

            delete_supplier()

        elif choice == "5":

            search_supplier()

        elif choice == "6":

            print("Returning to Main Menu...")
            break

        else:

            print("Invalid Choice!")
