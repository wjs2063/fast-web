import os
# Database
# real_db


# for CI 
IP_ADDRESS = "59.18.243.166"
WIFI_ADDRESS = "172.30.1.56"

# for local

ORIGIN_MONGODB = f"mongodb://{IP_ADDRESS}:54555/test"
TEST_MONGODB = f"mongodb://{IP_ADDRESS}:54254/test"


LOCAL_MONGODB = f"mongodb://{WIFI_ADDRESS}:54555/test"
LOCAL_TEST = f"mongodb://{WIFI_ADDRESS}:54254/test"

ALGORITHM = os.environ["ALGORITHM"]
SECRETKEY = os.environ["SECRETKEY"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
#REFRESH_TOKEN_EXPIRE_MINUTES = os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"]










