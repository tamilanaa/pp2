import psycopg2
import csv


def get_connection():
    return psycopg2.connect(
        dbname = "phonebook", 
        user="postgres",
        password="@GFk%ruw", 
        host="localhost",
        port="5432"
    )

# Create tables
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone_number VARCHAR(20)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully.")

# Insert a contact from console input
def insert_from_console():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO contacts (first_name, last_name, phone_number)
        VALUES (%s, %s, %s)
    """, (first_name, last_name, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added.")

# Insert contacts from a CSV file
def insert_from_csv():
    file_path = input("Enter path to CSV file: ")

    conn = get_connection()
    cur = conn.cursor()

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header if needed
        for row in reader:
            first_name, last_name, phone_number = row
            cur.execute("""
                INSERT INTO contacts (first_name, last_name, phone_number)
                VALUES (%s, %s, %s)
            """, (first_name, last_name, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("CSV data uploaded.")

# Update a contact
def update_contact():
    phone_number = input("Enter current phone number of the contact: ")
    new_first = input("Enter new first name (leave blank to skip): ")
    new_last = input("Enter new last name (leave blank to skip): ")

    conn = get_connection()
    cur = conn.cursor()

    if new_first:
        cur.execute("UPDATE contacts SET first_name = %s WHERE phone_number = %s", (new_first, phone_number))
    if new_last:
        cur.execute("UPDATE contacts SET last_name = %s WHERE phone_number = %s", (new_last, phone_number))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact updated.")

# Query contacts
def query_contacts():
    filter_option = input("Search by (1) First Name, (2) Last Name, (3) Phone Number: ")
    value = input("Enter value: ")

    conn = get_connection()
    cur = conn.cursor()

    if filter_option == "1":
        cur.execute("SELECT * FROM contacts WHERE first_name = %s", (value,))
    elif filter_option == "2":
        cur.execute("SELECT * FROM contacts WHERE last_name = %s", (value,))
    elif filter_option == "3":
        cur.execute("SELECT * FROM contacts WHERE phone_number = %s", (value,))
    else:
        print("Invalid choice.")
        return

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

# Delete a contact
def delete_contact():
    phone_number = input("Enter phone number of the contact to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE phone_number = %s", (phone_number,))
    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted.")

# Menu to choose actions
def main_menu():
    init_db()

    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Insert contact from console")
        print("2. Insert contacts from CSV")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
