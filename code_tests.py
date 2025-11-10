

import time
import sqlite3

conn = sqlite3.connect('library.db')
cur = conn.cursor()

while True:
    print("(Enter 'EXIT' to go back to Main Menu.)")
    to_search = input("Enter Title/Author/Publication Year: ")
    
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
conn.close()
        