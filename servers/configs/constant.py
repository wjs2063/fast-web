import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
# Database
# real_db
load_dotenv()

#

# for CI 
GCP_PUBLIC_ADDRESS = os.environ["GCP_PUBLIC_ADDRESS"]
TEST_ADDRESS = os.environ["TEST_ADDRESS"]
WIFI_ADDRESS = "172.30.1.56"

# for local

PUBLIC_MONGODB = f"mongodb://{GCP_PUBLIC_ADDRESS}:27017/test"
PUBLIC_TEST = f"mongodb://{TEST_ADDRESS}:54254/test"


PRIVATE_MONGODB = f"mongodb://{WIFI_ADDRESS}:54555/test"
PRIVATE_TEST = f"mongodb://{WIFI_ADDRESS}:54254/test"

ALGORITHM = os.environ["ALGORITHM"]
SECRETKEY = os.environ["SECRETKEY"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]

OWN_EMAIL = os.environ["OWN_EMAIL"]
OWN_EMAIL_PASSWORD = os.environ["OWN_EMAIL_PASSWORD"]

REFRESH_TOKEN_EXPIRE_DAY = os.environ["REFRESH_TOKEN_EXPIRE_DAY"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

# TOKEN 
TOKEN = "token"
REFRESH_TOKEN = "refresh_token"
ACCESS_TOKEN = "access_token"

#USER
USERS = "users"

# LOGIN, LOGOUT DATABASE
LOGIN = "login"
LOGIN_TIME = "login_time"
LOGOUT_TIME = "logout_time"
DEVICE = "device"
CLIENT_IP = "client_ip"
CREATED_AT = "created_at"
UPDATED_AT = "updated_at"

USAGE = "usage"
USER_ID = "user_id"

EMAIL = "email"
PASSWORD = "password"
NICKNAME = "nickname"
ACCOUNT = "account"

ANSWER_ID = "answer_id"
ITEM_ID = "item_id"
OBJECT_ID = "objectId"
ID = "_id"




DEFAULT_LIMIT = 10
QUESTIONS = "questions"
ANSWERS = "answers"
ANSWER = "answer"
CONTENT = "content"
COMMENTS = "comments"
TOTAL_DOCS = "total_docs"
IS_COMPLETED = "is_completed"

PAGE = "page"