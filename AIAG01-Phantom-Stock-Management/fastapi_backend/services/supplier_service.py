"""
Supplier Service - Multi-tier supplier simulation
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict

class SupplierService:
    def __init__(self):
        self.suppliers = {
            "tier1": [
                {"id": "T1-001", "name": "Tier1 Electronics Inc", "tier": 1, "capacity": 10000, "reliability": 0.95},
                {"id": "T1-002", "name": "Tier1 Components Ltd", "tier": 1, "capacity": 8000, "reliability": 0.90}
            ],
            "tier2": [
                {"id": "T2-001", "name": "Tier2 Parts Co", "tier": 2, "capacity": 5000, "reliability": 0.85},
                {"id": "T2-002", "name": "Tier2 Materials Inc", "tier": 2, "capacity": 6000, "reliability": 0.80},
                {"id": "T2-003", "name": "Tier2 Assembly Corp", "tier": 2, "capacity": 4500, "reliability": 0.88}
            ],
            "tier3": [
                {"id": "T3-001", "name": "Tier3 Raw Materials", "tier": 3, "capacity": 3000, "reliability": 0.75},
                {"id": "T3-002", "name": "Tier3 Metals Ltd", "tier": 3, "capacity": 3500, "reliability": 0.70},
                {"id": "T3-003", "name": "Tier3 Plastics Inc", "tier": 3, "capacity": 2800, "reliability": 0.78}
            ]
        }
    
    def get_all_suppliers(self) -> List[Dict]:
        return [s for tier in self.suppliers.values() for s in tier]
    
    def generate_inventory_data(self, days_back: int = 30) -> List[Dict]:
        inventory_data = []
        for tier_name, suppliers in self.suppliers.items():
            for supplier in suppliers:
                production_rate = supplier["capacity"] * 0.7
                consumption_rate = production_rate * 0.8
                has_phantom_stock = random.random() < 0.3
                
                for day in range(days_back):
                    date = datetime.now() - timedelta(days=day)
                    expected_stock = production_rate - consumption_rate + random.randint(-100, 100)
                    
                    if has_phantom_stock and day < 10:
                        reported_stock = expected_stock * random.uniform(1.3, 1.8)
                    else:
                        reported_stock = expected_stock * random.uniform(0.95, 1.05)
                    
                    inventory_data.append({
                        "supplier_id": supplier["id"],
                        "supplier_name": supplier["name"],
                        "tier": supplier["tier"],
                        "date": date.strftime("%Y-%m-%d"),
                        "reported_stock": max(0, int(reported_stock)),
                        "production_rate": int(production_rate),
                        "consumption_rate": int(consumption_rate),
                        "expected_stock": max(0, int(expected_stock)),
                        "reliability": supplier["reliability"]
                    })
        
        return inventory_data
