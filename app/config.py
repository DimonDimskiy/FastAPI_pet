import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# <------ jwt
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# <------ end jwt
SCOPES = {"admin": {"muscle_group_post", "muscle_post", "muscle_delete"}}

DEFAULT_LIMIT = 20
