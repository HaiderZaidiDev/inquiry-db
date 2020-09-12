import sqlite3
import os

# Inquiry Database

def backToMenu():
    """ Returns to the main menu upon key press. """
    print("\nPress enter to return to the main menu.")
    listener = input()
    if listener == '':
        menu()
    else:
        pass

def addInquiry():
    """ Adds inquiry information to db. """
    os.system('clear')
    print("Enter the inquiry information below.")
    name = input("Name: ")
    machine = input("Machine: ")
    contact = input("Contact: ")

    conn = sqlite3.connect("inquiries.db")
    c = conn.cursor()
    c.execute("INSERT INTO customers (name, machine, contact) values(?,?,?)", (name, machine, contact))
    conn.commit()
    conn.close()
    backToMenu()

def searchInquiry():
    """ Displays inquiry search menu. """
    os.system('clear')
    print("1. Search by Name: ")
    print("2. Search by Machine: ")
    try:
        option = int(input("Select an option from the list above:"))
        if option not in [1, 2]:
            raise ValueError()
        if option == 1:
            searchName()
        if option == 2:
            searchMachine()
    except ValueError:
        print("Error: Invalid option selected, you must enter a number.")
        menu()

def searchName():
    """ Matches a name to inquiry in the db. """
    os.system('clear')
    print("Check what machine a customer is looking for")
    names = input("Name(s): ").split(', ')
    conn = sqlite3.connect("inquiries.db")
    c = conn.cursor()
    for i in range(len(names)):
        try:
            machineRaw = c.execute("SELECT machine FROM customers WHERE name=?",(names[i],),).fetchone()
            machine, = machineRaw # Unpacking machine name from tuple.
            print("{0} placed an inquiry for: {1}".format(names[i], machine))
        except TypeError:
            print("{} does not have any inquiries.".format(names[i]))
    conn.close()
    backToMenu()

def searchMachine():
    """ Matches a machine to a name in the db. """
    os.system('clear')
    print("Match a machine to a customer")
    machine = input("Machine: ")
    conn = sqlite3.connect("inquiries.db")
    c = conn.cursor()
    namesRaw = c.execute("SELECT name, contact FROM customers WHERE machine=?",(machine,),).fetchall()
    if namesRaw:
        for i in range(len(namesRaw)):
            name, contact = namesRaw[i]
            print("{0} is looking for a {1}, their contact information is: {2}".format(name, machine, contact))
    if not namesRaw: # Usually raised if name is NoneType
        print("There are no customers currently looking for: {}".format(machine))

    conn.close()
    backToMenu()

def menu():
    """ Displays the main menu."""
    os.system('clear')
    print("1. Add an Inquiry")
    print("2. Search Current Inquiries")
    try:
        option = int(input("Select an option from the list above:"))
        if option not in [1, 2]:
            raise ValueError()
        if option == 1:
            addInquiry()
        if option == 2:
            searchInquiry()
    except ValueError:
        print("Error: Invalid option selected, you must enter a number.")
        menu()
menu()
