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


#----------------------CONSTANTS---------------------------

invalid_yes_no = "Invalid input. Enter 'y' for YES and 'n' for NO. Try again."
invalid_num_choice = "Invalid input. Enter the number of your choice."
error_return_main = "Error occurred. Returning to Main Menu."
invalid_id = "Invalid input. Enter valid ID number. Try again."
invalid_basic = "Enter valid input. Try again."
no_match = "No match. Try again."
invalid_year = "Enter valid year or 0 if year is unknown."
#--------------------Display Menu--------------------------

def display_menu(first_time=False):
    
    options = ("""
    1 - Add a book
    2 - View all books
    3 - Search a book
    4 - Edit a book entry
    5 - Delete book(s)
    6 - Exit the library
               """)
    
    if first_time:
        print("\n\nWhat would you like to do? Enter the number for the following option.\n\n", options)
    else:
        print("\n\nSo.....What would you like to do next? Enter the number for the following option.\n\n", options)
        


#---------------------Main Menu Functions-----------------



def confirm_repeat(action):
    """HELPER FUNC: ASK USER IF THEY WANT TO REPEAT THE ACTION"""
    while True:
        choice = input(f"Would you like to {action}? (y/n): ").lower()
        
        if choice == 'y':
            return 'repeat'
        
        elif choice == 'n':
            return 'stop'
        
        else: 
            print(invalid_yes_no)
    

def add_book():
    print("-" *20 + "ADD MENU" + "-" *20)
    while True:
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
            year = input("Publication year (Type 0 for unknown year): ").strip().upper()
            if not year:
                print(invalid_year)
                continue                     
            try:
                year = int(year)
                break           
            except ValueError:
                print(invalid_year)

        #duplicate handling portion      
        cur.execute('SELECT COUNT(*) FROM  books WHERE title = ? AND author = ?', (title, author))
        count = cur.fetchone()[0]
            
        if count == 0:    
            cur.execute("""
                    INSERT INTO books(title, author, year) VALUES (?, ?, ?)""", (title, author, year))
            print("\n\nBook successfully added.")
            #print("\n\nBook successfully added with ID:", cur.lastrowid) #if you want to print the ID 
            conn.commit()
            sub_choice = confirm_repeat('add another book')
            if sub_choice == 'stop':
                return
            elif sub_choice == 'repeat':
                continue
            else:
                print(error_return_main)
                return
        else:
            print("\nBook already in shelves. Try again.")
        
def prompt_add_or_menu():
    while True:
        print("""\nWhat would you like to do next?\n
    1 - Add Book
    2 - Return to Main Menu""")
        choice = input("\nEnter the number of your choice: ").strip()
        if choice == '1':
            add_book()
        elif choice == '2':
            return 'return'
        else:
            print(f"\n{invalid_num_choice}")

def view_booklist():
    print("-" *20, "ALL BOOK ENTRIES", "-" *20)
    cur.execute("SELECT * FROM books")
    all_books = cur.fetchall()
    
    if not all_books:
        print("\n\nShelves are empty! Add a book!")
        choice = prompt_add_or_menu()
        if choice == 'return':
            return
    else:            
        print("\n\nHere are all the books...\n")
        time.sleep(seconds_long)

        for book in all_books:
            id, title, author, year = book
            print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year}")
            time.sleep(seconds_short)
        choice = prompt_add_or_menu()
        if choice == 'return':
            return


def search():
    """SEARCH FUNCTION WHERE USER CAN SEARCH BOOK ENTRIES"""
    
    print("-" *20 + "SEARCH A BOOK" + "-" *20)
    while True:
        to_search = input("To Search a book entry, enter Title/Author/Publication Year: ").strip().upper()
        
        #to search by year
        try:
            to_search = int(to_search) 
            cur.execute("SELECT * FROM books WHERE year = ?", (to_search,))
            book_list = cur.fetchall() 
            
            if not book_list:
                print(no_match)
                continue
                
            for book in book_list:
                id, title, author, year = book
                print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year} ")
                time.sleep(seconds_short)
            sub_choice = confirm_repeat('search another book')
            if sub_choice == 'stop':
                return
            elif sub_choice == 'repeat':
                continue
            else:
                print(error_return_main)
                return

        except ValueError:
            if to_search == "":
                print(invalid_basic)
                continue
            
            cur.execute('SELECT * FROM books  WHERE title LIKE ? OR author LIKE ?', (f"%{to_search}%", f"%{to_search}%"))
            book_list = cur.fetchall()
            
            if not book_list:
                print(no_match)
                continue
                
            for book in book_list:
                id, title, author, year = book
                print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year} ")
            sub_choice = confirm_repeat('search another book')
            if sub_choice == 'stop':
                return
            elif sub_choice == 'repeat':
                continue
            else:
                print(error_return_main)
                return              

def edit_by_id():
    """HELPER FUNC FOR EDIT MENU: EDITING ENTRIES BY ID"""
    while True: 
        id_search = input("Enter ID: ").strip()
        try:
            id_search = int(id_search)
            cur.execute('SELECT * FROM books WHERE id = ?', (id_search,))
            show_book = cur.fetchone()
            if show_book is None:
                print("ID not found. Try again.")
                continue
            id, title, author, year = show_book
        
            #display entry for user verification
            print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication year: {year}")
            
            while True:
                choice = input("Are you sure you want to edit this book entry? (y/n): ").strip().lower() 
                if choice == 'y':
                    while True:
                        new_title = input("Edit title: ").strip().upper()
                        if new_title:
                            break
                        print("Please enter title.")
                                                    
                    while True:    
                        new_author = input("Edit Author: ").strip().upper()
                        if new_author:
                            break
                        print("Please enter author name.")
                    
                    while True:
                        new_year = input("Edit publication year (Type 0 for unknown year): ").strip() 
                        try:   
                            new_year = int(new_year)
                            break           
                        except ValueError:
                            print(invalid_year)
            
                    #to check whether the new entry doesnt exist already    
                    cur.execute('SELECT COUNT(*) FROM  books WHERE title = ? AND author = ? AND id != ?', (new_title, new_author, id_search))
                    count = cur.fetchone()[0]
                    
                    if count == 0:
                        cur.execute("""
                            UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?""", (new_title, new_author, new_year, id_search))
                        print("\n\nBook successfully updated.")
                        conn.commit()
                        return #return to main edit menu
                        
                    else:
                        print("\nBook already in shelves. Try again.")
                    
                    
                elif choice =='n':
                    return #return to main edit menu
                
                else:
                    print(invalid_yes_no)

        except ValueError:
            print(invalid_id)
           

def edit_book():
    """FUNCTION CONTROLLER: EDIT BOOK ENTRIES""" 
    print("-" *20 + "EDIT MENU" + "-" *20)
    while True:
        user_input = input("Do you know the ID? (y/n): ").strip().lower()
        
        if user_input == 'n':
            search()
            print("-" *20 + "EDIT BOOK ENTRY" + "-" *20)
            edit_by_id()
            sub_choice = confirm_repeat('edit another book')
            if sub_choice == 'stop':
                return
            else:
                continue
       
        elif user_input == 'y':
            edit_by_id()
            sub_choice = confirm_repeat('edit another book')
            if sub_choice == 'stop':
                return
            else:
                continue          
        else:
            print(invalid_yes_no)    


def delete_by_id():
    while True:
        book_id = input("Enter book ID: ")      
        try:
            book_id = int(book_id)
            cur.execute('SELECT * FROM books WHERE id = ?', (book_id,))
            show_book = cur.fetchone()
            if show_book is None:
                print(no_match)
                continue
            id, title, author, year = show_book
            print(f"Book ID: {id} | Title: {title} | Author: {author} | Publication Year: {year}")
            break       
        except ValueError:
            print("Enter valid ID. Try again.")

    while True:    
        delete = input("\nAre you sure you want to delete this book entry? (y/n): ").strip().lower()
        if delete == 'y':
            cur.execute('DELETE FROM books WHERE id = ?', (book_id,))
            conn.commit()
            print("Book entry successfully deleted.")
            return    
        elif delete == 'n':
            print("Returning to DELETE MENU.")
            return    
        else:
            print(invalid_yes_no)

def del_no_id_menu():
    while True:
        print("""
Enter the number for the following:
    1 - Search a book
    2 - Show all book list
    3 - Return to Delete Menu""")
        choice = input("Enter number: ")
        try:
            choice = int(choice)
            if choice == 1:
                print("-" *20 + "SEARCH MODE IN DELETE MENU" + "-" *20)
                search()
                print("-" *20 + "DELETE BOOK ENTRY" + "-" *20)
                delete_by_id()
                return
            elif choice == 2:
                view_booklist()
                print("-" *20 + "VIEW BOOKLIST MODE IN DELETE MENU" + "-" *20)
                print("-" *20 + "DELETE BOOK ENTRY" + "-" *20)
                delete_by_id()
                return                  
            elif choice == 3:
                return 'back'
            else:
                print(invalid_num_choice)

        except ValueError:
            print(invalid_num_choice)     
   

def delete_book():
    """CONTROLLER FUNCTION FOR DELETE"""
    while True:
        print("-" *20 + "DELETE MENU" + "-" *20)
        print("""
Enter the number to choose the following:
    1 - Delete a book entry
    2 - Delete all book entries
    3 - Return to main menu""")
        
        choice = input("Enter number: ")  
        try:
            choice = int(choice)                  
            if choice == 1:
                while True:
                    know_id = input("Do you know the ID number? (y/n): ").strip().lower()    
                    if know_id == 'y':
                        delete_by_id()
                        sub_choice = confirm_repeat('delete another book')
                        if sub_choice == 'stop':
                            return
  
                    elif know_id == 'n':                        
                        sub_choice1 = del_no_id_menu()
                        if sub_choice1 == 'back':
                            print('Returning to DELETE MENU')
                            continue
                        sub_choice2 = confirm_repeat('delete another book entry')
                        if sub_choice2 == 'stop':
                            print('Returning to MAIN MENU')
                            return
                        else:
                            print('Returning to DELETE MENU')
                            continue                
                    else:
                        print(invalid_yes_no)
 
            elif choice == 2:
                confirm = input("Are you sure you want to delete all book entries? (y/n): ").strip().lower()
                if confirm == 'y':
                    cur.execute('DELETE FROM books')
                    conn.commit()
                    print("All book entries successfully deleted. Returning to Main Menu.")
                    time.sleep(seconds_long)
                    return
                elif confirm == 'n':
                    print('Returning to DELETE MENU')
                    time.sleep(seconds_long)
                    continue                
            elif choice == 3:
                print("Returning to MAIN MENU")
                return
            else:
                print(invalid_yes_no)                       
        except ValueError:
            print(invalid_num_choice)
            
    
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
            print("-" * 50)
            delete_book()
            print("-" * 50)

        
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
            print(invalid_basic)
            
    conn.close()


#-----Run Program--------
if __name__ == "__main__":
    main_menu()

