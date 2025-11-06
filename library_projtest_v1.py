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

print('Table successfully added.')

print("\nHello, Welcome to LiShen's Library!") #HEADER

#Create loop that lets users choose the action

#cur.execute('DELETE FROM books')


#Intial welcome and main menu

print("""
\nSo...What would you like to do? Type the number for the following options.\n
1 - Adding a book.
2 - Printing the book list.
3 - Exiting the Library\n""")

choice = int(input("Enter number: "))

if choice == 1:
    
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
        print("\nBook already in shelves. Exiting...")
        
    
elif choice == 2:
    cur.execute("SELECT * FROM books")
    all_books = cur.fetchall()
    
    if all_books:
        print("\n\nHere are all the books...\n")
    
        for book in all_books:
            print(f"Book ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Publication Year: {book[3]}")
    else:
        print("\n\nShelves are empty! Add a book! Exiting now...")

elif choice == 3:
    print('\n\nExiting... Good bye!')
    conn.close()
    exit()
    

else:
    print("Invalid input. Try again..")



while True: #I want to have "to do next" in the succeeding loop unless after exit
    
    print("""
\n\nSo...What would you like to do next? Type the number for the following options.\n
    1 - Adding a book.
    2 - Printing the book list.
    3 - Exiting the Library\n""")
    
    choice = int(input("Enter number: "))
    
    if choice == 1:
        
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
            print("\nBook already in shelves. Exiting...")
            time.sleep(1.5)
            continue
        
    elif choice == 2:
        cur.execute("SELECT * FROM books")
        all_books = cur.fetchall()
        
        if all_books:
            print("\n\nHere are all the books...\n")
        
            for book in all_books:
                print(f"Book ID: {book[0]} | Title: {book[1]} | Author: {book[2]} | Publication Year: {book[3]}")
        else:
            print("\n\nShelves are empty! Add a book! Exiting now...")
            time.sleep(1.5)
    
    elif choice == 3:
        print('\n\nExiting the library... Good bye!')
        time.sleep(1.5)
        break
    
    else:
        print("Invalid input. Try again..")
    
    #print(choice)
    
conn.close()

