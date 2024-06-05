from operations import *

def main():
    while True:
        print("\nMenu:")
        print("1. Hash")
        print("2. Statistical Analysis")
        print("3. Insert the hashed Data to Disconnections_Primary Table")
        print("4. Decryption")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            opt1()
        elif choice == '2':
            opt2()
        elif choice == '3':
            opt3()
        elif choice == '4':
            opt4()
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
