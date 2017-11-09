from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# Define the tables:
from sqlalchemy import Column, Integer, Text, String, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

# episode_details:
class episode_details(Base):
    __tablename__ = 'episode_details'

    episode_id = Column(Integer, primary_key = True)    # Primary Key episode_id
    episode_narrative = Column(Text)
    

# event_details:
class event_details(Base):
    __tablename__ = 'event_details'
    
    event_id = Column(Integer, primary_key = True)   # Primary Key event_id
    episode_id = Column(Integer, ForeignKey('episode_details.episode_id'))   # Foreign Key constraint on episode_id
    event_narrative = Column(Text)
    month_name = Column(String)
    year = Column(Integer)
    begin_date_time = Column(DateTime)
    end_date_time = Column(DateTime)
    state_fips = Column(Integer)
    cz_fips = Column(Integer)
    cz_type = Column(String)
    cz_name = Column(String)
    state = Column(String)
    wfo = Column(String)
    cz_timezone = Column(String)
    injuries_direct = Column(Integer)
    injuries_indirect = Column(Integer)
    deaths_direct = Column(Integer)
    deaths_indirect = Column(Integer)
    event_type = Column(String)
    magnitude = Column(Float)
    magnitude_type = Column(String)
    category = Column(String)
    tor_f_scale = Column(String)
    tor_length = Column(Float)
    tor_width = Column(Float)
    tor_other_wfo = Column(String)
    tor_other_cz_state = Column(String)
    tor_other_cz_fips = Column(Integer)
    tor_other_cz_name = Column(String)
    damage_property = Column(Integer)
    damage_crops = Column(Integer)
    flood_cause = Column(String)
    event_detailscol = Column(String)
    begin_range = Column(String)
    begin_azimuth = Column(Float)
    begin_location = Column(String)
    end_range = Column(String)
    end_azimuth = Column(Float)
    end_location = Column(String)
    begin_latitute = Column(Float)
    begin_longitude = Column(Float)
    end_lattitude = Column(Float)
    end_longitude = Column(Float)
    data_source = Column(String)
    
    # Set up relationship between Event and Episode:
    episode = relationship('episode_details', back_populates = 'events')



# fatalities:
class fatalities(Base):
    __tablename__ = 'fatalities'
    
    fatality_id = Column(Integer, primary_key = True)
    event_id = Column(Integer, ForeignKey("event_details.event_id"))
    fatality_type = Column(String)
    fatality_date = Column(DateTime)
    fatality_age = Column(Integer)
    fatality_sex = Column(String)
    fatality_location = Column(String)

    # Relationship between fatalities and event
    event = relationship("event_details", back_populates = "fatalities1")

# location:
class location(Base):
    __tablename__ = 'location'

    episode_id = Column(Integer)
    event_id = Column(Integer, ForeignKey("event_details.event_id"), primary_key = True)
    location_index = Column(Integer)
    range = Column(Float)             # Note: lrange = range in table
    azimuth = Column(String)
    location = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    latitudeTwo = Column(Float)
    longitudeTwo = Column(Float)
    location_pk = Column(Integer, primary_key = True)
    
    # Relationship between locations and event
    event = relationship("event_details", back_populates = "locations")
    
# Update Foreign Keys:
episode_details.events = relationship('event_details', order_by = event_details.event_id, back_populates = 'episode')
event_details.fatalities1 = relationship('fatalities', order_by = fatalities.fatality_id, back_populates = 'event')
event_details.locations = relationship('location', order_by = location.location_index, back_populates = 'event')
