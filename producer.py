from kafka import KafkaProducer
import json
from initializer import generate_transaction

# We are using the json serializer to serialize the transaction data as a JSON string before sending it to Kafka.
# We are also flushing the producer to make sure that all the messages have been sent to Kafka before moving forward.

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: json.dumps(x).encode('utf-8'))

for i in range(100):
    transaction = generate_transaction()
    producer.send('transactions', value=transaction)
    print(generate_transaction())

producer.flush()

# while True:
#     try:
#         transaction = generate_transaction()
#         producer.send('transactions', value=transaction)
#     except KeyboardInterrupt:
#         break