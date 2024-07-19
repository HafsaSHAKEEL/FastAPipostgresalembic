from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Get the DATABASE_URL from environment variables
database_url = os.getenv('DATABASE_URL')

# Ensure the DATABASE_URL is correctly set
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Use the DATABASE_URL to create the SQLAlchemy engine
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

