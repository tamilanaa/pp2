from db import get_connection

def delete_by():
    try:
        conn = get_connection()
        cur = conn.cursor()

        choice = input("Delete by (1) Name or (2) Phone? ")

        if choice == "1":
            first = input("Enter first name: ")
            last = input("Enter last name: ")

            cur.execute("SELECT delete_contact_by_name(%s, %s);", (first, last))

        elif choice == "2":
            phone = input("Enter phone number: ")

            cur.execute("SELECT delete_contact_by_phone(%s);", (phone,))
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



def paginate_contacts(limit, offset):
    try:
        conn = get_connection()
        cur = conn.cursor()

        query = "SELECT * FROM contacts LIMIT %s OFFSET %s;"
        cur.execute(query, (limit, offset))

        rows = cur.fetchall()

        if not rows:
            print("No more records.")
        else:
            for row in rows:
                print(row)

    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()



def search_by_pattern(pattern):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM search_contacts_by_pattern(%s);", (pattern,))
        results = cur.fetchall()

        
        if results:
            for row in results:
                print(row)
        else:
            print("No matching contacts found.")


    except Exception as e:
        print("Error:", e)
    finally:
        if conn:
            cur.close()
            conn.close()