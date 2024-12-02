from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column("rating_id", Integer, primary_key=True)
    apartment_id = Column("apartment_id", Integer)
    user_id = Column("user_id", Integer)
    rent = Column("rent", Integer)
    location = Column("location", String)
    bedrooms = Column("bedrooms", Integer)
    bathrooms = Column("bathrooms", Integer)
    amenities = Column("amenities", String)

    def __init__(self, rating_id, apartment_id, user_id, rent, location, bedrooms, bathrooms, amenities):
        self.rating_id = rating_id
        self.apartment_id = apartment_id
        self.user_id = user_id
        self.rent = rent
        self.location = location
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.amenities = amenities

    def __repr__(self):
        return f"({self.rating_id}) {self.apartment_id} {self.user_id} ({self.rent}, {self.location})"
    
engine = create_engine("sqlite:///UNCRentDB.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

rating = Rating(1, 1, 1, 750, "Shortbread", 3, 1.5, "pool!")

rating1 = Rating(2, 2, 2, 10000, "Union", 4, 4, "nothing")

rating2 = Rating(3, 3, 3, 1200, "Lark", 3, 3, "gym!")

rating3 = Rating(4, 2, 4, 9500, "Union", 2, 2, "nothing!")

session.add(rating)
session.add(rating1)
session.add(rating2)
session.add(rating3)

session.commit()

results = session.query(Rating).all()
print(results)