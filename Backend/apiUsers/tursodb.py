
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

TURSO_DB_URL = os.environ.get("TURSO_DATABASE_URL")
TOKEN_DB = os.environ.get("TURSO_AUTH_TOKEN")

engine = create_engine(
     "sqlite+libsql:///embedded.db",
     connect_args={
         "auth_token": TOKEN_DB,
         "sync_url": TURSO_DB_URL,
     },
)