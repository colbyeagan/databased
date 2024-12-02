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

# delete a record
def delete_apartment_rating(session, rating_id):
    """
    Deletes a rating from the apartment_ratings table using the rating_id.

    :param session: SQLAlchemy session object
    :param rating_id: The ID of the rating to delete
    """
    # Query the table for the specific rating_id and delete it
    rating_to_delete = session.query(ApartmentRating).filter_by(rating_id=rating_id).first()
    
    if rating_to_delete:
        session.delete(rating_to_delete)
        session.commit()
        print(f"Rating with ID {rating_id} deleted successfully.")
    else:
        print(f"No rating found with ID {rating_id}.")


# update a record
def udpate_apartment_rating(session, rating):
    session.add(rating)
    session.commit()

# return all records with matching apartment id
def get_apartment_ratings(session, apartment_name):
    results = session.query(ApartmentRating).filter(ApartmentRating.apartment_name == apartment_name).all()
    return results

def update_rent(session, rating_id, new_rent):
    """
    Updates the rent field of a record in the apartment_ratings table.
    """
    try:
        rating_to_update = session.query(ApartmentRating).filter_by(rating_id=rating_id).first()
        
        if rating_to_update and isinstance(new_rent, float):
            rating_to_update.rent = new_rent
            session.commit()
            print(f"Rent for rating ID {rating_id} updated to {new_rent}.")
        elif rating_to_update and not isinstance(rating_to_update, str):
            print(f"Rent must be a float")
        else:
            print(f"No rating ID {rating_id} found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()

# update a rating comment
def update_comment(session, rating_id, new_comment):
    """
    Updates the rent field of a record in the apartment_ratings table.
    """
    try:
        rating_to_update = session.query(ApartmentRating).filter_by(rating_id=rating_id).first()
        
        if rating_to_update and isinstance(new_comment, str):
            rating_to_update.comments = new_comment
            session.commit()
            print(f"Rent for rating ID {rating_id} updated to {new_comment}.")
        elif rating_to_update and not isinstance(rating_to_update, str):
            print(f"Comment must be a string")
        else:
            print(f"No rating ID {rating_id} found.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()

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