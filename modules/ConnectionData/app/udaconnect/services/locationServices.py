from typing import Dict, List
from builtins import staticmethod
from functools import lru_cache

from app.udaconnect.models import Location
from app.udaconnect.infra.database import DBSession

session = DBSession()

class LocationService:
    @lru_cache(maxsize=10)
    @staticmethod
    def fetchLocations(person_id, start_date, end_date) -> List:
        locations : List = (
                        session.query(Location).filter(Location.person_id == person_id)
                        .filter(Location.creation_time < end_date)
                        .filter(Location.creation_time >= start_date).all()
                        )
        return locations