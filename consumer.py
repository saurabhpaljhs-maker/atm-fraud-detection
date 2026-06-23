import json
import time
from google.cloud import pubsub_v1
from google.cloud import bigquery
from google.auth import default
from fraud_detector import FraudDetector

credentials, project_id = default()
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
bq_client = bigquery.Client(credentials=credentials, project=project_id)
fraud_detector = FraudDetector()

subscription_path = subscriber.subscription_path(project_id, "atm-transactions-sub")
table_id = f"{project_id}.fraud_detection.transactions"

def process_message(message):
    """Har message ko process karo"""
    try:
        transaction = json.loads(message.data.decode("utf-8"))
        
        # Fraud check
        fraud_result = fraud_detector.detect_fraud(transaction)
        
        # BigQuery me insert karo
        row = {
            "card_id": transaction["card_id"],
            "amount": transaction["amount"],
            "location": transaction["location"],
            "atm_id": transaction["atm_id"],
            "timestamp": transaction["timestamp"],
            "is_fraud": fraud_result["is_fraud"],
            "flags": ",".join(fraud_result["flags"]),
            "risk_score": fraud_result["risk_score"]
        }
        
        errors = bq_client.insert_rows_json(table_id, [row])
        
        if fraud_result["is_fraud"]:
            print(f"🚨 FRAUD DETECTED: {transaction['card_id']} - Flags: {fraud_result['flags']}")
        else:
            print(f"✅ Transaction OK: {transaction['card_id']}")
        
        message.ack()
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()

if __name__ == "__main__":
    print(f"Listening to {subscription_path}...")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_message)
    
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
