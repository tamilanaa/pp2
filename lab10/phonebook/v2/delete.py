from db import get_connection

def delete_contact():
    first_name = input("Enter the first name of the contact to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE first_name = %s", (first_name,))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted.")
