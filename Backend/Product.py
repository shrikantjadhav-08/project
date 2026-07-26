from database import get_connection
from tabulate import tabulate

        # -------------------- TABLE HEADERS --------------------

PRODUCT_HEADERS = [
    "Product ID",
    "Product Name",
    "Category",
    "Brand",
    "Size",
    "Color",
    "Selling Price",
    "Stock",
    "Supplier ID"
]
        # -------------------- ADD PRODUCT --------------------

def add_product():

    conn = get_connection()
    cursor = conn.cursor()

    product_name = input("Enter Product Name : ")
    category = input("Enter Category : ")
    brand = input("Enter Brand : ")
    size = input("Enter Size : ")
    color = input("Enter Color : ")
    selling_price = float(input("Enter Selling Price : "))
    stock = int(input("Enter Stock : "))
    supplier_id = int(input("Enter Supplier ID : "))

    cursor.execute(
        "SELECT Supplier_ID FROM Suppliers WHERE Supplier_ID=%s",
        (supplier_id,)
    )

    if cursor.fetchone() is None:
        print("Supplier ID does not exist.")
        cursor.close()
        conn.close()
        return

    sql = """
    INSERT INTO Products
    (Product_Name, Category, Brand, Size, Color,
    Selling_Price, Stock, Supplier_ID)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        product_name,
        category,
        brand,
        size,
        color,
        selling_price,
        stock,
        supplier_id
    )

    cursor.execute(sql, values)
    conn.commit()

    print("\nProduct Added Successfully.")

    cursor.close()
    conn.close()

        # -------------------- VIEW PRODUCT --------------------

def view_product():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== VIEW PRODUCT ==========")
        print("1. View All Products")
        print("2. View Product Details")
        print("3. Back to Product Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":

            cursor.execute("""
            SELECT Product_ID, Product_Name, Category,
            Brand, Size, Color,
            Selling_Price, Stock, Supplier_ID
            FROM Products
            """)

            products = cursor.fetchall()

            if products:

                print("\n========== PRODUCT LIST ==========\n")

                print(
                    tabulate(
                        products,
                        headers=PRODUCT_HEADERS,
                        tablefmt="grid"
                    )
                )

            else:
                print("No Products Found.")

        elif choice == "2":

            product_id = int(input("Enter Product ID : "))

            cursor.execute("""
            SELECT Product_ID, Product_Name, Category,
            Brand, Size, Color,
            Selling_Price, Stock, Supplier_ID
            FROM Products
            WHERE Product_ID=%s
            """, (product_id,))

            product = cursor.fetchone()

            if product:

                print("\n========== PRODUCT DETAILS ==========\n")

                print(
                    tabulate(
                        [product],
                        headers=PRODUCT_HEADERS,
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
    
        # -------------------- UPDATE PRODUCT --------------------

def update_product():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID : "))

    cursor.execute(
        "SELECT * FROM Products WHERE Product_ID=%s",
        (product_id,)
    )

    if cursor.fetchone() is None:
        print("Product Not Found")
        cursor.close()
        conn.close()
        return

    while True:

        print("\n========== UPDATE PRODUCT ==========")
        print("1. Update Product Name")
        print("2. Update Category")
        print("3. Update Brand")
        print("4. Update Size")
        print("5. Update Color")
        print("6. Update Selling Price")
        print("7. Update Stock")
        print("8. Update Supplier ID")
        print("9. Save and Back")

        choice = int(input("Enter Choice : "))

        if choice == 1:
            value = input("New Product Name : ")
            cursor.execute(
                "UPDATE Products SET Product_Name=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 2:
            value = input("New Category : ")
            cursor.execute(
                "UPDATE Products SET Category=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 3:
            value = input("New Brand : ")
            cursor.execute(
                "UPDATE Products SET Brand=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 4:
            value = input("New Size : ")
            cursor.execute(
                "UPDATE Products SET Size=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 5:
            value = input("New Color : ")
            cursor.execute(
                "UPDATE Products SET Color=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 6:
            value = float(input("New Selling Price : "))
            cursor.execute(
                "UPDATE Products SET Selling_Price=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 7:
            value = int(input("New Stock : "))
            cursor.execute(
                "UPDATE Products SET Stock=%s WHERE Product_ID=%s",
                (value, product_id)
            )

        elif choice == 8:

            supplier = int(input("New Supplier ID : "))

            cursor.execute(
                "SELECT Supplier_ID FROM Suppliers WHERE Supplier_ID=%s",
                (supplier,)
            )

            if cursor.fetchone() is None:
                print("Supplier ID Not Found")
                continue

            cursor.execute(
                "UPDATE Products SET Supplier_ID=%s WHERE Product_ID=%s",
                (supplier, product_id)
            )

        elif choice == 9:
            conn.commit()
            print("Product Updated Successfully.")
            break

        else:
            print("Invalid Choice")

    cursor.close()
    conn.close()

        # -------------------- DELETE PRODUCT --------------------

def delete_product():

    conn = get_connection()
    cursor = conn.cursor()

    product_id = int(input("Enter Product ID to Delete : "))

    cursor.execute(
        "SELECT * FROM Products WHERE Product_ID=%s",
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:
        print("Product Not Found.")
        cursor.close()
        conn.close()
        return

    print("\n========== PRODUCT DETAILS ==========\n")

    print(
        tabulate(
            [product],
            headers=PRODUCT_HEADERS,
            tablefmt="grid"
        )
    )

    confirm = input("\nAre you sure you want to delete this product? (Y/N): ")

    if confirm.upper() == "Y":

        cursor.execute(
            "DELETE FROM Products WHERE Product_ID=%s",
            (product_id,)
        )

        conn.commit()
        print("Product Deleted Successfully.")

    else:
        print("Delete Cancelled.")

    cursor.close()
    conn.close()
    
        # -------------------- SEARCH PRODUCT --------------------

def search_product():

    conn = get_connection()
    cursor = conn.cursor()

    while True:

        print("\n========== SEARCH PRODUCT ==========")
        print("1. Search by Product ID")
        print("2. Search by Product Name")
        print("3. Search by Category")
        print("4. Search by Brand")
        print("5. Search by Size")
        print("6. Search by Color")
        print("7. Search by Selling Price")
        print("8. Search by Stock")
        print("9. Search by Supplier ID")
        print("10. Back")

        choice = input("Enter Choice : ")

        if choice == "1":
            sql = "SELECT * FROM Products WHERE Product_ID=%s"
            value = int(input("Enter Product ID : "))

        elif choice == "2":
            sql = "SELECT * FROM Products WHERE Product_Name=%s"
            value = input("Enter Product Name : ")

        elif choice == "3":
            sql = "SELECT * FROM Products WHERE Category=%s"
            value = input("Enter Category : ")

        elif choice == "4":
            sql = "SELECT * FROM Products WHERE Brand=%s"
            value = input("Enter Brand : ")

        elif choice == "5":
            sql = "SELECT * FROM Products WHERE Size=%s"
            value = input("Enter Size : ")

        elif choice == "6":
            sql = "SELECT * FROM Products WHERE Color=%s"
            value = input("Enter Color : ")

        elif choice == "7":
            sql = "SELECT * FROM Products WHERE Selling_Price=%s"
            value = float(input("Enter Selling Price : "))

        elif choice == "8":
            sql = "SELECT * FROM Products WHERE Stock=%s"
            value = int(input("Enter Stock : "))

        elif choice == "9":
            sql = "SELECT * FROM Products WHERE Supplier_ID=%s"
            value = int(input("Enter Supplier ID : "))

        elif choice == "10":
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
                    headers=PRODUCT_HEADERS,
                    tablefmt="grid"
                )
            )

        else:
            print("No Product Found.")

        # -------------------- PRODUCT MENU --------------------

def product_menu():

    while True:

        print("\n========== PRODUCT MANAGEMENT ==========")
        print("1. Add Product")
        print("2. View Product")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Search Product")
        print("6. Back to Main Menu")

        choice = input("Enter Your Choice : ")

        if choice == "1":
            add_product()

        elif choice == "2":
            view_product()

        elif choice == "3":
            update_product()

        elif choice == "4":
            delete_product()

        elif choice == "5":
            search_product()

        elif choice == "6":
            print("Returning to Main Menu...")
            break

        else:
            print("Invalid Choice!")
            
if __name__ == "__main__":
    product_menu()
