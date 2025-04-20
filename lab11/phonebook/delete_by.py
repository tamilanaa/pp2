
from db import get_connection

def delete_by():
    try:
        conn = get_connection()
        cur = conn.cursor()

        choice = input("Delete by (1) Name or (2) Phone? ")

        if choice == "1":
            first = input("Enter first name: ")
            last = input("Enter last name: ")

            cur.execute("""
                DELETE FROM contacts 
                WHERE first_name = %s AND last_name = %s
            """, (first, last))

        elif choice == "2":
            phone = input("Enter phone number: ")

            cur.execute("""
                DELETE FROM contacts 
                WHERE phone_number = %s
            """, (phone,))
        else:
            print("Invalid choice.")
            return

        conn.commit()
        print("Contact(s) deleted))")

    except Exception as e:
        print("error:", e)
    finally:
        cur.close()
        conn.close()
