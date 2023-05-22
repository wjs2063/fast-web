import os
# Database
# real_db


# for CI 
IpAddress = "59.18.243.166"


# for local
WifiAddress = "172.30.1.56"
ORIGIN_MONGODB = f"mongodb://{IpAddress}:54555/test"
TEST_MONGODB = f"mongodb://{IpAddress}:54254/test"


LOCAL_MONGODB = f"mongodb://{WifiAddress}:54555/test"
TEST_MONGODB = f"mongodb://{WifiAddress}:54254/test"

ALGORITHM = os.environ["ALGORITHM"]
SECRETKEY = os.environ["SECRETKEY"]
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]
#REFRESH_TOKEN_EXPIRE_MINUTES = os.environ["REFRESH_TOKEN_EXPIRE_MINUTES"]










