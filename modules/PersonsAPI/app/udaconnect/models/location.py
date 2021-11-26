from app import db
from datetime import datetime
from app.udaconnect.models.person import Person
from geoalchemy2 import Geometry as GeometryType
from geoalchemy2.shape import to_shape
from shapely.geometry.point import Point
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger
from sqlalchemy.ext.hybird import hybird_property
from __future__ import annotations

class Location(db.Model):
    __tablename__= 'location'
    id = Column(BigInteger, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id),nullable=False)
    coordinate = Column(Geometry('POINT'),nullable=False)
    creation_time = Column(DateTime,default=datetime.utcnow,nullable=False)
    _wkt_shape:str = None

# get readable text from binary form
# from geoalchemy2.functions import ST_AsText, ST_Point
@property
def wkt_shape(self) -> str:
    if not self._wkt_shape:
        point : Point = to_shape(self.coordinate)
        self._wkt_shape = point.to_wkt().replace('POINT','ST_POINT')
    return self._wkt_shape

# coordinate ---> longitude & latitude 
