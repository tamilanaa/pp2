from db import get_connection

def update_contact():
    name = input("Enter the first name of the contact to update: ")
    field = input("What do you want to update? (first_name, last_name, phone_number): ")
    new_value = input(f"Enter new {field}: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        UPDATE contacts
        SET {field} = %s
        WHERE first_name = %s
    """, (new_value, name))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")
