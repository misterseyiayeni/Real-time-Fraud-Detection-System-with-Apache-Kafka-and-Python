# Install faker library via Windows terminal (pip install faker)
# Import packages
from faker import Faker
import random
from uuid import uuid4


# Enforce PCI-DSS compliance
def truncate_card_number(card_number):
    # Check if the card number is a valid string
    if not isinstance(card_number, str):
        return "Invalid card number"
    # Check if the card number is 16 digits long
    # if len(card_number) != 16:
    #     return "Invalid card number"
    # Keep the first six and the last four digits
    first_six = card_number[:6]
    last_four = card_number[-4:]
    # Replace the middle six digits with asterisks
    masked = first_six + "******" + last_four
    # Return the truncated card number
    return masked


# Generate 10 sample transactions with a timestamp, a randomly generated credit card number, and a random amount.
fake = Faker()


def generate_transaction():
    # Generate a random customer_id of 8 digits
    customer_id = "".join([str(random.randint(0, 9)) for _ in range(9)])
    return {
        "transaction_id": str(uuid4()),
        "timestamp": fake.date_time_this_month().strftime("%Y-%m-%d %H:%M:%S"),
        "card_number": truncate_card_number(fake.credit_card_number()),
        "amount": round(random.uniform(1, 10000), 2),
        # Add the customer_id to the dictionary
        "customer_id": customer_id
    }