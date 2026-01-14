"""
Multi-Tier Supplier Simulation
Generates realistic supplier data with phantom stock scenarios
"""
import random
from datetime import datetime, timedelta
from typing import Dict, List

class SupplierSimulator:
    def __init__(self):
        self.suppliers = self._initialize_suppliers()
        
    def _initialize_suppliers(self) -> Dict:
        return {
            "tier1": [
                {"id": "T1-001", "name": "Tier1 Electronics Inc", "tier": 1, "capacity": 10000, "reliability": 0.95},
                {"id": "T1-002", "name": "Tier1 Components Ltd", "tier": 1, "capacity": 8000, "reliability": 0.90}
            ],
            "tier2": [
                {"id": "T2-001", "name": "Tier2 Parts Co", "tier": 2, "capacity": 5000, "reliability": 0.85, "supplies_to": "T1-001"},
                {"id": "T2-002", "name": "Tier2 Materials Inc", "tier": 2, "capacity": 6000, "reliability": 0.80, "supplies_to": "T1-002"},
                {"id": "T2-003", "name": "Tier2 Assembly Corp", "tier": 2, "capacity": 4500, "reliability": 0.88, "supplies_to": "T1-001"}
            ],
            "tier3": [
                {"id": "T3-001", "name": "Tier3 Raw Materials", "tier": 3, "capacity": 3000, "reliability": 0.75, "supplies_to": "T2-001"},
                {"id": "T3-002", "name": "Tier3 Metals Ltd", "tier": 3, "capacity": 3500, "reliability": 0.70, "supplies_to": "T2-002"},
                {"id": "T3-003", "name": "Tier3 Plastics Inc", "tier": 3, "capacity": 2800, "reliability": 0.78, "supplies_to": "T2-003"}
            ]
        }
    
    def get_all_suppliers(self) -> List[Dict]:
        all_suppliers = []
        for tier in self.suppliers.values():
            all_suppliers.extend(tier)
        return all_suppliers
    
    def generate_inventory_data(self, days_back: int = 30) -> List[Dict]:
        """Generate inventory data with phantom stock scenarios"""
        inventory_data = []
        
        for tier_name, suppliers in self.suppliers.items():
            for supplier in suppliers:
                # Calculate expected inventory based on production
                production_rate = supplier["capacity"] * 0.7  # 70% utilization
                consumption_rate = production_rate * 0.8  # 80% gets consumed
                
                # Simulate phantom stock for some suppliers
                has_phantom_stock = random.random() < 0.3  # 30% chance
                
                for day in range(days_back):
                    date = datetime.now() - timedelta(days=day)
                    
                    # Expected stock calculation
                    expected_stock = production_rate - consumption_rate + random.randint(-100, 100)
                    
                    # Reported stock (with phantom stock scenario)
                    if has_phantom_stock and day < 10:
                        # Report higher than actual (phantom stock)
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
                        "reliability": supplier["reliability"],
                        "has_phantom_stock": has_phantom_stock
                    })
        
        return inventory_data
    
    def generate_shipment_data(self) -> List[Dict]:
        """Generate shipment logs"""
        shipments = []
        
        for tier_name, suppliers in self.suppliers.items():
            for supplier in suppliers:
                # Generate 5-10 recent shipments
                for i in range(random.randint(5, 10)):
                    delay_days = random.randint(0, 14) if random.random() < 0.2 else 0
                    
                    shipments.append({
                        "supplier_id": supplier["id"],
                        "shipment_id": f"SH-{supplier['id']}-{i:03d}",
                        "quantity": random.randint(500, 2000),
                        "scheduled_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                        "actual_date": (datetime.now() - timedelta(days=random.randint(1, 30) - delay_days)).strftime("%Y-%m-%d"),
                        "delay_days": delay_days,
                        "status": "delayed" if delay_days > 0 else "on_time"
                    })
        
        return shipments
