import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    WEB_URL = os.getenv("WEB_URL")
    CORRECT_EMAIL = os.getenv("CORRECT_EMAIL")
    CORRECT_PASSWORD = os.getenv("CORRECT_PASSWORD")
config = Config()
