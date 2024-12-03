from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    DB_PATH = os.getenv("DB_PATH", ":memory:")  # Default to in-memory database
