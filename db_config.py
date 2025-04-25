import os
from dotenv import load_dotenv

# Load environment variables if using .env file
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME', 'postgres'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432')
}

# Create connection string for SQLAlchemy
DB_URI = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"

# SQLite URI for fallback/development
SQLITE_URI = 'sqlite:///pharma_app.db'

# Flag to force use of SQLite (set to True for local development)
USE_SQLITE = os.getenv('USE_SQLITE', 'true').lower() in ('true', '1', 't')

# Function to get the appropriate URI based on environment or settings
def get_uri():
    if USE_SQLITE:
        return SQLITE_URI
    return DB_URI

# Create connection string for psycopg2
def get_db_url():
    return f"dbname={DB_CONFIG['dbname']} user={DB_CONFIG['user']} password={DB_CONFIG['password']} host={DB_CONFIG['host']} port={DB_CONFIG['port']}"
