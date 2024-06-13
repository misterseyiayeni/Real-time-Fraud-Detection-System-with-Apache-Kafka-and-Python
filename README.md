# Real-Time Fraud Detection System

This system uses Apache Kafka to generate a stream of PCI-DSS-compliant dummy credit card numbers and feeds the stream into a isolation forest (anomaly detection) machine learning model to determine if there is an anomaly or not.

If any transaction is flagged, a mail is created and sent to the monitoring team immediately while further action is taken (e.g. keep the transaction in pending status) in the meantime.
