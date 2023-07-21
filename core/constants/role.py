from sqlalchemy import Enum

class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"