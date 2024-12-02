from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# base class
Base = declarative_base()

# Define the model
class ApartmentRating(Base):
    __tablename__ = 'apartment_ratings'

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    rating_value = Column(Float, nullable=False)
    apartment_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    rent = Column(Float, nullable=False)
    location = Column(String(255), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    amenities = Column(Text, nullable=True)
    year = Column(Integer, nullable=True)

    def __init__(self, rating_value, apartment_id, user_id, rent, location, bedrooms, bathrooms, amenities, year):
        self.rating_value = rating_value
        self.apartment_id = apartment_id
        self.user_id = user_id
        self.rent = rent
        self.location = location
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.amenities = amenities
        self.year = year

# Function to initialize db
def init_db():
    engine = create_engine('sqlite:///UNCRentdb.db', echo=True)
    Base.metadata.create_all(engine)
    return engine

# add a record
def add_apartment_rating(session, rating):
    session.add(rating)
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
        location="Downtown",
        bedrooms=2,
        bathrooms=1,
        amenities="Pool, Gym, Parking"
        year=2024
    )

    add_apartment_rating(session, new_rating)
    """
