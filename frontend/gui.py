from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import *  # Import your database logic here
from tkinter import Text


# Initialize database
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

# Main Application Class
class ApartmentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System")

        # Navigation Buttons
        self.nav_frame = Frame(self.root)
        self.nav_frame.grid(row=0, column=0, columnspan=2, pady=10)

        Button(self.nav_frame, text="Add Record", command=lambda: self.show_page("AddRecordPage")).grid(row=0, column=0, padx=10)
        Button(self.nav_frame, text="Delete Record", command=lambda: self.show_page("DeleteRecordPage")).grid(row=0, column=1, padx=10)
        Button(self.nav_frame, text="Update Rent", command=lambda: self.show_page("UpdateRentPage")).grid(row=0, column=2, padx=10)
        Button(self.nav_frame, text="Update Comment", command=lambda: self.show_page("UpdateCommentPage")).grid(row=0, column=3, padx=10)
        Button(self.nav_frame, text="Show All Data", command=lambda: self.show_page("ShowAllDataPage")).grid(row=0, column=4, padx=10)

        # Page Frames
        self.pages = {
            "AddRecordPage": AddRecordPage(self.root),
            "DeleteRecordPage": DeleteRecordPage(self.root),
            "UpdateRentPage": UpdateRentPage(self.root),
            "UpdateCommentPage": UpdateCommentPage(self.root),
            "ShowAllDataPage": ShowAllDataPage(self.root),
        }

        add_apartment(session, "Lark",
        "602 M.L.K. Jr Blvd, Chapel Hill, NC 27514", 
        "Pool, Gym", 
        1995)

        add_apartment(session, "Carolina Square",
        "133 W Franklin St, Chapel Hill, NC 27516", 
        "Pool, Gym", 
        2015)

        add_apartment(session, "Chancellor Square",
        "211 Church St, Chapel Hill, NC 27516", 
        "Pool, Gym", 
        2000)

        add_apartment(session, "Courtyard Lofts",
        "431 W Franklin St, Chapel Hill, NC 27516", 
        "Gym", 
        1988)

        add_apartment(session, "Mill Creek",
        "700 MLK Blvd (Airport Rd) in Chapel Hill, NC", 
        "Gym", 
        1977)

        add_apartment(session, "Shortbread",
        "333 W Rosemary St #130, Chapel Hill, NC 27516", 
        "Gym", 
        2011)

        add_apartment(session, "The Edition",
        "322 W Rosemary St, Chapel Hill, NC 27516", 
        "Pool, Gym", 
        2024)

        add_apartment(session, "Union",
        "425 Hillsborough St", 
        "Pool, Gym", 
        2017)

        add_apartment(session, "Warehouse",
        "316 W Rosemary St", 
        "Gym", 
        2005)

        add_events()

        # Show the default page
        self.show_page("AddRecordPage")

    def show_page(self, page_name):
        for page in self.pages.values():
            page.frame.grid_remove()  # Hide all pages
        self.pages[page_name].frame.grid(row=1, column=0, columnspan=2, pady=10)  # Show selected page


# Add Record Page
class AddRecordPage:
    def __init__(self, root):
        self.frame = Frame(root)

        Label(self.frame, text="Apartment ID:").grid(row=0, column=0, padx=10, pady=5)
        self.combo_apartment_id = ttk.Combobox(
            self.frame,
            values=sorted([
                "Carolina Square", 
                "Chancellor Square", 
                "Courtyard Lofts", 
                "Lark", 
                "Mill Creek", 
                "Shortbread", 
                "The Edition", 
                "Union", 
                "Warehouse"
            ]),
            state="readonly",
        )
        self.combo_apartment_id.set("Select")  # Default value
        self.combo_apartment_id.grid(row=0, column=1, padx=10, pady=5)

        Label(self.frame, text="User ID:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_user_id = Entry(self.frame)
        self.entry_user_id.grid(row=1, column=1, padx=10, pady=5)

        Label(self.frame, text="Rent:").grid(row=2, column=0, padx=10, pady=5)
        self.entry_rent = Entry(self.frame)
        self.entry_rent.grid(row=2, column=1, padx=10, pady=5)

        Label(self.frame, text="Bedrooms:").grid(row=3, column=0, padx=10, pady=5)
        self.entry_bedrooms = Entry(self.frame)
        self.entry_bedrooms.grid(row=3, column=1, padx=10, pady=5)

        Label(self.frame, text="Bathrooms:").grid(row=4, column=0, padx=10, pady=5)
        self.entry_bathrooms = Entry(self.frame)
        self.entry_bathrooms.grid(row=4, column=1, padx=10, pady=5)

        Label(self.frame, text="Year of Review:").grid(row=5, column=0, padx=10, pady=5)
        self.entry_year_of_review = Entry(self.frame)
        self.entry_year_of_review.grid(row=5, column=1, padx=10, pady=5)

        Label(self.frame, text="Comment:").grid(row=6, column=0, padx=10, pady=5)
        self.comment_frame = Frame(self.frame)
        self.entry_comments = Entry(self.frame)
        self.comment_frame.grid(row=6, column=1, padx=10, pady=5, sticky="nsew")
        self.text_comment = Text(self.comment_frame, width=40, height=5, wrap="word")
        self.text_comment.grid(row=0, column=0, sticky="nsew")
        scrollbar = Scrollbar(self.comment_frame, command=self.text_comment.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_comment.config(yscrollcommand=scrollbar.set)
        self.comment_frame.grid_rowconfigure(0, weight=1)
        self.comment_frame.grid_columnconfigure(0, weight=1)

        Button(self.frame, text="Submit Review", command=self.submit_review).grid(row=7, column=0, columnspan=2, pady=10)

    def submit_review(self):
        # Collect data from entry fields
        try:
            apartment_name = self.combo_apartment_id.get().split(" - ")[0]
            user_id = int(self.entry_user_id.get())
            rent = float(self.entry_rent.get())
            bedrooms = int(self.entry_bedrooms.get())
            bathrooms = int(self.entry_bathrooms.get())
            year_of_review = int(self.entry_year_of_review.get())
            comments = self.text_comment.get("1.0", "end-1c")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for User ID, Rent, Bedrooms, Bathrooms, and Year of Review.")
            return

        # Validation: Ensure all fields are filled
        if not all([apartment_name, user_id, rent, bedrooms, bathrooms, year_of_review]):
            messagebox.showwarning("Incomplete Data", "Please fill in all fields!")
            return
        

        # Try to add the review to the database (Placeholder)
        try:
            # Replace this with your database logic
            add_apartment_rating(session, 
            apartment_name=(apartment_name),                  
            comments=comments,  
            user_pid=user_id, 
            rent=rent, 
            bedrooms=bedrooms, 
            bathrooms=bathrooms, 
            year_of_review=year_of_review)
            print(f"Adding record: {apartment_name}, {user_id}, {rent}, {bedrooms}, {bathrooms}, {year_of_review}, {comments}")
            messagebox.showinfo("Success", "Review submitted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit review: {e}")

# bro

# Barebones Pages
class DeleteRecordPage:
    def __init__(self, root):
        self.frame = Frame(root)

        Label(self.frame, text="Rating ID:").grid(row=0, column=0, padx=10, pady=5)
        # Assign and place the entry for Rating ID
        self.entry_rating_id = Entry(self.frame)
        self.entry_rating_id.grid(row=0, column=1, padx=10, pady=5)

        Button(self.frame, text="Delete Record", command=self.delete_review).grid(row=1, column=0, columnspan=2, pady=10)
    
    def delete_review(self):
    # Collect data from entry fields
        try:
        # Assuming the review to delete is identified by a unique rating ID
            rating_id = int(self.entry_rating_id.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric Rating ID.")
            return

        # Validation: Ensure the field is filled
        if not rating_id:
            messagebox.showwarning("Incomplete Data", "Please enter the Rating ID to delete the review!")
            return

        # Try to delete the review from the database
        try:
            delete_apartment_rating(session, rating_id)  # Call the backend method
            print(f"Deleting review with Rating ID: {rating_id}")
            messagebox.showinfo("Success", f"Review with Rating ID {rating_id} deleted successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", f"Review not found: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete review: {e}")


class UpdateRentPage:
    def __init__(self, root):
        self.frame = Frame(root)

        Label(self.frame, text="Rating ID:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_rating_id = Entry(self.frame)
        self.entry_rating_id.grid(row=0, column=1, padx=10, pady=5)

        Label(self.frame, text="New Rent:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_new_rent = Entry(self.frame)
        self.entry_new_rent.grid(row=1, column=1, padx=10, pady=5)

        Button(self.frame, text="Update Rent", command=self.update_review_rent).grid(row=2, column=0, columnspan=2, pady=10)

    def update_review_rent(self):
        # Collect data from entry fields
        try:
            # Get the Rating ID and new rent value from the user
            rating_id = int(self.entry_rating_id.get())
            new_rent = float(self.entry_new_rent.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for Rating ID and Rent.")
            return

        # Validation: Ensure both fields are filled
        if not all([rating_id, new_rent]):
            messagebox.showwarning("Incomplete Data", "Please enter both the Rating ID and the new Rent value!")
            return

        # Try to update the review in the database
        try:
            update_rent(session, rating_id, new_rent)  # Call the backend method
            print(f"Updating rent for Rating ID {rating_id} to {new_rent}")
            messagebox.showinfo("Success", f"Rent for Rating ID {rating_id} updated successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", f"Review not found: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update rent: {e}")

class UpdateCommentPage:
    def __init__(self, root):
        self.frame = Frame(root)

        Label(self.frame, text="Rating ID:").grid(row=0, column=0, padx=10, pady=5)
        self.entry_rating_id = Entry(self.frame)
        self.entry_rating_id.grid(row=0, column=1, padx=10, pady=5)

        Label(self.frame, text="New Comments:").grid(row=1, column=0, padx=10, pady=5)
        self.entry_new_comments = Entry(self.frame)
        self.entry_new_comments.grid(row=1, column=1, padx=10, pady=5)

        Button(self.frame, text="Update Comments", command=self.update_review_comments).grid(row=2, column=0, columnspan=2, pady=10)

    def update_review_comments(self):
        # Collect data from entry fields
        try:
            # Get the Rating ID and new rent value from the user
            rating_id = int(self.entry_rating_id.get())
            new_comments = self.entry_new_comments.get()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for Rating ID.")
            return

        # Validation: Ensure both fields are filled
        if not all([rating_id]):
            messagebox.showwarning("Incomplete Data", "Please enter the Rating ID!")
            return

        # Try to update the review in the database
        try:
            update_comments(session, rating_id, new_comments)  # Call the backend method
            print(f"Updating rent for Rating ID {rating_id} to {new_comments}")
            messagebox.showinfo("Success", f"Comments for Rating ID {rating_id} updated successfully!")
        except ValueError as ve:
            messagebox.showerror("Error", f"Review not found: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update comment: {e}")

class ShowAllDataPage:
    def __init__(self, root):
        self.frame = Frame(root)
        self.session = session  # Store the database session

        Label(self.frame, text="Apartment Name:").grid(row=0, column=0, padx=10, pady=5)

        # Dropdown menu for apartment names
        self.combo_apartment_id = ttk.Combobox(
            self.frame,
            values=sorted([
                "Carolina Square", 
                "Chancellor Square", 
                "Courtyard Lofts", 
                "Lark", 
                "Mill Creek", 
                "Shortbread", 
                "The Edition", 
                "Union", 
                "Warehouse"
            ]),
            state="readonly",
        )
        self.combo_apartment_id.set("Select")  # Default value
        self.combo_apartment_id.grid(row=0, column=1, padx=10, pady=5)

        # Button to show all entries
        Button(self.frame, text="Show all entries", command=self.show_all_apt_data).grid(row=1, column=0, columnspan=2, pady=10)

        # Text widget to display query results
        self.results_text = Text(self.frame, width=60, height=20, wrap=WORD)
        self.results_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        self.results_text.config(state=DISABLED)  # Make it read-only by default

    def show_all_apt_data(self):
        apartment_name = self.combo_apartment_id.get()

        if apartment_name == "Select":
            messagebox.showwarning("Input Error", "Please select an apartment name!")
            return

        try:
            # Fetch popularity score
            apartment = self.session.query(Apartments).filter_by(apartment_name=apartment_name).first()
            if apartment and apartment.popularity_score:
                popularity_text = f"Popularity Score for {apartment_name}: {apartment.popularity_score}\n"
            else:
                popularity_text = f"Popularity Score for {apartment_name}: N/A\n"

            # Fetch reviews
            results = get_apt_reviews(self.session, apartment_name)

            # Clear the text widget and display popularity score
            self.results_text.config(state=NORMAL)
            self.results_text.delete(1.0, END)
            self.results_text.insert(END, popularity_text)
            self.results_text.insert(END, "-" * 40 + "\n")  # Divider

            # If no reviews, display a message
            if not results:
                self.results_text.insert(END, "No reviews found for the selected apartment.")
                self.results_text.config(state=DISABLED)
                return

            # Display reviews
            for review in results:
                self.results_text.insert(
                    END,
                    f"Review ID: {review.rating_id}\n"
                    f"User ID: {review.user_pid}\n"
                    f"Rent: {review.rent}\n"
                    f"Bedrooms: {review.bedrooms}\n"
                    f"Bathrooms: {review.bathrooms}\n"
                    f"Year of Review: {review.year_of_review}\n"
                    f"Comments: {review.comments}\n"
                    f"{'-' * 40}\n"
                )

            self.results_text.config(state=DISABLED)  # Make it read-only again

        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch reviews: {e}")




# Run the Application
if __name__ == "__main__":
    root = Tk()
    app = ApartmentManagementApp(root)
    root.mainloop()