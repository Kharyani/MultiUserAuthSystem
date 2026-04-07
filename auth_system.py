import re
import hashlib
import json
import os

# ------------------ Constants ------------------
DATA_FILE = "users.json"

# ------------------ Utility Functions ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_strong_password(password):
    # Minimum 8 chars, at least 1 uppercase, 1 lowercase, 1 number
    if (len(password) >= 8 and
        re.search(r"[A-Z]", password) and
        re.search(r"[a-z]", password) and
        re.search(r"[0-9]", password)):
        return True
    return False

def is_valid_email(email):
    # Simple regex for email validation
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def load_users():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

# ------------------ Core Functions ------------------
def register():
    users = load_users()

    username = input("Enter Username: ")
    email = input("Enter Email: ")
    password = input("Enter Password: ")

    # Check duplicate username
    if username in users:
        print("❌ Username already exists")
        return

    # Check duplicate email
    for user in users.values():
        if user["email"] == email:
            print("❌ Email already registered")
            return

    # Validate email format
    if not is_valid_email(email):
        print("❌ Invalid email format")
        return

    # Validate strong password
    if not is_strong_password(password):
        print("❌ Weak password! Must be 8+ chars with uppercase, lowercase, number")
        return

    # Save user with hashed password
    users[username] = {
        "email": email,
        "password": hash_password(password)
    }

    save_users(users)
    print("✅ Registration Successful!")

def login():
    users = load_users()

    username_or_email = input("Enter Username or Email: ")
    password = input("Enter Password: ")

    hashed_input = hash_password(password)

    for username, data in users.items():
        if username == username_or_email or data["email"] == username_or_email:
            if data["password"] == hashed_input:
                print(f"✅ Login Successful! Welcome {username}")
                return
            else:
                print("❌ Incorrect Password")
                return

    print("❌ User not found")

def reset_password():
    users = load_users()

    username_or_email = input("Enter your Username or Email: ")

    for username, data in users.items():
        if username == username_or_email or data["email"] == username_or_email:
            new_password = input("Enter new password: ")

            if not is_strong_password(new_password):
                print("❌ Weak password! Must be 8+ chars with uppercase, lowercase, number")
                return

            users[username]["password"] = hash_password(new_password)
            save_users(users)
            print("✅ Password Reset Successful!")
            return

    print("❌ User not found")

def delete_account():
    users = load_users()

    username_or_email = input("Enter your Username or Email: ")

    for username, data in list(users.items()):
        if username == username_or_email or data["email"] == username_or_email:
            confirm = input(f"Are you sure you want to delete {username}'s account? (yes/no): ")
            if confirm.lower() == "yes":
                users.pop(username)
                save_users(users)
                print("✅ Account Deleted Successfully!")
            else:
                print("❌ Deletion Cancelled")
            return

    print("❌ User not found")

# ------------------ Menu ------------------
def main_menu():
    while True:
        print("\n==== Authentication System ====")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Delete Account")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            reset_password()
        elif choice == "4":
            delete_account()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

# ------------------ Main ------------------
if __name__ == "__main__":
    main_menu()