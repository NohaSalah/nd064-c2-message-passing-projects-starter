from datetime import datetime
from builtins import staticmethod

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

# build person,location and connection models
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

"""
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
"""


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    @responds(schema=PersonSchema, many=True)
    
    @api.doc(description = 'Creation of a new location',
             body = personModel,
             responses = {
                            202 : 'Accepted Person Creation',
                            500 : 'Internal Server Error'
                         }
            )

    def post(self):
        payload = request.get_json()
        PersonService.create(payload)
        return {'status' : 'accepted person creation'}, 202

    @api.doc(description = 'Existing Persons')
    @api.response(200, 'Persons List', fields.List(fields.Nested(personModel)))
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)

    @api.doc(
                description = 'Search for a person with a specific id',
                params = {'person_id' : 'required person id'},
                responses = {
                                404 : 'Person Not Found',
                                500 : 'Internal Server Error'
                            }
            )

    @api.response(200, 'Person Found', personModel )

    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")

@api.doc(
            description = 'Search for a connection data for a person with his id',
            model = connectionModel
        )

class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> List[ConnectionSchema]:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=int(person_id),
            start_date=start_date,
            end_date=end_date,
            meters=float(distance),
        )

        connectionList : List[Connection] = [
                                                 ConnectionDataResource.pb2ToModel(connection)
                                                 for connection in results.connections
                                            ]

        return connectionList

@staticmethod
def pb2ToModel(connection) -> Connection:
    location_pb2 = connection.location
    locationData = Location(
                            id = location_pb2.id,
                            person_id = location_pb2.person_id,
                            creation_time = datetime.fromtimestamp(location_pb2.creation_time.seconds)
                       )
    person_pb2 = connection.person
    personData = Person(
                        id = person_pb2.id,
                        first_name = person_pb2.first_name,
                        last_name = person_pb2.last_name,
                        company_name = person_pb2.company_name
                   )                       
    return Connection(location=locationData, person=personData)                   