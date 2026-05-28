import sqlite3
import json
from typing import Dict, Any, List
import os

DB_PATH = "memory.db"

class LongTermMemory:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                client_id TEXT,
                report_summary TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                client_id TEXT,
                transaction_id TEXT,
                reason TEXT,
                severity TEXT,
                is_approved BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def save_session_report(self, session_id: str, client_id: str, report_summary: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sessions (session_id, client_id, report_summary) VALUES (?, ?, ?)',
            (session_id, client_id, report_summary)
        )
        conn.commit()
        conn.close()

    def save_anomalies(self, session_id: str, client_id: str, anomalies: List[Dict[str, Any]]):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for anomaly in anomalies:
            cursor.execute('''
                INSERT INTO anomalies (session_id, client_id, transaction_id, reason, severity, is_approved)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session_id, client_id, anomaly.get('transaction_id'), anomaly.get('reason'), 
                  anomaly.get('severity'), anomaly.get('is_approved')))
        conn.commit()
        conn.close()
        
    def get_client_history(self, client_id: str) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT session_id, report_summary, timestamp FROM sessions WHERE client_id = ? ORDER BY timestamp DESC', (client_id,))
        rows = cursor.fetchall()
        conn.close()
        return [{"session_id": row[0], "report_summary": row[1], "timestamp": row[2]} for row in rows]

long_term_store = LongTermMemory()
