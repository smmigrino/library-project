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


#----------------------Constants---------------------------
seconds_short = .5
seconds_long = 1

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
    print("-" *20 + "ADD MENU" + "-" *20)
    print("\nAwesome! Let's add a book. Please enter the following details.")
    print("If you want to return to the Main Menu, type '#EXIT'.")
    
    #helper validators for duplicate handling and empty entries
    while True:
        title = input("Book title: ").strip().upper()
        
        if title == '#EXIT':
            print("Returning to Main Menu...")
            return
        
        elif title:
            break
        else:
            print("Please enter title.")
        
    while True:    
        author = input("Author: ").strip().upper()
        
        if author == '#EXIT':
            print("Returning to Main Menu...")
            return
        
        elif author:
            break
        
        else:
            print("Please enter author name.")
    
    while True:
        year = input("Publication year (Type 0 for unknown year): ").strip().upper()
         
        if year == '#EXIT':
            print("Returning to Main Menu...")
            return
     
        elif year:
            try:
                year = int(year)
                break
            
            except ValueError:
                print("Please enter valid year or 0 if year is unknown.")
        else:
            print("Enter valid year or 0 if year is unknown.")
                        

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
    print("-" *20, "ALL BOOK ENTRIES", "-" *20)
    cur.execute("SELECT * FROM books")
    all_books = cur.fetchall()
    
    if all_books:
        print("\n\nHere are all the books...\n")
        time.sleep(3)
    
        for book in all_books:
            print(f"Book ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Publication Year: {book[3]}")
            time.sleep(seconds_short)
    else:
        print("\n\nShelves are empty! Add a book!")
        time.sleep(seconds_long)
        

def search():
    print("-" *20, "SEARCH A BOOK", "-" *20)
    while True:
        print("(If you want to return to the Main Menu, type '#EXIT')") #you need to think this through and clean this up
        to_search = input("To Search a book entry, enter Title/Author/Publication Year: ")
        
        try:
            to_search = int(to_search) #to search by year
            cur.execute("SELECT * FROM books WHERE year = ?", (to_search,))
            book_list = cur.fetchall()
            
            if book_list:
                for book in book_list:
                    id, title, author, year = book
                    print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year} ")
                    time.sleep(seconds_short)
            else:        
                print("No match. Try again.")
            
        
        except ValueError:
            if to_search == '#EXIT': #go back here and clean this up
                print("Returning to main menu.")
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

def delete_by_id():
    book_id = input("Enter book ID: ")
    cur.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    show_book = cur.fetchall()

    id, title, author, year = show_book
    print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year}")

    while True:    
        confirm = input("\nAre you sure you want to delete this book entry? (y/n): ").lower()

        if confirm == 'y':
            cur.execute('DELETE FROM books WHERE id = ?', (book_id,))
            print("Book entry successfully deleted. Returning to Delete Menu.")
            break
        
        elif confirm == 'n':
            print("Returning to DELETE MENU.")
            break
        
        else:
            ("Invalid input. Try again.")
    

def delete_book():

    
    while True:
        print("----------DELETE MENU----------","""
Enter the number to choose the following:
    1 - Delete a book entry
    2 - Delete all book entries
    3 - Return to main menu""")
        
        choice = input("Enter number: ")
        
        try:
            choice = int(choice)
            
            
            if choice == 1:
                while True:
                    confirm = input("Do you know the ID number? (y/n): ").strip().lower()
                    
                    if confirm == 'y':
                        delete_by_id()
                        break                    
                        
                    elif confirm == 'n':
                        while True:
                            choice = input("""
Enter the number for the following:
    1 - Search a book
    2 - Show all book list
    3 - Return to Delete Menu""")
                            try:
                                choice = int(choice)
                                if choice == 1:
                                    search()
                                    delete_by_id
                                    break
                                                                
                                elif choice == 2:
                                    view_booklist()
                                    delete_by_id()
                                    break
                                                    
                                elif choice == 3:
                                    break
                                break
                            except ValueError:
                                print("Invalid entry. Enter number of your choice. Try again.")                        
                      
                    else:
                        print("Enter 'y' for yes, and 'n' for no. Try again.")
            
            if choice == 2:
                confirm = input("Are you sure you want to delete all book entries? (y/n): ").lower()
                if confirm == 'y':
                    cur.execute('DELETE FROM books')
                    print("All book entries successfully deleted. Returning to Delete Menu.")
                    time.sleep(seconds_long)
                    break
                elif confirm == 'n':#EDIT THIS 
                    print('hello')
                        
            
        except ValueError:
            print("Invalid input. Try again. Enter a number within the following choices.")
            
            
    

    
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
        
        if choice == 1: #ADD BOOK
            print("-" * 50)   
            add_book()
            print("-" * 50)    
            
        elif choice == 2: #PRINT ALL BOOKS
            print("-" * 50)
            view_booklist()
            print("-" * 50)

        elif choice == 3: #SEARCH A BOOK
            print("-" * 50)
            search()
            print("-" * 50)
            
        elif choice == 4: #EDIT A BOOK
            print("-" * 50)
            edit_book()
            print("-" * 50)
            
        elif choice == 5: #DELETE BOOK(s)
            cur.execute()
            #print("Delete functions still in development hehehehe")
        
        elif choice == 6:
            print("Exiting the library...")
            time.sleep(seconds_short)
            print("3")
            time.sleep(seconds_short)
            print("2")
            time.sleep(seconds_long)
            print("1")
            time.sleep(seconds_long)
            print("Good bye!")
            print("-" * 50)
            break
    
        else:
            print("Invalid input. Try again..")
            
    conn.close()



#-----Run Program--------
if __name__ == "__main__":
    main_menu()

