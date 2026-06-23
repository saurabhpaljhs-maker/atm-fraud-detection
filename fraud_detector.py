from datetime import datetime, timedelta
from collections import defaultdict

class FraudDetector:
    def __init__(self):
        self.transaction_history = defaultdict(list)  # card_id -> [transactions]
        self.velocity_threshold = 3  # 3 transactions in 5 minutes = suspicious
        self.amount_threshold = 25000  # 25k INR per transaction
        self.location_jump_minutes = 2  # Same card 2 ATMs in 2 min = fraud
    
    def check_velocity(self, card_id, timestamp):
        """Same card se 5 min me 3 se zyada transactions?"""
        now = datetime.fromisoformat(timestamp)
        recent = [
            t for t in self.transaction_history[card_id]
            if now - datetime.fromisoformat(t["timestamp"]) < timedelta(minutes=5)
        ]
        return len(recent) >= self.velocity_threshold
    
    def check_location_jump(self, card_id, location, timestamp):
        """Same card 2 locations me 2 min ke andar?"""
        now = datetime.fromisoformat(timestamp)
        for prev_txn in self.transaction_history[card_id]:
            prev_time = datetime.fromisoformat(prev_txn["timestamp"])
            time_diff = (now - prev_time).total_seconds() / 60
            
            if time_diff < self.location_jump_minutes and prev_txn["location"] != location:
                return True
        return False
    
    def check_amount_threshold(self, amount):
        """Amount 25k se zyada?"""
        return amount > self.amount_threshold
    
    def detect_fraud(self, transaction):
        """Main detection logic"""
        flags = []
        
        if self.check_velocity(transaction["card_id"], transaction["timestamp"]):
            flags.append("VELOCITY_CHECK")
        
        if self.check_location_jump(transaction["card_id"], transaction["location"], transaction["timestamp"]):
            flags.append("LOCATION_JUMP")
        
        if self.check_amount_threshold(transaction["amount"]):
            flags.append("HIGH_AMOUNT")
        
        # Store transaction in history
        self.transaction_history[transaction["card_id"]].append(transaction)
        
        return {
            "is_fraud": len(flags) > 0,
            "flags": flags,
            "risk_score": len(flags) / 3.0  # 0-1 score
        }
