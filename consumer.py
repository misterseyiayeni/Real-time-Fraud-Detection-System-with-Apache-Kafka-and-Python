from kafka import KafkaConsumer
import json
from sklearn.ensemble import IsolationForest
from producer import producer
# Import the smtplib module for sending emails
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# Install scikit-learn in Windows terminal(pip install scikit-learn)

# We need to define the machine learning model that we will be using to detect fraudulent transactions. We will be
# using an unsupervised anomaly detection algorithm called Isolation Forest. Defining the machine learning model We
# are using the default hyperparameters for the IsolationForest algorithm, but you can experiment with different
# hyperparameters to improve the performance of the model.
model = IsolationForest(n_estimators = 100, max_samples = 'auto', contamination = 'auto', random_state = 42)

# Set up a Kafka consumer to receive transaction data from our Kafka cluster
# and apply the machine learning model for fraud detection

# We are using the KafkaConsumer class from the kafka-python library to subscribe to the transactions topic and
# receive transaction data from Kafka. We are also using the json deserializer to deserialize the JSON string back
# into a Python object For each message received from Kafka, we are extracting the transaction data and applying the
# machine learning model to detect fraud. We are using the predict method of the Isolation Forest model to classify
# the transaction as either normal or anomalous. If the model predicts that the transaction is anomalous, we print a
# message indicating that a fraudulent transaction has been detected, along with the details of the transaction.

# Define the details of participants
sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
recipient_email = os.getenv('RECIPIENT_EMAIL_ADDRESS')
sender_password = os.getenv('SENDER_PASSWORD')

# Create an SMTP session with SMTP server
session = smtplib.SMTP_SSL('DOMAIN_NAME_PORT')
# Start the TLS encryption
session.starttls()
# Log into the sender's email account
session.login(sender_email, sender_password)

consumer = KafkaConsumer('transactions', bootstrap_servers = ['localhost:9092'],
                         auto_offset_reset = 'earliest',
                         enable_auto_commit = True,
                         value_deserializer = lambda x: json.loads(x.decode('utf-8')))

for message in consumer:
    transaction = message.value
    amount = transaction['amount']
    transaction_id = transaction.get('transaction_id')
    X_pred = [[amount]]
    model.fit(X_pred)
    y_pred = model.predict(X_pred)
    if y_pred[0] == -1 or transaction['amount'] >= 9000:
        producer.send('fraud-alerts', value = transaction)
        print(f'Fraudulent transaction detected: {transaction}')
        msg = EmailMessage()
        msg['From'] = 'real-time-fraud-detection@any---mail.com'
        msg['To'] = recipient_email
        # Set the subject
        msg['Subject'] = f"Important Notification about Transaction with id {transaction_id}!"
        # Set the message body with the name
        msg.set_content(f"The transaction with id {transaction_id} has been classified as fraudulent. Please review "
                        f"it immediately!")
        # session.send_message(msg)
        print(f'mail for transaction id: {transaction_id} sent')
    else:
        producer.send('legitimate-transactions', value = transaction)
        print(f'This transaction is legitimate: {transaction}')
session.quit()
