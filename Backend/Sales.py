from database import get_connection
from tabulate import tabulate
from datetime import date


# -------------------- TABLE HEADERS --------------------

SALES_HEADERS = [
    "Sale ID",
    "Product ID",
    "Customer Name",
    "Quantity",
    "Selling Price",
    "Total Amount",
    "Sale Date"
]

PRODUCT_HEADERS = [
    "Product ID",
    "Product Name",
    "Category",
    "Brand",
    "Stock",
    "Selling Price"
]

BILL_HEADERS = [
    "No.",
    "Product Name",
    "Qty",
    "Price",
    "Amount"
]


# -------------------- GENERATE BILL --------------------

def generate_bill(customer_name, bill_items, grand_total):

    print("\n")
    print("=" * 60)
    print("         CLOTHING INVENTORY MANAGEMENT SYSTEM")
    print("=" * 60)

    print(f"Customer Name : {customer_name}")
    print(f"Date          : {date.today()}")

    print()

    print(
        tabulate(
            bill_items,
            headers=BILL_HEADERS,
            tablefmt="grid"
        )
    )

    print(f"\nGrand Total : ₹{grand_total}")

    print("=" * 60)
    print("            Thank You! Visit Again")
    print("=" * 60)
def add_sale():

    conn = get_connection()
    cursor = conn.cursor()

    customer_name = input("Enter Customer Name : ")

    bill_items = []

    grand_total = 0

    sr_no = 1

    while True:

        try:

            product_id = int(input("\nEnter Product ID : "))

            cursor.execute("""
                SELECT Product_ID,
                       Product_Name,
                       Category,
                       Brand,
                       Stock,
                       Selling_Price
                FROM Products
                WHERE Product_ID=%s
            """, (product_id,))

            product = cursor.fetchone()

            if product is None:

                print("Product Not Found.")
                continue

            print("\nProduct Details\n")

            print(
                tabulate(
                    [product],
                    headers=PRODUCT_HEADERS,
                    tablefmt="grid"
                )
            )

            quantity = int(input("\nEnter Quantity : "))

            stock = product[4]
            price = float(product[5])

            if quantity <= 0:

                print("Quantity should be greater than zero.")
                continue

            if quantity > stock:

                print("Insufficient Stock.")
                continue

            amount = quantity * price

            sale_date = date.today()

            cursor.execute("""
                INSERT INTO Sales
                (
                    Product_ID,
                    Customer_Name,
                    Quantity,
                    Selling_Price,
                    Total_Amount,
                    Sale_Date
                )
                VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                product_id,
                customer_name,
                quantity,
                price,
                amount,
                sale_date
            ))

            cursor.execute("""
                UPDATE Products
                SET Stock = Stock - %s
                WHERE Product_ID=%s
            """,
            (
                quantity,
                product_id
            ))

            conn.commit()

            bill_items.append(
                [
                    sr_no,
                    product[1],
                    quantity,
                    price,
                    amount
                ]
            )

            grand_total += amount

            sr_no += 1

            choice = input("\nAdd Another Product? (Y/N) : ")

            if choice.upper() != "Y":

                break

        except ValueError:

            print("Invalid Input.")

        except Exception as e:

            conn.rollback()

            print("Error :", e)

    generate_bill(
        customer_name,
        bill_items,
        grand_total
    )

    cursor.close()
    conn.close()
# -------------------- VIEW SALES --------------------

def view_sales():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== VIEW SALES ==========")
        print("1. View All Sales")
        print("2. View Sale Details")
        print("3. Back")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            cursor.execute("""
                SELECT
                    s.Sale_ID,
                    p.Product_Name,
                    s.Customer_Name,
                    s.Quantity,
                    s.Selling_Price,
                    s.Total_Amount,
                    s.Sale_Date
                FROM Sales s
                JOIN Products p
                ON s.Product_ID = p.Product_ID
                ORDER BY s.Sale_ID
            """)

            sales = cursor.fetchall()

            if sales:

                headers = [
                    "Sale ID",
                    "Product",
                    "Customer",
                    "Qty",
                    "Price",
                    "Amount",
                    "Date"
                ]

                print()

                print(
                    tabulate(
                        sales,
                        headers=headers,
                        tablefmt="grid"
                    )
                )

                print("\nTotal Records :", len(sales))

            else:

                print("No Sales Found.")

        elif choice == "2":

            try:

                sale_id = int(input("Enter Sale ID : "))

                cursor.execute("""
                    SELECT
                        s.Sale_ID,
                        p.Product_Name,
                        s.Customer_Name,
                        s.Quantity,
                        s.Selling_Price,
                        s.Total_Amount,
                        s.Sale_Date
                    FROM Sales s
                    JOIN Products p
                    ON s.Product_ID = p.Product_ID
                    WHERE s.Sale_ID=%s
                """, (sale_id,))

                sale = cursor.fetchone()

                if sale:

                    headers = [
                        "Sale ID",
                        "Product",
                        "Customer",
                        "Qty",
                        "Price",
                        "Amount",
                        "Date"
                    ]

                    print()

                    print(
                        tabulate(
                            [sale],
                            headers=headers,
                            tablefmt="grid"
                        )
                    )

                else:

                    print("Sale Not Found.")

            except ValueError:

                print("Invalid Sale ID.")

        elif choice == "3":

            break

        else:

            print("Invalid Choice!")

    cursor.close()
    conn.close()
# -------------------- SEARCH SALE --------------------

def search_sale():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== SEARCH SALE ==========")
        print("1. Search by Sale ID")
        print("2. Search by Customer Name")
        print("3. Search by Product Name")
        print("4. Search by Sale Date")
        print("5. Back")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            sql = """
            SELECT
                s.Sale_ID,
                p.Product_Name,
                s.Customer_Name,
                s.Quantity,
                s.Selling_Price,
                s.Total_Amount,
                s.Sale_Date
            FROM Sales s
            JOIN Products p
            ON s.Product_ID = p.Product_ID
            WHERE s.Sale_ID=%s
            """

            value = int(input("Enter Sale ID : "))

        elif choice == "2":

            sql = """
            SELECT
                s.Sale_ID,
                p.Product_Name,
                s.Customer_Name,
                s.Quantity,
                s.Selling_Price,
                s.Total_Amount,
                s.Sale_Date
            FROM Sales s
            JOIN Products p
            ON s.Product_ID = p.Product_ID
            WHERE s.Customer_Name LIKE %s
            """

            value = "%" + input("Enter Customer Name : ") + "%"

        elif choice == "3":

            sql = """
            SELECT
                s.Sale_ID,
                p.Product_Name,
                s.Customer_Name,
                s.Quantity,
                s.Selling_Price,
                s.Total_Amount,
                s.Sale_Date
            FROM Sales s
            JOIN Products p
            ON s.Product_ID = p.Product_ID
            WHERE p.Product_Name LIKE %s
            """

            value = "%" + input("Enter Product Name : ") + "%"

        elif choice == "4":

            sql = """
            SELECT
                s.Sale_ID,
                p.Product_Name,
                s.Customer_Name,
                s.Quantity,
                s.Selling_Price,
                s.Total_Amount,
                s.Sale_Date
            FROM Sales s
            JOIN Products p
            ON s.Product_ID = p.Product_ID
            WHERE s.Sale_Date=%s
            """

            value = input("Enter Date (YYYY-MM-DD) : ")

        elif choice == "5":

            cursor.close()
            conn.close()
            return

        else:

            print("Invalid Choice!")
            continue

        cursor.execute(sql, (value,))
        sales = cursor.fetchall()

        if sales:

            headers = [
                "Sale ID",
                "Product",
                "Customer",
                "Qty",
                "Price",
                "Amount",
                "Date"
            ]

            print()

            print(
                tabulate(
                    sales,
                    headers=headers,
                    tablefmt="grid"
                )
            )

            print("\nTotal Records :", len(sales))

        else:

            print("No Sales Found.")
# -------------------- DELETE SALE --------------------

def delete_sale():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        sale_id = int(input("Enter Sale ID to Delete : "))

        cursor.execute("""
            SELECT
                s.Sale_ID,
                s.Product_ID,
                p.Product_Name,
                s.Customer_Name,
                s.Quantity,
                s.Selling_Price,
                s.Total_Amount,
                s.Sale_Date
            FROM Sales s
            JOIN Products p
            ON s.Product_ID = p.Product_ID
            WHERE s.Sale_ID=%s
        """, (sale_id,))

        sale = cursor.fetchone()

        if sale is None:

            print("Sale Not Found.")

            cursor.close()
            conn.close()
            return

        headers = [
            "Sale ID",
            "Product ID",
            "Product",
            "Customer",
            "Qty",
            "Price",
            "Amount",
            "Date"
        ]

        print("\nSale Details\n")

        print(
            tabulate(
                [sale],
                headers=headers,
                tablefmt="grid"
            )
        )

        confirm = input("\nAre you sure? (Y/N) : ")

        if confirm.upper() != "Y":

            print("Delete Cancelled.")

            cursor.close()
            conn.close()
            return

        product_id = sale[1]
        quantity = sale[4]

        # Restore Stock

        cursor.execute("""
            UPDATE Products
            SET Stock = Stock + %s
            WHERE Product_ID=%s
        """,
        (
            quantity,
            product_id
        ))

        # Delete Sale

        cursor.execute("""
            DELETE FROM Sales
            WHERE Sale_ID=%s
        """, (sale_id,))

        conn.commit()

        print("\nSale Deleted Successfully.")
        print("Stock Restored Successfully.")

    except ValueError:

        print("Invalid Sale ID.")

    except Exception as e:

        conn.rollback()

        print("Error :", e)

    finally:

        cursor.close()
        conn.close()


# -------------------- SALES MENU --------------------

def sales_menu():

    while True:

        print("\n========== SALES MANAGEMENT ==========")
        print("1. Add Sale")
        print("2. View Sales")
        print("3. Search Sale")
        print("4. Delete Sale")
        print("5. Back to Main Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            add_sale()

        elif choice == "2":

            view_sales()

        elif choice == "3":

            search_sale()

        elif choice == "4":

            delete_sale()

        elif choice == "5":

            print("Returning to Main Menu...")
            break

        else:

            print("Invalid Choice!")
