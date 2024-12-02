from tkinter import *
from tkinter import messagebox

# Function to handle form submission
def submit_review():
    # Collect data from entry fields
    rating_id = entry_rating_id.get()
    apartment_id = entry_apartment_id.get()
    user_id = entry_user_id.get()
    rent = entry_rent.get()
    location = entry_location.get()
    bedrooms = entry_bedrooms.get()
    bathrooms = entry_bathrooms.get()
    year_of_review = entry_year_of_review.get()
    
    # Validation: Ensure all fields are filled
    if not all([rating_id, apartment_id, user_id, rent, location, bedrooms, bathrooms, year_of_review]):
        messagebox.showwarning("Incomplete Data", "Please fill in all fields!")
        return
    
    # Simulate storing data (you could connect to a database here)
    print(f"Rating ID: {rating_id}")
    print(f"Apartment ID: {apartment_id}")
    print(f"User ID: {user_id}")
    print(f"Rent: {rent}")
    print(f"Location: {location}")
    print(f"Bedrooms: {bedrooms}")
    print(f"Bathrooms: {bathrooms}")
    print(f"Year of Review: {year_of_review}")
    messagebox.showinfo("Success", "Review submitted successfully!")

# Initialize main window
root = Tk()
root.title("Apartment Review Submission")

# Create labels and entry fields
Label(root, text="Rating ID:").grid(row=0, column=0, padx=10, pady=5)
entry_rating_id = Entry(root)
entry_rating_id.grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Apartment ID:").grid(row=1, column=0, padx=10, pady=5)
entry_apartment_id = Entry(root)
entry_apartment_id.grid(row=1, column=1, padx=10, pady=5)

Label(root, text="User ID:").grid(row=2, column=0, padx=10, pady=5)
entry_user_id = Entry(root)
entry_user_id.grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Rent:").grid(row=3, column=0, padx=10, pady=5)
entry_rent = Entry(root)
entry_rent.grid(row=3, column=1, padx=10, pady=5)

Label(root, text="Location:").grid(row=4, column=0, padx=10, pady=5)
entry_location = Entry(root)
entry_location.grid(row=4, column=1, padx=10, pady=5)

Label(root, text="Bedrooms:").grid(row=5, column=0, padx=10, pady=5)
entry_bedrooms = Entry(root)
entry_bedrooms.grid(row=5, column=1, padx=10, pady=5)

Label(root, text="Bathrooms:").grid(row=6, column=0, padx=10, pady=5)
entry_bathrooms = Entry(root)
entry_bathrooms.grid(row=6, column=1, padx=10, pady=5)

Label(root, text="Year of Review:").grid(row=7, column=0, padx=10, pady=5)
entry_year_of_review = Entry(root)
entry_year_of_review.grid(row=7, column=1, padx=10, pady=5)

# Add a submit button
Button(root, text="Submit Review", command=submit_review).grid(row=8, column=0, columnspan=2, pady=10)

# Run the main loop
root.mainloop()

