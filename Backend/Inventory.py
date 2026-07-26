from database import get_connection
from tabulate import tabulate


# -------------------- TABLE HEADERS --------------------

INVENTORY_HEADERS = [
    "Product ID",
    "Product Name",
    "Category",
    "Brand",
    "Stock",
    "Supplier ID"
]


# -------------------- VIEW INVENTORY --------------------

def view_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== VIEW INVENTORY ==========")
        print("1. View All Inventory")
        print("2. View Product Stock")
        print("3. Back to Inventory Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            cursor.execute("""
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            ORDER BY Product_ID
            """)

            products = cursor.fetchall()

            if products:

                print("\n========== INVENTORY LIST ==========\n")

                print(
                    tabulate(
                        products,
                        headers=INVENTORY_HEADERS,
                        tablefmt="grid"
                    )
                )

            else:

                print("No Products Found.")

        elif choice == "2":

            product_id = int(input("Enter Product ID : "))

            cursor.execute("""
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            WHERE Product_ID=%s
            """, (product_id,))

            product = cursor.fetchone()

            if product:

                print("\n========== PRODUCT STOCK ==========\n")

                print(
                    tabulate(
                        [product],
                        headers=INVENTORY_HEADERS,
                        tablefmt="grid"
                    )
                )

            else:

                print("Product Not Found.")

        elif choice == "3":

            break

        else:

            print("Invalid Choice!")

    cursor.close()
    conn.close()
    # -------------------- UPDATE STOCK --------------------

def update_stock():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID : "))

    cursor.execute(
        """
        SELECT Product_ID,
               Product_Name,
               Category,
               Brand,
               Stock,
               Supplier_ID
        FROM Products
        WHERE Product_ID=%s
        """,
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:

        print("Product Not Found.")

        cursor.close()
        conn.close()
        return

    print("\n========== CURRENT PRODUCT DETAILS ==========\n")

    print(
        tabulate(
            [product],
            headers=INVENTORY_HEADERS,
            tablefmt="grid"
        )
    )

    new_stock = int(input("\nEnter New Stock Quantity : "))

    if new_stock < 0:

        print("Stock cannot be negative.")

        cursor.close()
        conn.close()
        return

    cursor.execute(
        "UPDATE Products SET Stock=%s WHERE Product_ID=%s",
        (new_stock, product_id)
    )

    conn.commit()

    print("Stock Updated Successfully.")

    cursor.close()
    conn.close()


# -------------------- SEARCH INVENTORY --------------------

def search_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== SEARCH INVENTORY ==========")
        print("1. Search by Product ID")
        print("2. Search by Product Name")
        print("3. Search by Category")
        print("4. Search by Brand")
        print("5. Search by Supplier ID")
        print("6. Back")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            sql = """
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            WHERE Product_ID=%s
            """

            value = int(input("Enter Product ID : "))

        elif choice == "2":

            sql = """
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            WHERE Product_Name=%s
            """

            value = input("Enter Product Name : ")

        elif choice == "3":

            sql = """
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            WHERE Category=%s
            """

            value = input("Enter Category : ")

        elif choice == "4":

            sql = """
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            WHERE Brand=%s
            """

            value = input("Enter Brand : ")

        elif choice == "5":

            sql = """
            SELECT Product_ID,
                   Product_Name,
                   Category,
                   Brand,
                   Stock,
                   Supplier_ID
            FROM Products
            WHERE Supplier_ID=%s
            """

            value = int(input("Enter Supplier ID : "))

        elif choice == "6":

            cursor.close()
            conn.close()
            return

        else:

            print("Invalid Choice!")
            continue

        cursor.execute(sql, (value,))
        products = cursor.fetchall()

        if products:

            print("\n========== SEARCH RESULT ==========\n")

            print(
                tabulate(
                    products,
                    headers=INVENTORY_HEADERS,
                    tablefmt="grid"
                )
            )

        else:

            print("No Product Found.")
            # -------------------- LOW STOCK REPORT --------------------

def low_stock_report():

    conn = get_connection()
    cursor = conn.cursor()

    low_stock_limit = 5

    cursor.execute("""
        SELECT Product_ID,
               Product_Name,
               Category,
               Brand,
               Stock,
               Supplier_ID
        FROM Products
        WHERE Stock < %s
        ORDER BY Stock ASC
    """, (low_stock_limit,))

    products = cursor.fetchall()

    if products:

        print("\n========== LOW STOCK REPORT ==========\n")

        print(
            tabulate(
                products,
                headers=INVENTORY_HEADERS,
                tablefmt="grid"
            )
        )

    else:

        print("\nAll Products Have Sufficient Stock.")

    cursor.close()
    conn.close()


# -------------------- INVENTORY MENU --------------------

def inventory_menu():

    while True:

        print("\n========== INVENTORY MANAGEMENT ==========")
        print("1. View Inventory")
        print("2. Update Stock")
        print("3. Search Inventory")
        print("4. Low Stock Report")
        print("5. Back to Main Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            view_inventory()

        elif choice == "2":

            update_stock()

        elif choice == "3":

            search_inventory()

        elif choice == "4":

            low_stock_report()

        elif choice == "5":

            print("Returning to Main Menu...")
            break

        else:

            print("Invalid Choice!")
