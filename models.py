# models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from fasthtml.common import database

Base = declarative_base()

class Growers(Base):
    __tablename__ = 'growers'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    contact_info = Column(String(255), nullable=False)
    joined_at = Column(Date, nullable=False)
    address = Column(String(255))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    group_membership = Column(String(255))

class SeedSource(Base):
    __tablename__ = 'seedsource'
    id = Column(Integer, primary_key=True)
    succession_number = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    germination_rate = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    scarification_instructions = Column(Text)
    stratification_instructions = Column(Text)
    date_added = Column(Date, nullable=False)
    seeds_issued = Column(Integer)
    geographic_location = Column(String(255))
    supplier = Column(String(255))
    viability_duration = Column(String(255))

class SubSuccession(Base):
    __tablename__ = 'subsuccession'
    id = Column(Integer, primary_key=True)
    sub_succession_number = Column(String(255), nullable=False)
    seed_source_id = Column(Integer, ForeignKey('seedsource.id'), nullable=False)
    grower_id = Column(Integer, ForeignKey('growers.id'), nullable=False)
    created_at = Column(Date, nullable=False)
    status = Column(String(255), nullable=False)
    merged_into = Column(Integer, ForeignKey('subsuccession.id'))
    parent_sub_succession = Column(Integer, ForeignKey('subsuccession.id'))
    expected_outcome = Column(Text)

class Trees(Base):
    __tablename__ = 'trees'
    id = Column(Integer, primary_key=True)
    sub_succession_id = Column(Integer, ForeignKey('subsuccession.id'), nullable=False)
    species = Column(String(255), nullable=False)
    growth_stage = Column(String(255), nullable=False)
    planted_at = Column(Date, nullable=False)
    height = Column(Float)
    health_status = Column(String(255))
    yield_data = Column(Text)
    notes = Column(Text)

class EnvironmentalMonitoring(Base):
    __tablename__ = 'environmentalmonitoring'
    id = Column(Integer, primary_key=True)
    tree_id = Column(Integer, ForeignKey('trees.id'), nullable=False)
    timestamp = Column(Date, nullable=False)
    soil_moisture = Column(String(255))
    light_exposure = Column(String(255))
    temperature = Column(Float)

class DistributionLog(Base):
    __tablename__ = 'distributionlog'
    id = Column(Integer, primary_key=True)
    seed_source_id = Column(Integer, ForeignKey('seedsource.id'), nullable=False)
    sub_succession_id = Column(Integer, ForeignKey('subsuccession.id'), nullable=False)
    seeds_issued = Column(Integer, nullable=False)
    issued_at = Column(Date, nullable=False)

class AssignedSubSuccessions(Base):
    __tablename__ = 'assignedsubsuccessions'
    id = Column(Integer, primary_key=True)
    grower_id = Column(Integer, ForeignKey('growers.id'), nullable=False)
    sub_succession_id = Column(Integer, ForeignKey('subsuccession.id'), nullable=False)

# Setup SQLite database
engine = create_engine('sqlite:///seedgrower.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
