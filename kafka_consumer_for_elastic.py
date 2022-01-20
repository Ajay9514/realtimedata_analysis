import avro.schema
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import avro
import avro.io
import os
import io
# pip install kafka-python==2.0.2
# pip install lz4==3.1.3
# pip install elasticsearch
global ID
ID = 0
EL_ADDRESS = "elastic:changeme@localhost:9200"
SCHEMA_PATH = "./conf/MyEventRecord.avsc"
BOOTSTRAP_SERVERS = ['localhost:9092']
INDEXNAME = "realtimedata_analysis" 
class Kafka_Consumer():
    def __init__(self, schema = None, es_address= EL_ADDRESS, topic=None, client_id= None, group_id= None, bootstrap_servers = None):
        if all(arg is not None for arg in [schema, client_id, group_id, bootstrap_servers]):
            schema = SCHEMA_PATH
            self.schema = avro.schema.parse(open(schema,'r').read())
            self.topic = topic
            self.es_address = es_address
            self.client_id = client_id
            self.group_id = group_id
            self.bootstrap_servers = bootstrap_servers
            self.ID = 0
        else:
            raise TypeError

    def message_decoder(self):
        for message in self.kafa_consumer:
            bytes_reader = io.BytesIO(message.value)
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(self.schema)
            events = reader.read(decoder)
            print(events)
            es = Elasticsearch(self.es_address)
            es.index(index=INDEXNAME, id= self.ID, body=events)
            self.ID+=1

    def initialize_consumer(self):
        self.kafa_consumer = KafkaConsumer(self.topic, client_id= self.client_id, group_id= self.group_id, bootstrap_servers= self.bootstrap_servers)
        self.message_decoder()

if __name__ =="__main__":
    consumer_obj = Kafka_Consumer(schema=SCHEMA_PATH, es_address= EL_ADDRESS, topic="divolte", client_id="divolte.collector", group_id='divolte-group', bootstrap_servers=BOOTSTRAP_SERVERS)
    consumer_obj.initialize_consumer()