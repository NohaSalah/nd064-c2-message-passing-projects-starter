from datetime import datetime

from app.udaconnect.models.person import Person
from app.udaconnect.models.location import Location
from app.udaconnect.models.connection import Connection
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services.personService import PersonService
from app.udaconnect.services.connectionService import ConnectionService

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource, Fields
from typing import Optional, List


DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Person Data.")  # noqa


# TODO: This needs better exception handling
personModel = api.model('Person',{
                                    'id' : fields.Integer,
                                    'first_name' : fields.String,
                                    'last_name' : fields.String,
                                    'company_name' : fields.String
                                 })

locationModel = api.model('Location',{
                                        'id' : fields.Integer,
                                        'person_id' : fields.Integer,
                                        'longitude' : fields.String,
                                        'latitude' : fields.String,
                                        'creation_time' : fields.DateTime
                                     })

connectionModel = api.model('Connection',{
                                            'location' : fields.Nested(locationModel),
                                            'person' : fields.Nested(personModel)
                                         })

@api.route("/locations")
@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")
class LocationResource(Resource):
    @accepts(schema=LocationSchema)
    @responds(schema=LocationSchema)
    def post(self) -> Location:
        request.get_json()
        location: Location = LocationService.create(request.get_json())
        return location

    @responds(schema=LocationSchema)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        new_person: Person = PersonService.create(payload)
        return new_person

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
