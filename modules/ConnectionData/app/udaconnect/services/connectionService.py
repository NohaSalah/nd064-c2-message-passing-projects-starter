from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from builtins import staticmethod
from google.protobuf.timestamp_pb2 import Timestamp
from sqlalchemy.sql import text

from app.udaconnect.infra.database import DBSession, engine
from app.udaconnect.services.locationServices import LocationService
from app.udaconnect.services.personService import PersonService

from app.udaconnect.proto.connection_data_pb2 import Person as PersonPB2, \
    Location as LocationPB2, ConnectionMessage, ConnectionMessageList



session = DBSession()

data_channel = grcp.insecure_channel("udaconnect-connection-api:5005")
serviceStub = ConnectionServiceStub(data_channel)


class ConnectionService:
    @staticmethod
    def find_contacts(person_id, start_date, end_date, meters):
        """
        Finds all Person who have been within a given distance of a given Person within a date range.

        This will run rather quickly locally, but this is an expensive method and will take a bit of time to run on
        large datasets. This is by design: what are some ways or techniques to help make this data integrate more
        smoothly for a better user experience for API consumers?
        """
        startTime = Timestamp(seconds = int(start_date.timestamp()))

        endtTime = Timestamp(seconds = int(end_date.timestamp()))
        
        searchMesg = SearchMesg(
                                person_id = person_id,
                                start_date = startTime,
                                end_date = endtTime, 
                                meters = meters
                                )
        response = serviceStub.FindContacts(searchMesg)
        return response

        