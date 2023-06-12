import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
# Database
# real_db
load_dotenv()

#

# for CI 
IP_ADDRESS = "59.18.243.166"
WIFI_ADDRESS = "172.30.1.56"

# for local

PUBLIC_MONGODB = f"mongodb://{IP_ADDRESS}:54555/test"
PUBLIC_TEST = f"mongodb://{IP_ADDRESS}:54254/test"


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

# LOGIN, LOGOUT
LOGIN = "login"
LOGIN_TIME = "login_time"
LOGOUT_TIME = "logout_time"

USAGE = "usage"
USER_ID = "user_id"

EMAIL = "email"
PASSWORD = "password"
NICKNAME = "nickname"
ACCOUNT = "account"
DEVICE = "device"
CLIENT_IP = "client_ip"
CREATED_AT = "created_at"





