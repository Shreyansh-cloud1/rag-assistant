import os  # Imports Python's built-in os module, which allows access to environment variables and operating system functions.

from dotenv import load_dotenv  # Imports the load_dotenv function from python-dotenv to load variables from a .env file.

from sqlalchemy import create_engine  # Imports create_engine from SQLAlchemy to create a database connection engine.


load_dotenv()  # Reads the .env file in the current directory and loads all variables into the environment.


DATABASE_URL = (  # Constructs the PostgreSQL connection string and stores it in DATABASE_URL.
    
    # Creates the first part of the connection string:
    # postgresql://username:password
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    
    # Appends the second part of the connection string:
    # @hostname:port/database_name
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

# Example final value of DATABASE_URL:
# postgresql://postgres:secret123@localhost:5432/ragdb


engine = create_engine(DATABASE_URL)  
# Creates a SQLAlchemy Engine object using the DATABASE_URL.
# The engine manages connections to the PostgreSQL database.
# You will use this engine to execute SQL queries or integrate with ORM models.