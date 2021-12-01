from typing import Dict, List
from builtins import staticmethod
from functools import lru_cache

from app.udaconnect.infra.database import DBSession
from app.udaconnect.models import Person

session = DBSession()

class PersonService:
    @staticmethod
    def retrieve(person_id: int) -> Person:
        person = session.query(Person).get(person_id)
        return person

    @staticmethod
    def retrieve_all() -> List[Person]:
        return session.query(Person).all()
