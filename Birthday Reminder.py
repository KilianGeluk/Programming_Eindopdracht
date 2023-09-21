# This program will send a Signal message informing a user who of their friends their birthday it is today.

# Programmer: Kilian Geluk

import sys
import csv
from datetime import date
import re
import requests
import json

# Globals that will be used to construct the API call
SYSTEMID = "CTYYCerWl2gTI5L"
PASSWORD = "vUObg2JV"
PHONE_NUMBER = "+31616293282"


def main():
    # Validate input
    choice = input_validation()

    # Start the selected option
    if choice == "-a":
        add_birthday()
    elif choice == "-r":
        remove_birthday()
    elif choice == "-l":
        messages = send_birthday_reminders()
        for message in messages:
            send_signal_message(message)
    elif choice == "-h":
        print_help()


# Verify if the commandline argument given is valid, argument is sys.argv and returns the argument if valid.
def input_validation():
    # If there is more than 1 command-line argument given print usage instructions
    if len(sys.argv) > 2:
        sys.exit(print_help())

    # If there is exactly 1 command-line argument given
    if len(sys.argv) == 2:
        if sys.argv[1].lower() == "-a":
            return "-a"
        elif sys.argv[1].lower() == "-r":
            return "-r"
        elif sys.argv[1].lower() == "-l":
            return "-l"
        elif sys.argv[1].lower() in ["-h", "--help"]:
            return "-h"
        else:
            sys.exit(print_help())

    # If no command-line argument is given print usage instructions
    elif len(sys.argv) < 2:
        sys.exit(print_help())


# Function to check valid format in a given birthday YYYY-MM-DD
def is_valid_birthday(birthday):
    match = re.match(
        r"^[0-9]{4}-(1[0-2]|0[1-9])-(3[0-1]|[1-2][0-9]|0[1-9])$", birthday
    )
    if not match:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")


# Add a birthday to a given csv file, by default birthdays.csv
def add_birthday(csv_file="birthdays.csv"):
    with open(csv_file, "a", newline="\n") as csvfile:
        first_name = input("First name: ")
        last_name = input("Last name: ")
        birthday = input("Birthday YYYY-MM-DD: ")

        # Check if the input of birthday is in valid YYYY-MM-DD format
        is_valid_birthday(birthday)

        # If the birthday is of valid format
        person = [first_name, last_name, birthday]
        writer = csv.writer(csvfile)
        writer.writerow(person)

    print("Birthday added!")


# Remove a birthday from a given csv file, by default birthdays.csv, update csv file.
def remove_birthday(csv_file="birthdays.csv"):
    # Read the existing birthdays into the list birthdays[]
    birthdays = []
    with open(csv_file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            birthdays.append(row)

        # Get user input to specify which birthday to remove
        birthday_to_remove = input("Enter the birthday (YYYY-MM-DD) to remove: ")
        first_name_to_remove = input("Enter the first name to remove: ")

        # Check if the birthday entered as input is of valid format
        is_valid_birthday(birthday_to_remove)

        # If the birthday is of valid format find and remove the birthday
        new_birthdays = []
        removed = False
        for birthday in birthdays:
            if birthday[0] == first_name_to_remove and birthday[2] == birthday_to_remove:
                removed = True
                print(f"Removed birthday: {birthday[0]} {birthday[1]} - {birthday[2]}")
            else:
                new_birthdays.append(birthday)

        # If no birthday is found to remove
        if not removed:
            print("Birthday not found.")

    # Write the updated list of birthdays back to the file
    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_birthdays)


def print_help():
    # Print the different options of the program to the user
    print("Usage:")
    print("-a : Add a birthday")
    print("-r : Remove a birthday")
    print("-l : Send a notification if any birthdays today")
    print("-h : Print the help page")


# Function that checks the given csv, by default birthdays.csv
# and both prints and pipes message to send_signal_message
def send_birthday_reminders():
    # Get the current date and year
    today = date.today()
    current_year = today.year

    # Read from the csv file
    with open("birthdays.csv", "r") as csvfile:
        reader = csv.reader(csvfile)

        # Don't include the header line in the loop
        next(reader, None)

        # For each row in the csv file, replace birth year with current year
        messages = []
        for row in reader:
            birthday = row[2]
            birth_year = row[2].split("-")[0]
            birthday_this_year = birthday.replace(str(birth_year), str(current_year))

            # Look for a match between birthday and today
            if str(birthday_this_year) == str(today):
                age = int(current_year) - int(birth_year)
                message = f"Today is {row[0]} {row[1]}'s birthday! They are turning {age} years old."
                print(message)
                messages.append(message)

        return messages


# Function to make a Signal API call sending a message
def send_signal_message(message):
    """
    This code was taken from API documentation at
    https://developers.melroselabs.com/docs/send-signal-with-rest-using-python
    """
    url = "https://api.melroselabs.com/signal/message"

    # Construct the payload for the API call
    payload = {
        "systemid": f"{SYSTEMID}",
        "password": f"{PASSWORD}",
        "destination": f"{PHONE_NUMBER}",
        "text": message,
    }

    # Construct the header for the API call
    headers = {
        'Content-Type': 'application/json'
    }

    # Send an API request
    requests.request("POST", url, headers=headers, data=json.dumps(payload))


if __name__ == "__main__":
    main()
