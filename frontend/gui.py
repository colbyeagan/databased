from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import * 

# Initialize database
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

# Function to fetch apartment IDs dynamically
def get_apartment_list():
    apartments = session.query(Apartments).all()
    return [f"{apartment.apartment_id} - {apartment.location}" for apartment in apartments]

# Function to handle form submission
def submit_review():
    # Collect data from entry fields
    try:
        apartment_id = combo_apartment_id.get().split(" - ")[0]
        user_id = int(entry_user_id.get())
        rent = float(entry_rent.get())
        bedrooms = int(entry_bedrooms.get())
        bathrooms = int(entry_bathrooms.get())
        year_of_review = int(entry_year_of_review.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values for User ID, Rent, Bedrooms, Bathrooms, and Year of Review.")
        return

    # Validation: Ensure all fields are filled
    if not all([apartment_id, user_id, rent, bedrooms, bathrooms, year_of_review]):
        messagebox.showwarning("Incomplete Data", "Please fill in all fields!")
        return

    # Try to add the review to the database
    try:
        add_apartment_rating(session, 
            apartment_id=int(apartment_id),                  
            comments="",  # You can extend the GUI to take comments
            user_pid=user_id, 
            rent=rent, 
            bedrooms=bedrooms, 
            bathrooms=bathrooms, 
            year_of_review=year_of_review)
        messagebox.showinfo("Success", "Review submitted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to submit review: {e}")

# Initialize main window
root = Tk()
root.title("Apartment Review Submission")

# Create labels and entry fields
Label(root, text="Apartment ID:").grid(row=0, column=0, padx=10, pady=5)

# Dropdown menu for Apartment IDs
apartment_list = get_apartment_list()
combo_apartment_id = ttk.Combobox(root, values=apartment_list, state="readonly")
combo_apartment_id.set("Select")  # Default value
combo_apartment_id.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="User ID:").grid(row=1, column=0, padx=10, pady=5)
entry_user_id = Entry(root)
entry_user_id.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Rent:").grid(row=2, column=0, padx=10, pady=5)
entry_rent = Entry(root)
entry_rent.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Bedrooms:").grid(row=3, column=0, padx=10, pady=5)
entry_bedrooms = Entry(root)
entry_bedrooms.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Bathrooms:").grid(row=4, column=0, padx=10, pady=5)
entry_bathrooms = Entry(root)
entry_bathrooms.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Year of Review:").grid(row=5, column=0, padx=10, pady=5)
entry_year_of_review = Entry(root)
entry_year_of_review.grid(row=5, column=1, padx=10, pady=5)

# Add a submit button
Button(root, text="Submit Review", command=submit_review).grid(row=6, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()
