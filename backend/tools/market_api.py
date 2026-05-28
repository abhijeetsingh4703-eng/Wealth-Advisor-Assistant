import random

def get_market_benchmark(asset_class: str) -> float:
    """Mock API to return YTD market benchmarks"""
    benchmarks = {
        "equities": 0.085, 
        "bonds": 0.021,    
        "real_estate": 0.045, 
        "cash": 0.015      
    }
    
    base_return = benchmarks.get(asset_class, 0.0)
    return round(base_return + random.uniform(-0.01, 0.01), 3)

def get_risk_free_rate() -> float:
    return 0.042 
