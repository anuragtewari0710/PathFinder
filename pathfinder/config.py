import os
from dotenv import load_dotenv
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST','localhost'),
    'user': os.getenv('DB_USER','root'),
    'password': os.getenv('DB_PASS','#@Anu123'),
    'database': os.getenv('DB_NAME','pathfinder_db')
}

SECRET_KEY = os.getenv('SECRET_KEY','change-me')
SESSION_TYPE = os.getenv('SESSION_TYPE','filesystem')
