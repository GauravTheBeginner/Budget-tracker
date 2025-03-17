import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from dotenv import load_dotenv 

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_endpoint = os.getenv("DB_ENDPOINT")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

if not all([db_username, db_password, db_endpoint, db_port, db_name]):
    raise ValueError("Missing required database environment variables!")

db_password = quote_plus(db_password)



class DatabaseHelper:
    def __init__(self):
        self.engine = None
        self.session = None

    def __enter__(self):
        self.engine = self.get_database_engine()
        if not self.engine:
            raise Exception("Could not create database engine.")
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.engine.dispose()

    @staticmethod
    def get_database_engine():
        """
        Create a database engine using environment variables."""
        try:
            engine = create_engine(
                f'postgresql+psycopg2://{db_username}:{db_password}@{db_endpoint}:{db_port}/{db_name}',
                echo=False  
            )

            return engine
        except Exception as e:
            logging.error(f"Error creating the database engine: {e}")
            return None
        
