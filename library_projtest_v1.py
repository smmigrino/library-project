#THIS PROGRAM IS INTENDED FOR LIBRARY ADMIN, NOT A GUEST TO THE LIBRARY

import sqlite3
import time

#connect database
conn = sqlite3.connect('library.db')

#print("Connected to the database successfully.")

#create cursor
cur = conn.cursor()

#create table
cur.execute("""CREATE TABLE IF NOT EXISTS
            books(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, year INTEGER)""")

conn.commit()


#----------------------HEADER------------------------------
print("\nHello, Welcome to LiShen's Library!") 

#--------------------Display Menu--------------------------

def display_menu(first_time=False):
    
    options = ("""
    1 - Add a book
    2 - View book list
    3 - Search a book
    4 - Edit a book entry
    5 - Delete a book
    6 - Exit the library
               """)
    
    if first_time:
        print("\n\nWhat would you like to do? Enter the number for the following option.\n\n", options)
    else:
        print("\n\nSo.....What would you like to do next? Enter the number for the following option.\n\n", options)
        


#---------------------Main Menu Functions-----------------

def add_book():
    print("\nAwesome! Let's add a book. Please enter the following details.")
    title = input("Book title: ")
    author = input("Author: ")
    year = int(input("Publication year (Type 0 for unknown year): "))
    
    
    cur.execute('SELECT COUNT(*) FROM  books WHERE title = ? AND author = ?', (title, author))
    count = cur.fetchone()[0]
    
    if count == 0:
        
        cur.execute("""
                INSERT INTO books(title, author, year) VALUES (?, ?, ?)""", (title, author, year))
        print("\n\nBook successfully added.")
        #print("\n\nBook successfully added with ID:", cur.lastrowid) #if you want to print the ID 
        conn.commit()
    else:
        print("\nBook already in shelves. Try again.")
        

def view_booklist():
    cur.execute("SELECT * FROM books")
    all_books = cur.fetchall()
    
    if all_books:
        print("\n\nHere are all the books...\n")
        time.sleep(3)
    
        for book in all_books:
            print(f"Book ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Publication Year: {book[3]}")
            time.sleep(2)
    else:
        print("\n\nShelves are empty! Add a book! Exiting now...")
        time.sleep(4)
        


    
#--------Main Menu block--------
def main_menu():
    first_time = True
    
    while True:
        display_menu(first_time)
        first_time = False
        
        try:
            choice = int(input("Enter number: "))
        
        except ValueError:
            print("Invalid input. Enter a number in the Menu options.")
            continue    
        
        if choice == 1:
            add_book()    
            
        elif choice == 2:
            view_booklist()

        elif choice == 3:
            print('\n\nExiting... Good bye!')
            time.sleep(1.5)
            conn.close()
            exit()    

        else:
            print("Invalid input. Try again..")
            continue
    conn.close()



#-----Run Program--------
if __name__ == "__main__":
    main_menu()

