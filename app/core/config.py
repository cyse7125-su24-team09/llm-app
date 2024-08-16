import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ES_HOST_URL = os.getenv("ES_HOST_URL")
    ES_USERNAME = os.getenv("ES_USERNAME")
    ES_PASSWORD = os.getenv("ES_PASSWORD")
    APP_PORT = int(os.getenv("APP_PORT"))
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")
config = Config()
