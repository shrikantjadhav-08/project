from database import get_connection


def add_users():
    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter your username : ")
    password = input("Enter your password : ")
    
    while True:

      role = input("Enter Role (admin/user): ").lower()

      if role in ["admin", "user"]:
        break

      print("Invalid Role! Please enter only admin or user.")



    query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
    values = (username, password, role)

    cursor.execute(query, values)
    conn.commit()

    print("User added successfully...")

    cursor.close()
    conn.close()


def login():

    conn = get_connection()
    cursor = conn.cursor()

    username = input("Enter your username : ")
    password = input("Enter your password : ")

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    values = (username, password)

    cursor.execute(query, values)
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        print("Login Successful...")
        return row[3].lower()      # returns "admin" or "user"

    else:
        print("Invalid Credentials!!!")
        return None
