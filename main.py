from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# base class
Base = declarative_base()

# Define the model
class ApartmentRating(Base):
    __tablename__ = 'apartment_ratings'

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_name = Column(Integer, ForeignKey('apartments.apartment_name'), nullable=False)
    comments = Column(String(255), nullable=True)
    user_pid = Column(Integer, nullable=False)
    rent = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    year_of_review = Column(Integer, nullable=True)

    def __init__(self, apartment_name, comments, user_pid, rent, bedrooms, bathrooms, year_of_review):
        self.apartment_name = apartment_name
        self.comments = comments
        self.user_pid = user_pid
        self.rent = rent
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.year_of_review = year_of_review

class Apartments(Base):
    __tablename__ = 'apartments'

    apartment_name = Column(String(255), primary_key=True)
    location = Column(String(255), nullable=False)
    amenities = Column(Text, nullable=True)
    year_of_construction = Column(Integer, nullable=True)

    def __init__(self, location, amenities, year_of_construction):
        self.location = location
        self.amenities = amenities
        self.year_of_construction = year_of_construction

# Function to initialize db
def init_db():
    from __main__ import ApartmentRating, Apartments
    engine = create_engine('sqlite:///UNCRentdb.db', echo=True)
    Base.metadata.create_all(engine)
    return engine

# add a rating
def add_apartment_rating(session, apartment_name, comments, user_pid, rent, bedrooms, bathrooms, year_of_review):
    # Check if the user already has a review for the specified year
    existing_review = session.query(ApartmentRating).filter(
        ApartmentRating.user_pid == user_pid,
        ApartmentRating.year_of_review == year_of_review
    ).first()

    if existing_review:
        raise ValueError(f"User {user_pid} already has a review for the year {year_of_review}.")

    if(apartment_name == "Select"):
        raise ValueError(f"Please choose an apartment for your review.")

    # If no existing review, proceed to create a new one
    new_rating = ApartmentRating(
        apartment_name=apartment_name,
        comments=comments,
        user_pid=user_pid,
        rent=rent,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        year_of_review=year_of_review
    )
    try:
        session.add(new_rating)
        session.commit()  # Commit the transaction
    except Exception as e:
        session.rollback()  # Rollback in case of errors
        raise e  # Re-raise the exception for the caller to handle

# add an apartment
def add_apartment(session, apartment):
    session.add(apartment)
    session.commit()

def get_apt_reviews(session, apartment_name):
    try:
        results = session.query(ApartmentRating).filter_by(apartment_name=apartment_name).all()
        return results
    except Exception as e:
        print(f"Error fetching apartment reviews: {e}")
        return []

# delete a record
def delete_apartment_rating(session, rating_id):
    """
    Deletes a rating from the apartment_ratings table using the rating_id.

    :param session: SQLAlchemy session object
    :param rating_id: The ID of the rating to delete
    :raises ValueError: If no rating is found with the provided rating_id
    """
    # Query the table for the specific rating_id
    rating_to_delete = session.query(ApartmentRating).filter_by(rating_id=rating_id).first()

    if rating_to_delete:
        try:
            session.delete(rating_to_delete)
            session.commit()
            print(f"Rating with ID {rating_id} deleted successfully.")
        except Exception as e:
            session.rollback()  # Rollback in case of an error
            raise Exception(f"An error occurred while deleting the rating: {e}")
    else:
        # Raise an exception if the rating is not found
        raise ValueError(f"No rating found with ID {rating_id}.")


# update a record
def udpate_apartment_rating(session, rating):
    session.add(rating)
    session.commit()

# return all records with matching apartment id
def get_apartment_ratings(session, apartment_name):
    results = session.query(ApartmentRating).filter(ApartmentRating.apartment_name == apartment_name).all()
    return results

def update_comments(session, rating_id, new_comments):
    """
    Updates the comments field of a record in the apartment_ratings table.
    """
    try:
        # Query the database for the rating
        rating_to_update = session.query(ApartmentRating).filter_by(rating_id=rating_id).first()

        # Check if the rating exists
        if not rating_to_update:
            raise ValueError(f"No rating found with Rating ID {rating_id}.")

        # Validate that new_rent is a float
        if not isinstance(new_comments, String):
            raise ValueError("The new rent must be a String value.")

        # Update the rent and commit the transaction
        rating_to_update.comment = new_comments
        session.commit()
        print(f"Comment for rating ID {rating_id} updated to {new_comments}.")

    except ValueError as ve:
        print(f"Validation error: {ve}")
        raise ve  # Re-raise the ValueError for the caller to handle
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction in case of error
        raise Exception(f"An error occurred while updating the comments: {e}")


def update_rent(session, rating_id, new_rent):
    """
    Updates the rent field of a record in the apartment_ratings table.

    :param session: SQLAlchemy session object
    :param rating_id: The ID of the rating to update
    :param new_rent: The new rent value to set (must be a float)
    :raises ValueError: If no rating is found with the provided rating_id
    """
    try:
        # Query the database for the rating
        rating_to_update = session.query(ApartmentRating).filter_by(rating_id=rating_id).first()

        # Check if the rating exists
        if not rating_to_update:
            raise ValueError(f"No rating found with Rating ID {rating_id}.")

        # Validate that new_rent is a float
        if not isinstance(new_rent, float):
            raise ValueError("The new rent must be a float value.")

        # Update the rent and commit the transaction
        rating_to_update.rent = new_rent
        session.commit()
        print(f"Rent for rating ID {rating_id} updated to {new_rent}.")

    except ValueError as ve:
        print(f"Validation error: {ve}")
        raise ve  # Re-raise the ValueError for the caller to handle
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Rollback the transaction in case of error
        raise Exception(f"An error occurred while updating the rent: {e}")


# Main
if __name__ == "__main__":
    # Initialize db
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # add a new record
    """
    add_apartment_rating(session, apartment_name=101,
        comments="Amazing stay",
        user_pid=730566108,
        rent=1500.00,
        bedrooms=2, 
        bathrooms=1,
        year_of_review=2024)
    """

    
    # add a new apartment
    """
    new_apartment = Apartments(
        "602 M.L.K. Jr Blvd, Chapel Hill, NC 27514", 
        "Pool, Gym", 
        1995
    )
    add_apartment(session, new_apartment)
    """

    # delete a review
    """
    rating_id=1
    delete_apartment_rating(session, rating_id)
    """

    # update rent
    """
    rating_id=1
    update_rent(session, rating_id, 1900.00)
    """

    # update comment
    """
    rating_id=1
    update_comment(session, rating_id, "Great stay!")
    """