from datetime import datetime

from app.udaconnect.models import Location
from app.udaconnect.schemas import LocationSchema

from app.udaconnect.services.locationServices import LocationService

from flask import request
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect-Location API", description="Location data.")  # noqa


# TODO: This needs better exception handling

locationResult = api.model(
                                'Location',{
                                                'id' : fields.Integer,
                                                'person_id' : fields.Integer,
                                                'longitude' : fields.String,
                                                'latitude' : fields.String,
                                                'creation_time' : fields.DateTime
                                           }
                          ) 

@api.route("/locations")
class LocationListResource(Resource):

    @accepts(schema=LocationSchema)

    @api.doc(description = 'Creation of a new location',
             body = locationResult,
             responses = {
                            202 : 'Accepted Location Creation',
                            500 : 'Internal Server Error'
                         }
            )
   
    def post(self):
        location: Location = request.get_json()
        LocationService.create(location)
        return {'status' : 'accepted'}, 202


@api.route("/locations/<location_id>")
@api.param("location_id", "Unique ID for a given Location", _in="query")

class LocationResource(Resource):
    @responds(schema=LocationSchema)

    @api.doc(description = 'Search for a given location by id',
             params = {'location_id' : 'Required location id'},
             responses = {
                            404 : 'Location Not Found',
                            500 : 'Internal Server Error'
                         }
            )
    @api.response(200, 'Location is founded', locationResult)
    def get(self, location_id) -> Location:
        location: Location = LocationService.retrieve(location_id)
        return location




