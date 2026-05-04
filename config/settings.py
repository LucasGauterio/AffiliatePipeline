import os
from dotenv import load_dotenv

load_dotenv()

class AppSettings:
    def __init__(self):
        self.ENV = os.getenv("ENV", "development")
        self.GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
