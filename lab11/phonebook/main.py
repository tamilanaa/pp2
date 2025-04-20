from db import init_db
from insert import insert_from_console, insert_from_csv
from update import update_contact
from query import query_contacts
from delete import delete_contact
from pagination import paginate_query
from delete_by import delete_by
from search_pattern import search_by_pattern

def main_menu():
    init_db()

    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert contact from console")
        print("2. Insert contacts from CSV")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Paginate contacts")
        print("7. Delete by name or phone")
        print("8. Search by pattern")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()

        elif choice == '6':
            limit = int(input("Enter limit (how many rows): "))
            offset = int(input("Enter offset (starting from which row): "))
            paginate_query('contacts', limit, offset) 

        elif choice == "7":
            delete_by()
        elif choice == "8":
            pattern = input("Enter part of name, surname or phone: ")
            search_by_pattern(pattern)

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
