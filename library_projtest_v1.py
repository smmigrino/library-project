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
    2 - View all books
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
    
    #helper validators for duplicate handling and empty entries
    while True:
        title = input("Book title: ").strip().upper()
        if title:
            break
        print("Please enter title.")
        
    while True:    
        author = input("Author: ").strip().upper()
        if author:
            break
        print("Please enter author name.")
    
    while True:

        try:
            year = input("Publication year (Type 0 for unknown year): ").strip()    
            year = int(year)
            break
        
        except ValueError:
            print("Please enter valid year or 0 if year is unknown.")
                    

    #duplicate handling portion    
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
        

def search():
    while True:
        print("(Enter 'EXIT' to go back to Main Menu.)")
        to_search = input("To Search, enter Title/Author/Publication Year: ")
        
        try:
            to_search = int(to_search)
            cur.execute("SELECT * FROM books WHERE year = ?", (to_search,))
            book_list = cur.fetchall()
            
            if book_list:
                for book in book_list:
                    id, title, author, year = book
                    print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year} ")
                    time.sleep(1.5)
            else:        
                print("No match. Try again.")
            continue
        
        except ValueError:
            if to_search == 'EXIT':
                break
            elif to_search != "":
                to_search = to_search.upper()
                cur.execute('SELECT * FROM books  WHERE title LIKE ? OR author LIKE ?', (f"%{to_search}%", f"%{to_search}%"))
                book_list = cur.fetchall()
                
                if book_list:
                    for book in book_list:
                        id, title, author, year = book
                        print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year} ")
                else:    
                    print("No match. Try again.")
                continue
            else:
                print("Enter valid input. Try again.")
                continue

def edit_by_id():
    while True:
        id_search = input("Enter ID: ").strip()
         
        try:
            id_search = int(id_search)
            while True:
                new_title = input("Book title: ").strip().upper()
                if new_title:
                    break
                print("Please enter title.")
                
            while True:    
                new_author = input("Author: ").strip().upper()
                if new_author:
                    break
                print("Please enter author name.")
            
            while True:

                try:
                    new_year = input("Publication year (Type 0 for unknown year): ").strip()    
                    new_year = int(new_year)
                    break
                
                except ValueError:
                    print("Please enter valid year or 0 if year is unknown.")
                            

            #duplicate handling portion    
            cur.execute('SELECT COUNT(*) FROM  books WHERE title = ? AND author = ? AND id != ?', (new_title, new_author, id_search))
            count = cur.fetchone()[0]
            

            if count == 0:
                
                cur.execute("""
                        UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?""", (new_title, new_author, new_year, id_search))
                print("\n\nBook successfully updated.")
                conn.commit()
                break
            else:
                print("\nBook already in shelves. Try again.")
                        
                       
        except ValueError:
            print("Enter valid ID number. Try again.")
            continue


def edit_book():     
        
    while True:
        user_input = input("Do you know the ID? (y/n)").strip().lower()
        
        if user_input == 'n':
            search()
            edit_by_id()
            break

            
        elif user_input == 'y':
            edit_by_id()
            break
            
        else:
            print("Enter 'y' for yes, or 'n'  for no. Try again.")    


    
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
            search()
            
        elif choice == 4:
            edit_book()
            
        elif choice == 5:
            print("Delete functions still in development hehehehe")
        
        elif choice == 6:
            print("Exiting the library...")
            time.sleep(1)
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("Good bye!")
            break
    
        else:
            print("Invalid input. Try again..")
            
    conn.close()



#-----Run Program--------
if __name__ == "__main__":
    main_menu()

