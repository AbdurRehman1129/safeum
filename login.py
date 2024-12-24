import os
import time
import re
import json
import argparse

# Helper function to run ADB commands and suppress standard output while preserving errors
def run_adb_command(command):
    return os.system(f"{command} >nul 2>&1")  # Redirect stdout to null, keep stderr

# Function to check if the login page is visible
def is_login_page():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "com.safeum.android:id/et_login" in xml_content and "com.safeum.android:id/et_password" in xml_content and "com.safeum.android:id/login_button" in xml_content

# Function to check if the GO TO AUTH button is visible
def is_go_to_auth_button():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "GO TO AUTH" in xml_content

# Function to check if the progress bar is visible
def is_progress_bar_visible():
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    return "android:id/progress" in xml_content

# Function to check if "Invite" or "Settings" button is visible
def check_for_buttons(setup_data):
    run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
    run_adb_command("adb pull /sdcard/window_dump.xml .")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()

    # Use coordinates for checking buttons dynamically
    if "Invite" in xml_content:
        return "invite"
    elif "Settings" in xml_content:
        return "settings"
    else:
        return None

# Function to automate login
def automate_login(setup_data, username, password):
    print(f"Logging in with username: {username}")
    username_coords = tuple(map(int, setup_data["username_field"].split(',')))
    password_coords = tuple(map(int, setup_data["password_field"].split(',')))
    login_coords = tuple(map(int, setup_data["login_button"].split(',')))

    run_adb_command(f"adb shell input tap {username_coords[0]} {username_coords[1]}")
    run_adb_command(f"adb shell input text {username}")
    run_adb_command(f"adb shell input tap {password_coords[0]} {password_coords[1]}")
    run_adb_command(f"adb shell input text {password}")
    run_adb_command(f"adb shell input tap {login_coords[0]} {login_coords[1]}")

# Function to launch SafeUM app
def launch_safeum():
    print("Launching SafeUM app...")
    run_adb_command("adb shell monkey -p com.safeum.android 1")

# Wait for progress bar to disappear
def wait_for_progress_bar_to_disappear():
    print("Waiting for the progress bar to disappear...")
    while True:
        if not is_progress_bar_visible():
            print("Progress bar disappeared!")
            break
        time.sleep(1)

# Function to extract phone number from the screen XML
def extract_phone_number():
    print("Extracting phone number...")
    with open("window_dump.xml", "r", encoding="utf-8") as file:
        xml_content = file.read()
    phone_number_pattern = r'\b9944[\d\s]{10}\b'
    phone_numbers = re.findall(phone_number_pattern, xml_content)
    time.sleep(0.12)
    if phone_numbers:
        for number in phone_numbers:
            print("Found phone number:", number)
        return phone_numbers
    else:
        return []

# Function to log out from SafeUM
def logout(setup_data, username):
    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account control" in xml_content:
            print("Found Account control, clicking button...")
            account_control_coords = tuple(map(int, setup_data["account_control_button"].split(',')))
            run_adb_command(f"adb shell input tap {account_control_coords[0]} {account_control_coords[1]}")
            run_adb_command(f"adb shell input tap {account_control_coords[0]} {account_control_coords[1]}")
            break
        time.sleep(1)

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if username in xml_content:
            print("Username found, clicking logout...")
            logout_coords = tuple(map(int, setup_data["logout_button"].split(',')))
            run_adb_command(f"adb shell input tap {logout_coords[0]} {logout_coords[1]}")
            break
        time.sleep(1)

    while True:
        run_adb_command("adb shell uiautomator dump /sdcard/window_dump.xml")
        run_adb_command("adb pull /sdcard/window_dump.xml .")
        with open("window_dump.xml", "r", encoding="utf-8") as file:
            xml_content = file.read()
        if "Account exit" in xml_content:
            print("Found Account exit Page, clicking Keep on device...")
            keep_device_coords = tuple(map(int, setup_data["keep_in_device_button"].split(',')))
            run_adb_command(f"adb shell input tap {keep_device_coords[0]} {keep_device_coords[1]}")
            break
        time.sleep(1)

# Function to save the setup configuration
def save_setup(setup_name, setup_data):
    setups = load_setups()
    setups[setup_name] = setup_data
    with open("setups.json", "w", encoding="utf-8") as f:
        json.dump(setups, f, ensure_ascii=False, indent=4)
    print(f"Setup '{setup_name}' saved successfully!")

# Function to load all setups
def load_setups():
    if os.path.exists("setups.json"):
        with open("setups.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# Function to setup the coordinates for UI elements
def setup_coordinates():
    print("Please enter the coordinates for the following UI elements:")

    # Collect the coordinates
    setup_data = {
        "username_field": input("Username field coordinates (x,y): ").strip(),
        "password_field": input("Password field coordinates (x,y): ").strip(),
        "login_button": input("Login button coordinates (x,y): ").strip(),
        "go_to_auth_button": input("GO TO AUTH button coordinates (x,y): ").strip(),
        "settings_button": input("Settings button coordinates (x,y): ").strip(),
        "account_control_button": input("Account control button coordinates (x,y): ").strip(),
        "logout_button": input("Logout button coordinates (x,y): ").strip(),
        "keep_in_device_button": input("Keep in device button coordinates (x,y): ").strip()
    }

    setup_name = input("Enter a name for this setup: ").strip()
    save_setup(setup_name, setup_data)

# Function to load a specific setup
def load_setup_by_name(setup_name):
    setups = load_setups()
    if setup_name in setups:
        return setups[setup_name]
    else:
        print(f"Setup '{setup_name}' not found!")
        return None

# Main function to login and logout multiple accounts
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Automate SafeUM login process.")
    parser.add_argument("--setup", type=str, help="Specify the setup name to use.")
    args = parser.parse_args()

    # If a setup name is provided, load that setup
    setup_data = None
    if args.setup:
        setup_data = load_setup_by_name(args.setup)
        if setup_data:
            print(f"Loaded setup '{args.setup}' successfully.")
    
    if setup_data is None:
        # If no setup is provided or failed to load, ask the user to create a new one
        print("No setup provided or failed to load, please create a new one.")
        setup_coordinates()

    usernames = input("Enter usernames separated by commas: ").split(',')
    usernames = [username.strip() for username in usernames if username.strip()]
    password = input("Enter password for all accounts: ")

    # Launch SafeUM app
    launch_safeum()
    time.sleep(3)  # Wait for the app to load

    for username in usernames:
        print(f"\nProcessing account: {username}")

        # Login
        for attempt in range(10):
            print(f"Checking for login page or GO TO AUTH button... Attempt {attempt + 1}")
            if is_go_to_auth_button():
                print("GO TO AUTH button found! Clicking it...")
                run_adb_command("adb shell input tap 395 1524")  # Coordinates for the GO TO AUTH button
                time.sleep(1)  # Wait for the transition
            if is_login_page():
                print("Login page found!")
                automate_login(setup_data, username, password)
                break
            else:
                print("Neither GO TO AUTH nor Login page found.")
            time.sleep(2)
        else:
            print(f"Login page not found for {username}, skipping...")

        # Wait for progress bar
        wait_for_progress_bar_to_disappear()

        # Check for and click the appropriate button
        print("Checking for Settings button...")
        while True:
            
            button = check_for_buttons(setup_data)
            if button == "settings":
                print("Clicking the Settings button...")
                run_adb_command(f"adb shell input tap {setup_data['settings_button']}")
                break

        # Extract phone number
        phone_numbers = extract_phone_number()
        if phone_numbers:
            print(f"Phone number for {username} has been extracted.")
        
        # Logout
        logout(setup_data, username)
        print(f"Logged out from account: {username}\n")

def display_accounts(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            accounts = json.load(file)
            print("Extracted Accounts:")
            for account in accounts:
                print(account)
    else:
        print(f"No file named '{file_name}' found.")
# Display the menu
def displaymenu():
    print("\nMENU:")
    print("1. Extract phone numbers from SafeUM.")
    print("2. Display Extracted accounts.")
    print("3. Setup coordinates.")
    print("4. Exit")

if __name__ == "__main__":
    while True:
        displaymenu()
        choice = int(input("\nEnter Your choice: "))
        if choice == 1:
            main()
            input("\nPress any key to go back to main menu...")
        elif choice == 2:
            display_accounts('extracted_phone_numbers.json')
            input("\nPress any key to go back to main menu...")
        elif choice == 3:
            setup_coordinates()
            input("\nPress any key to go back to main menu...")
        elif choice == 4:
            exit("Exiting...")
        else:
            print("Invalid input...")
            input("\nPress any key to go back to main menu...")
