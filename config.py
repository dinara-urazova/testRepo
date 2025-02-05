import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    POSTGRESQL_DATABASE=os.getenv('POSTGRESQL_DATABASE')
    POSTGRESQL_USERNAME=os.getenv('POSTGRESQL_USERNAME')
    POSTGRESQL_PASSWORD=os.getenv('POSTGRESQL_PASSWORD')
    POSTGRESQL_HOSTNAME=os.getenv('POSTGRESQL_HOSTNAME')
    POSTGRESQL_PORT=os.getenv('POSTGRESQL_PORT')