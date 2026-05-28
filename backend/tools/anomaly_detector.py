import numpy as np
from typing import List, Dict, Any

def detect_anomalies(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect statistical outliers and rule-based anomalies in transactions.
    """
    if not transactions:
        return []

    anomalies = []
    
    withdrawals = [t for t in transactions if t["type"] == "withdrawal"]
    if len(withdrawals) >= 3:
        amounts = [t["amount"] for t in withdrawals]
        mean_amt = np.mean(amounts)
        std_amt = np.std(amounts)
        
        for txn in withdrawals:
            if std_amt > 0:
                z_score = (txn["amount"] - mean_amt) / std_amt
                if z_score > 2.5: 
                    anomalies.append({
                        "transaction_id": txn["id"],
                        "reason": f"Statistical outlier: Amount {txn['amount']} is unusually high compared to typical withdrawals (Z={z_score:.2f})",
                        "severity": "high",
                        "is_approved": None
                    })

    for txn in transactions:
        if any(a["transaction_id"] == txn["id"] for a in anomalies):
            continue
            
        if txn["amount"] > 100000:
             anomalies.append({
                        "transaction_id": txn["id"],
                        "reason": f"Large movement rule: Transaction amount {txn['amount']} exceeds $100k threshold.",
                        "severity": "medium",
                        "is_approved": None
             })
            
        suspicious_categories = ["crypto", "unknown", "offshore"]
        if txn.get("category", "").lower() in suspicious_categories:
            anomalies.append({
                        "transaction_id": txn["id"],
                        "reason": f"High-risk category: Transaction flagged for category '{txn['category']}'.",
                        "severity": "high",
                        "is_approved": None
            })

    return anomalies
