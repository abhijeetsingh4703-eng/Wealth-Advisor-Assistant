import json
import os
from typing import Dict, Any, List

def get_client_profile(client_id: str) -> Dict[str, Any]:
    """Mock CRM API to fetch client profile"""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "mock_data", "clients.json")
    
    with open(file_path, "r") as f:
        clients = json.load(f)
        
    for client in clients:
        if client["client_id"] == client_id:
            return client
    raise ValueError(f"Client {client_id} not found in CRM")

def get_client_transactions(client_id: str) -> List[Dict[str, Any]]:
     """Mock API to fetch client transaction history"""
     base_dir = os.path.dirname(os.path.dirname(__file__))
     file_path = os.path.join(base_dir, "mock_data", "transactions.json")
     
     with open(file_path, "r") as f:
         transactions = json.load(f)
         
     if client_id in transactions:
         return transactions[client_id]
     return []
