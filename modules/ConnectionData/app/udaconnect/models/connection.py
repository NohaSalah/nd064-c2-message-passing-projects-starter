from __future__ import annotations
from app import db
from dataclasses import dataclass
from app.udaconnect.models.person import Person
from app.udaconnect.models.location import Location


@dataclass
class Connection:
    location = Location
    person = Person
