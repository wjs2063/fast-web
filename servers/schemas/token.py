from dataclasses import dataclass
from datetime import datetime


@dataclass
class Token:
    user_id:str
    exp: str

