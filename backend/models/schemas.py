from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import date

class Portfolio(BaseModel):
    total_value: float
    currency: str
    allocations: Dict[str, float]

class ClientProfile(BaseModel):
    client_id: str
    name: str
    age: int
    email: str
    portfolio: Portfolio
    risk_profile: str
    income: float
    expenses: float
    goals: List[str]

class Transaction(BaseModel):
    id: str
    date: str
    type: str
    amount: float
    category: str
    description: str

class Anomaly(BaseModel):
    transaction_id: str
    reason: str
    severity: str 
    is_approved: Optional[bool] = None

class AnalysisResult(BaseModel):
    client_id: str
    anomalies: List[Anomaly]
    risk_score: int 
    metrics: Dict[str, Any]

class AdvisoryReport(BaseModel):
    client_id: str
    summary: str
    action_items: List[str]
    anomalies_flagged: int
    portfolio_health_score: int

class HitlReviewRequest(BaseModel):
    session_id: str
    client_id: str
    anomalies: List[Anomaly]

class HitlReviewDecision(BaseModel):
    session_id: str
    transaction_id: str
    is_approved: bool
