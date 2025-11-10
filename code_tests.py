

import time
import sqlite3

conn = sqlite3.connect('library.db')
cur = conn.cursor()

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
    
conn.close()
        