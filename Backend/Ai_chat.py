from ollama import chat
from database import get_connection
conversation = [
    {
        "role": "system",
        "content": """
You are an AI Assistant for a Clothing Inventory Management System.

Your job is to help users understand:
- Products
- Inventory
- Sales
- Suppliers

Reply in simple English.
"""
    }
]


def ai_assistant():
    conn = get_connection()
    cursor = conn.cursor()

    print("\n========== AI INVENTORY ASSISTANT ==========")
    print("Type 'exit' to return to Main Menu.\n")

    while True:

        user_input = input("You : ")
        text = user_input.lower()

        if "all products" in text:

            cursor.execute("""
                SELECT Product_Name
                FROM Products
            """)

            products = cursor.fetchall()

            product_list = "\n".join(
                [product[0] for product in products]
            )

            prompt = f"""
        User asked:

        Show all products.

        Database returned:

        {product_list}

        Reply politely.
        """

            response = chat(
                model="llama3.2",
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )

            print("\nAI :", response.message.content)

            continue
                

        if user_input.lower() == "exit":
            print("Returning to Main Menu...")
            break

        conversation.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = chat(
            model="llama3.2",
            messages=conversation
        )

        reply = response.message.content

        print("\nAI :", reply)

        conversation.append(
            {
                "role": "assistant",
                "content": reply
            }
        )
