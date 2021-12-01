import logging
import json

from kafka import KafkaProducer


logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-location-svc")

TOPIC_NAME = 'location'              
KAFKA_SERVER = 'kafka:9092'
kafkaProducer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

class LocationProducer:
    @staticmethod
    # Produces message to Kafka location in creation topic
    def sendMsg(location):
        kafkaProducer.send(TOPIC_NAME, json.dumps(location).encode())
        # flush kafka connection
        kafkaProducer.flush(timeout=5.0)
