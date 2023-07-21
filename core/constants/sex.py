from sqlalchemy import Enum

class Sex(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"