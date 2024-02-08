from tkinter import *
from tkinter import ttk
import pymysql
from tkinter import messagebox
import datetime
import tkinter as tk

root = Tk()
root.title("Library Management System")
root.geometry("1920x1080+0+0")



mypass = "Shrupass@123"
mydatabase="newdb"

con = pymysql.connect(host="localhost",user="root",password=mypass,database=mydatabase)
cur = con.cursor()


################################################### Adding book ##################################################################

def addBook():
    # new window for adding a book
    add_book_window = Toplevel(root)
    add_book_window.title("Add Book")
    add_book_window.geometry("1920x1080")
    add_book_window.configure(bg="lavender") 

    # place frames for book details
    frame_add_book = Frame(add_book_window, bd=10, relief="ridge", bg="lavender")
    frame_add_book.place(relx=0.5, rely=0.5, anchor="center")  # Adjusted placement and size

    frame_heading = Frame(frame_add_book, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)

    label_heading = Label(frame_heading, text="Add Book", bg="lavender", fg="hot pink", font=("Courier", 20, "bold"))
    label_heading.pack()

    frame_entries = Frame(frame_add_book, bd=10, relief="ridge", bg="lavender")
    frame_entries.pack(fill=BOTH, expand=True)  # Adjusted size

    # place labels and entry widgets for book details
    labels = ["ISBN :", "Title: ", "Author 1 :", "Author 2 :", "Author 3 :", "Edition :", "Volume :", "Publication :", "Number of Pages :", "Book Language :", "Book Subject :"]
    entries = [Entry(frame_entries, font=("Courier", 16)) for _ in range(len(labels))]

    for label, entry in zip(labels, entries):
        Label(frame_entries, text=label, font=("Courier", 14, "bold"), bg="lavender").grid(row=labels.index(label), column=0, sticky=W, padx=10)
        entry.grid(row=labels.index(label), column=1, padx=10, pady=5)

    # Function to insert book details into the database
    def insertBookDetails():
        try:
            book_details = [entry.get() for entry in entries]
            insert_query = "INSERT INTO book_master (isbn, bk_title, author1, author2, author3, edition, vol, publication, no_of_pg, bk_lang, bk_sub) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query, tuple(book_details))
            con.commit()
            messagebox.showinfo("Success", "Book added successfully.")
            add_book_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error in adding book details: {str(e)}")

    # 'Add Book' button
    add_button = Button(frame_add_book, text="Add Book", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=insertBookDetails)
    add_button.pack(pady=20)  
    
######################################## updating copies #########################################################

def updateBookCopies():
    # Define book_title_var globally or within the same scope where it's being accessed
    book_title_var = StringVar()
    
    def fillIsbn(event):
        # Fetch ISBN based on the selected book title
        selected_title = book_title_var.get()
        if selected_title:
            cur.execute("SELECT isbn FROM book_master WHERE bk_title = %s", (selected_title,))
            isbn = cur.fetchone()
            if isbn:
                isbn_var.set(isbn[0])


    # Create a new window for updating book copies
    update_copies_window = Toplevel(root)
    update_copies_window.title("Update Book Copies")
    update_copies_window.geometry("1920x1080")
    update_copies_window.configure(bg="lavender")

    # Create and place frames for updating book copies
    frame_update_copies = Frame(update_copies_window, bd=10, relief="ridge", bg="lavender")
    frame_update_copies.place(relx=0.5, rely=0.5, anchor="center")   # Adjusted placement and size

    frame_heading = Frame(frame_update_copies, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)

    label_heading = Label(frame_heading, text="Update Book Copies", bg="lavender", fg="hot pink", font=("Courier", 20, "bold"))
    label_heading.pack()

    frame_entries = Frame(frame_update_copies, bd=10, relief="ridge", bg="lavender")
    frame_entries.pack(fill=BOTH, expand=True)  # Adjusted size

    # Create and place labels and entry widgets for updating book copies
    update_labels = ["Title:", "ISBN:", "Number of Copies:", "Status:", "Date of Purchase:"]
    update_entries = [Entry(frame_entries, font=("Courier", 16)) for _ in range(len(update_labels))]

    for label, entry in zip(update_labels, update_entries):
        Label(frame_entries, text=label, font=("Courier", 14, "bold"), bg="lavender").grid(row=update_labels.index(label), column=0, sticky=W, padx=10)
        entry.grid(row=update_labels.index(label), column=1, padx=10, pady=5)

    # Add a dropdown for book titles
    book_titles_query = "SELECT bk_title FROM book_master"
    cur.execute(book_titles_query)
    book_titles = cur.fetchall()
    book_titles = [title[0] for title in book_titles]
    
    book_title_var = StringVar()
    book_title_dropdown = ttk.Combobox(frame_entries, textvariable=book_title_var, values=book_titles, font=("Courier", 16))
    book_title_dropdown.grid(row=update_labels.index("Title:"), column=1, padx=10, pady=5)
    book_title_dropdown.bind("<<ComboboxSelected>>", fillIsbn)

    def updateBookCopiesDetails():
        try:
            # Access values directly from update_entries using index
            title = update_entries[0].get()
            no_of_copies = update_entries[2].get()
            status = update_entries[3].get()
            purchase_dt = update_entries[4].get()
    
            status = status if status else "Available"  # Default to 'Available' if status is not provided
    
            # Retrieve ISBN based on the selected book title
            title = book_title_var.get()
            print(f"Title Before Query: {title}")
            isbn_query = f"SELECT isbn FROM book_master WHERE bk_title = '{title}'"
            print("ISBN Query:", isbn_query)
            cur.execute(isbn_query)
            isbn_result = cur.fetchone()
            
            print(f"ISBN Result: {isbn_result}")
            if isbn_result:
                isbn = isbn_result[0]
                print(f"ISBN: {isbn}")
            else:
                print("ISBN not found for the given book title.")
                
    
            if isbn_result:
                isbn = isbn_result[0]
    
                # Insert new book copies with auto-incremented accession numbers
                insert_details_query = "INSERT INTO book_details ( isbn, status, dept, purchase_dt) VALUES (%s, %s, %s, %s)"
    
                for _ in range(int(no_of_copies)):
                    cur.execute(insert_details_query, (isbn, status, 'Library', purchase_dt))
    
                con.commit()
                messagebox.showinfo("Success", "Book copies updated successfully.")
                update_copies_window.destroy()
            else:
                messagebox.showerror("Error", "ISBN not found for the given book title.")
        except Exception as e:
            messagebox.showerror("Error", f"Error in updating book copies: {str(e)}")


    # Create and place the 'Update Book Copies' button
    update_button = Button(frame_update_copies, text="Update Book Copies", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=updateBookCopiesDetails)
    update_button.pack(pady=20)

    # Variables to store ISBN and populate it based on selected title
    isbn_var = StringVar()
    isbn_entry = Entry(frame_entries, textvariable=isbn_var, font=("Courier", 16), state="readonly")
    isbn_entry.grid(row=update_labels.index("ISBN:"), column=1, padx=10, pady=5)
    
    update_copies_window.mainloop()

############################################### Delete Book ###############################################################   

def delete():
 def delete_book(acc_no):
    try:
            # SQL statement to delete a book by ID
            sql = f"DELETE FROM book_details WHERE acc_no = {acc_no}"

            # Execute the SQL statement
            cur.execute(sql)

            # Commit the changes
            con.commit()

            print(f"Book with acc_no {acc_no} deleted successfully.")
    except Exception as e:
        # Handle exceptions, e.g., database errors
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Error in deleting book: {str(e)}")
        con.rollback()
    finally:
        # Close the database connection
        con.close()

 def delete_book_gui():
    # Function to handle the delete button click event
    def delete_button_clicked():
        acc_no = entry_acc_no.get()
        if acc_no.isdigit():
            delete_book(int(acc_no))
            messagebox.showinfo("Success", f"Book with acc_no {acc_no} deleted successfully.")
            
        else:
            messagebox.showerror("Error", "Invalid Acc_No. Please enter a valid numeric ID.")

    # Create the main window
    window = tk.Tk()
    window.title("Book Deletion Tool")
    window.geometry("1920x1080")

    frame = tk.Frame(window, bd=12, relief="ridge", padx=20, bg="lavender")
    frame.place(relx=0.5, rely=0.5, anchor="center")
 
    

    label_acc_no = tk.Label(frame, text="Enter Accession No:", font=("Courier", 14, "bold"), bg="lavender")
    entry_acc_no = tk.Entry(frame, font=("Courier", 14))


    delete_button = tk.Button(frame, text="Delete Book", font=("Courier", 12, "bold"), command=delete_button_clicked, bg='hot pink', fg='white')
    
    label_acc_no.grid(row=0, column=0, padx=10, pady=10)
    entry_acc_no.grid(row=0, column=1, padx=10, pady=10)
    delete_button.grid(row=0, column=2, padx=10, pady=10)

    
    
    # Start the Tkinter event loop
    window.mainloop()

# Example: Launch the GUI
 delete_book_gui()
    

################################################ view book list ##############################################################     

def viewBookList():
    def fillBookTable():
        # Fetch all books from book_master
        cur.execute("""
            SELECT bm.isbn, bm.bk_title, bm.author1, bm.author2, bm.edition, bm.vol, bm.publication, bm.no_of_pg, bm.bk_lang, bm.bk_sub,
            COUNT(bd.isbn) AS copies
            FROM book_master bm
            LEFT JOIN book_details bd ON bm.isbn = bd.isbn
            GROUP BY bm.isbn
        """)
        book_data = cur.fetchall()

        # Clear existing items in the treeview
        for item in book_tree.get_children():
            book_tree.delete(item)

        # Insert new data into the treeview
        for book in book_data:
            book_tree.insert("", "end", values=book)

    # Create a new window for viewing book list
    view_book_list_window = Toplevel(root)
    view_book_list_window.title("View Book List")
    view_book_list_window.geometry("1920x1080")
    view_book_list_window.configure(bg="lavender")

    # Create and place frames for viewing book list
    frame_view_books = Frame(view_book_list_window, bd=10, relief="ridge", bg="lavender")
    frame_view_books.place(relx=0.5, rely=0.5, anchor="center")

    frame_heading = Frame(frame_view_books, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)

    label_heading = Label(frame_heading, text="List of Books", bg="lavender", fg="hot pink", font=("Courier", 25, "bold"))
    label_heading.pack()

    frame_treeview = Frame(frame_view_books, bd=10, relief="ridge", bg="lavender")
    frame_treeview.pack(fill=BOTH, expand=True)

    # Create a treeview to display book information
    columns = ["ISBN", "Title", "Author 1", "Author 2", "Edition", "Volume", "Publication", "Pages", "Language", "Subject", "Copies"]
    book_tree = ttk.Treeview(frame_treeview, columns=columns, show="headings", selectmode="browse", height=30)

    # Configure column headings
    for col in columns:
        book_tree.heading(col, text=col, anchor=CENTER)
        book_tree.column(col, width=100, anchor=CENTER)

    book_tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(frame_treeview, orient=VERTICAL, command=book_tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    book_tree.configure(yscrollcommand=scrollbar.set)

    # Fill the treeview with book data
    fillBookTable()

    view_book_list_window.mainloop()

################################################ issue book  ##############################################################     

def get_book_titles():
    # Fetch all book titles from book_master
    cur.execute("SELECT bk_title FROM book_master")
    titles = cur.fetchall()
    return [title[0] for title in titles]

def issueBook():
    def search_book():
     try:
        # Clear previous search results
        for i in tree.get_children():
            tree.delete(i)

        # Get the selected book title from the Combobox
        selected_title_index = entry_title.current()

        # Ensure a valid title is selected
        if selected_title_index == -1:
            messagebox.showinfo("Information", "Please select a book title.")
            return

        selected_title = entry_title.get()

        # Search for the book title in the database (case-insensitive)
        query = """
            SELECT bd.acc_no, bd.isbn, bm.bk_title, bm.author1, bd.status
            FROM book_details bd
            JOIN book_master bm ON bd.isbn = bm.isbn
            WHERE LOWER(bm.bk_title) = %s AND bd.status = 'Available';
        """
        print("Search Query:", query)
        print("Search Title:", selected_title)
        cur.execute(query, (selected_title.lower(),))

        # Display search results in the Tkinter Treeview
        for row in cur.fetchall():
            tree.insert("", "end", values=row)
     except Exception as e:
        messagebox.showerror("Error", f"Error in searching books: {str(e)}")




    def issue_book():
        accession_no = entry_acc_no.get()
        prn = entry_prn.get()
        issue_date = datetime.date.today()
        fine = 0

        # Check if the book is available
        cur.execute("SELECT status FROM book_details WHERE acc_no = %s", (accession_no,))
        status = cur.fetchone()

        if status and status[0] == "Available":
            # Update the book status to "Issued"
            #cur.execute("UPDATE book_details SET status = 'Issued' WHERE acc_no = %s", (accession_no,))
            #con.commit()

            # Insert the issue record into the 'issues' table
            cur.execute("INSERT INTO issues (prn, acc_no, issue_dt, fine) VALUES (%s, %s, %s, %s)",
                        (prn, accession_no, issue_date, fine))
            con.commit()

            messagebox.showinfo("Success", "Book issued to student successfully.")

        else:
            messagebox.showerror("Error", "The book is not available for issuing.")

    # Create a new window for issuing books
    root = tk.Tk()
    root.title("Issue Book")
    root.geometry("1920x1080")
    root.configure(bg="lavender")
    
    
    # Create and place a frame for the content
    frame = tk.Frame(root, bd=12, relief="ridge", padx=20, bg="lavender")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label_title = tk.Label(frame, text="Enter Book Title:", font=("Courier", 14, "bold"), bg="lavender")
    title_var = tk.StringVar()
    entry_title = ttk.Combobox(frame, font=("Courier", 14))
    entry_title['values'] = get_book_titles()
    entry_title.set("Select Book Title")
    entry_title['textvariable'] = title_var
    entry_title.bind("<<ComboboxSelected>>", lambda event: print("Current title_var value:", title_var.get()))

      # Call function to get book titles
    

    button_search = tk.Button(frame, text="Search", font=("Courier", 12, "bold"), command=search_book, bg='hot pink', fg='white')

    label_acc_no = tk.Label(frame, text="Enter Accession No:", font=("Courier", 14, "bold"), bg="lavender")
    entry_acc_no = tk.Entry(frame, font=("Courier", 14))

    label_prn = tk.Label(frame, text="Enter PRN:", font=("Courier", 14, "bold"), bg="lavender")
    entry_prn = tk.Entry(frame, font=("Courier", 14))

    button_issue = tk.Button(frame, text="Issue Book", font=("Courier", 12, "bold"), command=issue_book, bg='hot pink', fg='white')

    columns = ('Acc No', 'ISBN', 'Title', 'Author', 'Status')
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)

    # Layout
    label_title.grid(row=0, column=0, padx=10, pady=10)
    entry_title.grid(row=0, column=1, padx=10, pady=10)
    button_search.grid(row=0, column=2, padx=10, pady=10)
    tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

    label_acc_no.grid(row=2, column=0, padx=10, pady=10)
    entry_acc_no.grid(row=2, column=1, padx=10, pady=10)

    label_prn.grid(row=3, column=0, padx=10, pady=10)
    entry_prn.grid(row=3, column=1, padx=10, pady=10)

    button_issue.grid(row=4, column=0, columnspan=3, pady=10)

    root.mainloop()

    

################################################ return book ##############################################################     

def returnBook():
    def return_book():
        acc_no = entry_acc_no.get()
        prn = entry_prn.get()
        return_date = entry_return_date.get()
    
        try:
            # Parse return date
            return_date = datetime.datetime.strptime(return_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
    
        # Check if the book is issued
        cur.execute("SELECT issue_dt, due_dt FROM issues WHERE acc_no = %s AND prn = %s AND return_dt IS NULL", (acc_no, prn))
        issue_info = cur.fetchone()
    
        if issue_info:
            issue_dt, due_dt = issue_info
            
            cur.execute("UPDATE book_details SET status = 'Available' WHERE acc_no = %s", (acc_no,))
            con.commit()
    
            # Update the return date and calculate fine
            cur.execute("UPDATE issues SET return_dt = %s, fine = CASE WHEN %s > due_dt THEN DATEDIFF(%s, due_dt) ELSE 0 END WHERE acc_no = %s AND prn = %s AND return_dt IS NULL",
                        (return_date, return_date, return_date, acc_no, prn))
            con.commit()
    
            messagebox.showinfo("Success", "Book returned successfully.")
    
        else:
            messagebox.showerror("Error", "No active issue record found for the provided accession number and PRN.")

    root_return = Tk()
    root_return.title("Return Book")
    root_return.geometry("1920x1080")

    frame_return = Frame(root_return, bd=10, relief="ridge", bg="lavender")
    frame_return.place(relx=0.5, rely=0.5, anchor="center")

    label_acc_no = Label(frame_return, text="Accession No:", font=("Courier", 14, "bold"), bg="lavender")
    entry_acc_no = Entry(frame_return, font=("Courier", 14))

    label_prn = Label(frame_return, text="PRN:", font=("Courier", 14, "bold"), bg="lavender")
    entry_prn = Entry(frame_return, font=("Courier", 14))

    label_return_date = Label(frame_return, text="Return Date (YYYY-MM-DD):", font=("Courier", 14, "bold"), bg="lavender")
    entry_return_date = Entry(frame_return, font=("Courier", 14))

    button_return = Button(frame_return, text="Return", font=("Courier", 12, "bold"), command=return_book, bg='hot pink', fg='white')

    label_acc_no.grid(row=0, column=0, padx=10, pady=10)
    entry_acc_no.grid(row=0, column=1, padx=10, pady=10)

    label_prn.grid(row=1, column=0, padx=10, pady=10)
    entry_prn.grid(row=1, column=1, padx=10, pady=10)

    label_return_date.grid(row=2, column=0, padx=10, pady=10)
    entry_return_date.grid(row=2, column=1, padx=10, pady=10)

    button_return.grid(row=3, column=0, columnspan=2, pady=10)

    root_return.mainloop()




##########################################################################################################################

################################################# book transactions #####################################################


def open_book_transactions():
    def get_book_transactions():
        try:
            # Fetch book transactions data from the 'issues' table
            cur.execute("""
                SELECT i.PRN, s.Name, s.dept, s.PH_NO, i.acc_no, bm.bk_title, i.issue_dt, i.due_dt, i.return_dt, i.fine
                FROM issues i
                JOIN student s ON i.prn = s.prn
                JOIN book_details bd ON i.acc_no = bd.acc_no
                JOIN book_master bm ON bd.isbn = bm.isbn
            """)
            transactions_data = cur.fetchall()
            return transactions_data
        except Exception as e:
            messagebox.showerror("Error", f"Error in fetching book transactions: {str(e)}")
            return []

    def update_transactions():
        # Clear previous data in the Treeview
        for i in tree.get_children():
            tree.delete(i)

        # Fetch and populate book transactions data
        transactions_data = get_book_transactions()
        for row in transactions_data:
            status = "Returned" if row[8] else "Not Returned"
            tree.insert("", "end", values=(*row[:8], status, row[9]))

    # Create a new window for book transactions
    transactions_window = Toplevel(root)
    transactions_window.title("Book Transactions")
    transactions_window.geometry("1920x1080")
    transactions_window.configure(bg="lavender")

    # Create and place frames for viewing book transactions
    frame_transactions = Frame(transactions_window, bd=10, relief="ridge", bg="lavender")
    frame_transactions.place(relx=0.5, rely=0.5, anchor="center")

    frame_heading = Frame(frame_transactions, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)

    label_heading = Label(frame_heading, text="Book Transactions", bg="lavender", fg="hot pink", font=("Courier", 25, "bold"))
    label_heading.pack()

    frame_treeview = Frame(frame_transactions, bd=10, relief="ridge", bg="lavender")
    frame_treeview.pack(fill=BOTH, expand=True)

    # Create a treeview to display book transactions information
    columns = ["PRN", "Student Name", "Department", "Phone No", "Acc No", "Book Title", "Issue Date", "Due Date", "Status", "Fine"]
    tree = ttk.Treeview(frame_treeview, columns=columns, show="headings", selectmode="browse", height=30)

    # Configure column headings
    for col in columns:
        tree.heading(col, text=col, anchor=CENTER)
        tree.column(col, width=100, anchor=CENTER)

    tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(frame_treeview, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    # Fill the treeview with book transactions data
    update_transactions()

    # Create a button to refresh the data
    btn_refresh = tk.Button(frame_treeview, text="Refresh", font=("Courier", 12, "bold"), command=update_transactions, bg='hot pink', fg='white')
    btn_refresh.pack(side=tk.BOTTOM, pady=10)

    transactions_window.mainloop()


#################################################### Add student ##########################################################

def addStudent():
# Create a new window for adding a student
    add_student_window = Toplevel(root)
    add_student_window.title("Add Student")
    add_student_window.geometry("1920x1080")
    add_student_window.configure(bg="lavender")
    
    # Create and place frames for student details
    frame_add_student = Frame(add_student_window, bd=10, relief="ridge", bg="lavender")
    frame_add_student.place(relx=0.2, rely=0.5, anchor="center")  # Adjusted placement and size
    
    frame_heading = Frame(frame_add_student, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)
    
    label_heading = Label(frame_heading, text="Add Student", bg="lavender", fg="hot pink", font=("Courier", 20, "bold"))
    label_heading.pack()
    
    frame_entries = Frame(frame_add_student, bd=10, relief="ridge", bg="lavender")
    frame_entries.pack(fill=BOTH, expand=True)  # Adjusted size
    
    # Create and place labels and entry widgets for student details
    labels = ["PRN:", "Name:", "Department:", "Phone No:", "Email:"]
    entries = [Entry(frame_entries, font=("Courier", 16)) for _ in range(len(labels))]
    
    for label, entry in zip(labels, entries):
        Label(frame_entries, text=label, font=("Courier", 14, "bold"), bg="lavender").grid(row=labels.index(label), column=0, sticky=W, padx=10)
        entry.grid(row=labels.index(label), column=1, padx=10, pady=5)
    
    # Function to insert student details into the database
    def insertStudentDetails():
        try:
            student_details = [entry.get() for entry in entries]
            insert_query = "INSERT INTO student (PRN, Name, Dept, PH_NO, email) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(insert_query, tuple(student_details))
            con.commit()
            messagebox.showinfo("Success", "Student added successfully.")
            add_student_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error in adding student details: {str(e)}")
    
    # Create and place the 'Add Student' button
    add_button = Button(frame_add_student, text="Add Student", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=insertStudentDetails)
    add_button.pack(pady=20)
    
    # Create a frame for displaying the list of students
    frame_students_list = Frame(add_student_window, bd=10, relief="ridge", bg="lavender")
    frame_students_list.place(relx=0.7, rely=0.5, anchor="center")
    
    # Create a function to refresh the student list
    def refreshStudentList():
        # Fetch all students from the student table
        cur.execute("SELECT PRN, Name, Dept, PH_NO, email FROM student")
        student_data = cur.fetchall()
    
        # Clear existing items in the treeview
        for item in students_tree.get_children():
            students_tree.delete(item)
    
        # Insert new data into the treeview
        for student in student_data:
            students_tree.insert("", "end", values=student)
    
    # Create a Treeview to display the list of students
    columns = ["PRN", "Name", "Department", "Phone No", "Email"]
    students_tree = ttk.Treeview(frame_students_list, columns=columns, show="headings", selectmode="browse", height=30)
    
    # Configure column headings
    for col in columns:
        students_tree.heading(col, text=col, anchor=CENTER)
        students_tree.column(col, width=100, anchor=CENTER)
    
    students_tree.pack(side=LEFT, fill=BOTH, expand=True)
    
    # Add a vertical scrollbar
    scrollbar = ttk.Scrollbar(frame_students_list, orient=VERTICAL, command=students_tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    students_tree.configure(yscrollcommand=scrollbar.set)
    
    # Create a 'Refresh' button
    btn_refresh = Button(frame_students_list, text="Refresh", font=("Courier", 12, "bold"), command=refreshStudentList, bg='hot pink', fg='white')
    btn_refresh.pack(side=BOTTOM, pady=10)
    
    # Initial load of student list
    refreshStudentList()
    
##########################################################################################################################

################################################# add purchase details ####################################################

def addPurchase():
    def insertPurchaseDetails():
        try:
            # Get values from the entry widgets
            invoice_no = entry_invoice.get()
            publisher_id = pub_id_var.get()
            isbn = entry_isbn.get()
            quantity = entry_quantity.get()
            purchase_date = entry_purchase_date.get()
            price = entry_price.get()

            # Insert into the purchase table
            insert_query = "INSERT INTO purchase (invoice_no, pub_id, isbn, quantity, purchase_dt, price) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(insert_query, (invoice_no, publisher_id, isbn, quantity, purchase_date, price))
            con.commit()

            messagebox.showinfo("Success", "Purchase details added successfully.")
            add_purchase_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error in adding purchase details: {str(e)}")

    add_purchase_window = Toplevel(root)
    add_purchase_window.title("Add Purchase")
    add_purchase_window.geometry("1920x1080")
    add_purchase_window.configure(bg="lavender")

    frame_add_purchase = Frame(add_purchase_window, bd=10, relief="ridge", bg="lavender")
    frame_add_purchase.place(relx=0.5, rely=0.5, anchor="center")

    frame_heading = Frame(frame_add_purchase, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)

    label_heading = Label(frame_heading, text="Add Purchase", bg="lavender", fg="hot pink", font=("Courier", 20, "bold"))
    label_heading.pack()

    frame_entries = Frame(frame_add_purchase, bd=10, relief="ridge", bg="lavender")
    frame_entries.pack(fill=BOTH, expand=True)

    labels = ["Invoice No:", "Publisher ID:", "ISBN:", "Quantity:", "Purchase Date:", "Price:"]
    
    for label in labels:
        Label(frame_entries, text=label, font=("Courier", 14, "bold"), bg="lavender").grid(row=labels.index(label), column=0, sticky=W, padx=10)

    entry_invoice = Entry(frame_entries, font=("Courier", 16))
    entry_invoice.grid(row=labels.index("Invoice No:"), column=1, padx=10, pady=5)

    pub_id_var = StringVar()
    pub_id_dropdown = ttk.Combobox(frame_entries, textvariable=pub_id_var, state="readonly")
    pub_id_dropdown.grid(row=labels.index("Publisher ID:"), column=1, padx=10, pady=5)

    entry_isbn = Entry(frame_entries, font=("Courier", 16))
    entry_isbn.grid(row=labels.index("ISBN:"), column=1, padx=10, pady=5)

    entry_quantity = Entry(frame_entries, font=("Courier", 16))
    entry_quantity.grid(row=labels.index("Quantity:"), column=1, padx=10, pady=5)

    entry_purchase_date = Entry(frame_entries, font=("Courier", 16))
    entry_purchase_date.grid(row=labels.index("Purchase Date:"), column=1, padx=10, pady=5)

    entry_price = Entry(frame_entries, font=("Courier", 16))
    entry_price.grid(row=labels.index("Price:"), column=1, padx=10, pady=5)

    # Function to clear the entry widgets
    def clearEntries():
        entry_invoice.delete(0, END)
        pub_id_dropdown.set("")
        entry_isbn.delete(0, END)
        entry_quantity.delete(0, END)
        entry_purchase_date.delete(0, END)
        entry_price.delete(0, END)

    # Create and place the 'Add' button
    add_button = Button(frame_add_purchase, text="Add", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=insertPurchaseDetails)
    add_button.pack(pady=20)

    # Create a 'Clear' button
    clear_button = Button(frame_add_purchase, text="Clear", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=clearEntries)
    clear_button.pack(pady=10)

    # Populate the dropdown with pub_names and corresponding pub_ids
    pub_id_query = "SELECT pub_id, pub_name FROM publication"
    cur.execute(pub_id_query)
    pub_id_options = cur.fetchall()
    
    pub_names = [pub[1] for pub in pub_id_options]
    pub_ids = [pub[0] for pub in pub_id_options]
    
    pub_id_dropdown['values'] = pub_names
    
    # Function to update pub_id when a pub_name is selected
    def updatePubId(*args):
        selected_pub_name = pub_id_var.get()
        if selected_pub_name in pub_names:
            selected_index = pub_names.index(selected_pub_name)
            pub_id_var.set(pub_ids[selected_index])
    
    # Link the updatePubId function to the dropdown
    pub_id_var.trace_add('write', updatePubId)
    
########################################################### add publication ##########################################


def addPublication():
    def insertPublicationDetails():
        try:
            # Get values from the entry widgets
            pub_id = entry_pub_id.get()
            pub_name = entry_pub_name.get()
            phone_number = entry_phone_number.get()
            address = entry_address.get()
            email = entry_email.get()

            # Insert into the publication table
            insert_query = "INSERT INTO publication (pub_id, pub_name, ph_no, addr, email) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(insert_query, (pub_id, pub_name, phone_number, address, email))
            con.commit()

            messagebox.showinfo("Success", "Publication details added successfully.")
            add_publication_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error in adding publication details: {str(e)}")

    add_publication_window = Toplevel(root)
    add_publication_window.title("Add Publication")
    add_publication_window.geometry("1920x1080")
    add_publication_window.configure(bg="lavender")

    frame_add_publication = Frame(add_publication_window, bd=10, relief="ridge", bg="lavender")
    frame_add_publication.place(relx=0.5, rely=0.5, anchor="center")

    frame_heading = Frame(frame_add_publication, bd=5, relief="ridge", bg="lavender")
    frame_heading.pack(side=TOP, fill=X)

    label_heading = Label(frame_heading, text="Add Publication", bg="lavender", fg="hot pink", font=("Courier", 20, "bold"))
    label_heading.pack()

    frame_entries = Frame(frame_add_publication, bd=10, relief="ridge", bg="lavender")
    frame_entries.pack(fill=BOTH, expand=True)

    labels = ["Publisher ID:", "Publisher Name:", "Phone Number:", "Address:", "Email:"]
    
    for label in labels:
        Label(frame_entries, text=label, font=("Courier", 14, "bold"), bg="lavender").grid(row=labels.index(label), column=0, sticky=W, padx=10)

    entry_pub_id = Entry(frame_entries, font=("Courier", 16))
    entry_pub_id.grid(row=labels.index("Publisher ID:"), column=1, padx=10, pady=5)

    entry_pub_name = Entry(frame_entries, font=("Courier", 16))
    entry_pub_name.grid(row=labels.index("Publisher Name:"), column=1, padx=10, pady=5)

    entry_phone_number = Entry(frame_entries, font=("Courier", 16))
    entry_phone_number.grid(row=labels.index("Phone Number:"), column=1, padx=10, pady=5)

    entry_address = Entry(frame_entries, font=("Courier", 16))
    entry_address.grid(row=labels.index("Address:"), column=1, padx=10, pady=5)

    entry_email = Entry(frame_entries, font=("Courier", 16))
    entry_email.grid(row=labels.index("Email:"), column=1, padx=10, pady=5)

    # Function to clear the entry widgets
    def clearEntries():
        entry_pub_id.delete(0, END)
        entry_pub_name.delete(0, END)
        entry_phone_number.delete(0, END)
        entry_address.delete(0, END)
        entry_email.delete(0, END)

    # Create and place the 'Add' button
    add_button = Button(frame_add_publication, text="Add", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=insertPublicationDetails)
    add_button.pack(pady=20)

    # Create a 'Clear' button
    clear_button = Button(frame_add_publication, text="Clear", bg='hot pink', fg='white', font=("Courier", 12, "bold"), command=clearEntries)
    clear_button.pack(pady=10)


########################################################################################################################


## 1st frame ##
lbltitle = Label(root, text="LIBRARY MANAGEMENT SYSTEM", bg="Lavender", fg="hot pink", bd=20, relief="ridge",
                 font=("times new roman", 35, "bold"), padx=2, pady=6)
lbltitle.pack(side=TOP, fill=X)

frame = Frame(root, bd=12, relief="ridge", padx=20, bg="lavender")
frame.place(x=0, y=100, width=1535, height=780)

# LabelFrame for book-related buttons
DataFrameLeft = LabelFrame(frame, text="BOOKS", bg="Lavender", fg="hot pink", bd=20, relief="ridge",
                                   font=("times new roman", 20, "bold"))
DataFrameLeft.place(x=0, y=5, width=450, height=700)

btn1 = Button(DataFrameLeft, text="Add Book Details", bg='hot pink', fg='white', command=addBook)
btn1.place(relx=0.2, rely=0.10, relwidth=0.45, relheight=0.1)

btn6 = Button(DataFrameLeft, text="Update Book Copies", bg='hot pink', fg='white', command=updateBookCopies)
btn6.place(relx=0.2, rely=0.25, relwidth=0.45, relheight=0.1)

btn2 = Button(DataFrameLeft, text="Delete Book", bg='hot pink', fg='white', command= delete)
btn2.place(relx=0.2, rely=0.40, relwidth=0.45, relheight=0.1)

btn3 = Button(DataFrameLeft, text="View Book List", bg='hot pink', fg='white', command=viewBookList)
btn3.place(relx=0.2, rely=0.55, relwidth=0.45, relheight=0.1)

btn4 = Button(DataFrameLeft, text="Issue Book to Student", bg='hot pink', fg='white', command = issueBook)
btn4.place(relx=0.2, rely=0.70, relwidth=0.45, relheight=0.1)

btn5 = Button(DataFrameLeft, text="Return Book", bg='hot pink', fg='white', command= returnBook)
btn5.place(relx=0.2, rely=0.85, relwidth=0.45, relheight=0.1)

# 2nd frame - Student Info
DataFrameStudent = LabelFrame(frame, text="STUDENT INFO", bg="Lavender", fg="hot pink", bd=20, relief="ridge",
                              font=("times new roman", 20, "bold"))
DataFrameStudent.place(x=1020, y=5, width=450, height=300)

btnBookTranactions = Button(DataFrameStudent, text="Book Transactions", bg='hot pink', fg='white', command= open_book_transactions)
btnBookTranactions.place(relx=0.2, rely=0.10, relwidth=0.6, relheight=0.2)

btnAddStudent = Button(DataFrameStudent, text="Add Student", bg='hot pink', fg='white', command= addStudent)
btnAddStudent.place(relx=0.2, rely=0.60, relwidth=0.6, relheight=0.2)

# 3rd frame - Purchase
DataFramePurchase = LabelFrame(frame, text="PURCHASE", bg="Lavender", fg="hot pink", bd=20, relief="ridge",
                               font=("times new roman", 20, "bold"))
DataFramePurchase.place(x=1020, y=315, width=450, height=380)

btnPurchase = Button(DataFramePurchase, text="Add Purchase", bg='hot pink', fg='white', command= addPurchase)
btnPurchase.place(relx=0.2, rely=0.10, relwidth=0.6, relheight=0.2)

btnAddPublication = Button(DataFramePurchase, text="Add Publication", bg='hot pink', fg='white', command= addPublication)
btnAddPublication.place(relx=0.2, rely=0.60, relwidth=0.6, relheight=0.2)


root.mainloop()


