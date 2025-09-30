from flask import Flask, request, abort
from confluent_kafka import Producer
from confluent_kafka import Consumer
import socket
import uuid
import json
import logging

app = Flask(__name__)
 
@app.route('/api/events/health')
def health():
    return "{\"status\": true}"

@app.route('/api/events/movie', methods=['POST'])
def movie():
    massage=json.dumps(request.json)
    message=massage.encode('utf-8')
    conf = {'bootstrap.servers': 'kafka:9092',
        'client.id': socket.gethostname()}
    producer = Producer(conf)
    topic='movie-events'
    producer.produce(topic, key=str(uuid.uuid4()), value=message)
    producer.flush()
    readtopic(topic)
    return '{\"status\": \"success\"}', 201

@app.route('/api/events/user', methods=['POST'])
def user():
    massage=json.dumps(request.json)
    message=massage.encode('utf-8')
    conf = {'bootstrap.servers': 'kafka:9092',
        'client.id': socket.gethostname()}
    producer = Producer(conf)
    topic='user-events'
    producer.produce(topic, key=str(uuid.uuid4()), value=message)
    producer.flush()
    readtopic(topic)
    return '{\"status\": \"success\"}', 201

@app.route('/api/events/payment', methods=['POST'])
def payment():
    massage=json.dumps(request.json)
    message=massage.encode('utf-8')
    conf = {'bootstrap.servers': 'kafka:9092',
        'client.id': socket.gethostname()}
    producer = Producer(conf)
    topic='payment-events'
    producer.produce(topic, key=str(uuid.uuid4()), value=message)
    producer.flush()
    red=True
    while red==True:
        red=readtopic(topic)
    return '{\"status\": \"success\"}', 201


def readtopic(topic):
    conf = {'bootstrap.servers': 'kafka:9092',
        'group.id': 'Demo',
        'enable.auto.commit': 'true',
        'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    gotsmthn=False
    try:
        consumer.subscribe([topic])
        for i in range(5):
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                    logging.error('%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                logging.warning(msg.value().decode('utf-8'))
                gotsmthn=True
    finally:
        consumer.close()
    return gotsmthn


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8082)
