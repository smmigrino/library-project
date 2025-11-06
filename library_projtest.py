import sqlite3

conn = sqlite3.connect('library.db')
print('Connected. No error here.')

cur = conn.cursor()

cur.execute(
            
"""CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, year INTEGER)"""            

)

print("Table created Successfully.")

cur.execute("DELETE FROM books;")
#to restart the table


title = input("Enter book title: ")
author = input("Enter author name: ")
year = int(input("Enter publication year: "))

cur.execute("SELECT COUNT(*) FROM books WHERE title = ? AND author = ?", (title, author))
count =  cur.fetchone()[0]

if count == 0:
    cur.execute("""
    INSERT INTO books (title, author, year) VALUES (?, ?, ?)""" , (title, author, year)                
    )
    print("Book Added.")

else:
    print("Book already exists. Skipping insert.")

conn.commit()

#cur.execute(
    
#    "INSERT INTO books (id, title, author, year) VALUES (?, ?, ?, ?)", (1, "Blue Soul", "Xue Min", 2002))


#print("Book added Successfully.")


cur.execute(
    "SELECT * FROM books"
)

rows = cur.fetchall()

print(rows)



conn.commit()
conn.close()

