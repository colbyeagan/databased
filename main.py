from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# base class
Base = declarative_base()

# Define the model
class ApartmentRating(Base):
    __tablename__ = 'apartment_ratings'

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    apartment_id = Column(Integer, ForeignKey('apartments.apartment_id'), nullable=False)
    comments = Column(String(255), nullable=True)
    user_id = Column(Integer, nullable=False)
    rent = Column(Float, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    year_of_review = Column(Integer, nullable=True)

    def __init__(self, apartment_id, comments, user_id, rent, bedrooms, bathrooms, year_of_review):
        self.apartment_id = apartment_id
        self.comments = comments
        self.user_id = user_id
        self.rent = rent
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.year_of_review = year_of_review

class Apartments(Base):
    __tablename__ = 'apartments'

    apartment_id = Column(Integer, autoincrement=True, primary_key=True)
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

# add a record
def add_apartment_rating(session, rating):
    session.add(rating)
    session.commit()

# add a record
def add_apartment(session, apartment):
    session.add(apartment)
    session.commit()

# Main
if __name__ == "__main__":
    # Initialize db
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()

    # add a new record
    """
    new_rating = ApartmentRating(
        rating_value=4.5,
        apartment_id=101,
        user_id=1,
        rent=1500.00,
        bedrooms=2, 
        bathrooms=1,
        year_of_review=2024
    )
    add_apartment_rating(session, new_rating)
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
