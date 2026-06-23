import json
import time
import random
from datetime import datetime
from google.cloud import pubsub_v1
from google.auth import default

# GCP credentials auto-load (GOOGLE_APPLICATION_CREDENTIALS env var ya default)
credentials, project_id = default()
publisher = pubsub_v1.PublisherClient(credentials=credentials)
topic_path = publisher.topic_path(project_id, "atm-transactions")

def generate_fake_transaction():
    """Fake ATM transaction generate karo"""
    card_id = f"CARD{random.randint(1000, 9999)}"
    amount = random.choice([500, 1000, 5000, 10000, 50000])  # INR
    location = random.choice(["Delhi", "Mumbai", "Bangalore", "Agra", "Hyderabad"])
    atm_id = f"ATM{random.randint(100, 999)}"
    timestamp = datetime.utcnow().isoformat()
    
    transaction = {
        "card_id": card_id,
        "amount": amount,
        "location": location,
        "atm_id": atm_id,
        "timestamp": timestamp
    }
    return json.dumps(transaction).encode("utf-8")

def publish_transaction(message):
    """Message Pub/Sub me publish karo"""
    future = publisher.publish(topic_path, message)
    print(f"Published: {future.result()}")

if __name__ == "__main__":
    print(f"Publishing transactions to {topic_path}...")
    try:
        while True:
            transaction = generate_fake_transaction()
            publish_transaction(transaction)
            time.sleep(2)  # Every 2 seconds
    except KeyboardInterrupt:
        print("\nStopped.")
