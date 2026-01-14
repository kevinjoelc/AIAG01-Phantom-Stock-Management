"""
Validation Agent
Predicts expected inventory levels and detects deviations
"""
from typing import Dict, List
import statistics

class ValidationAgent:
    def __init__(self):
        self.name = "Validation Agent"
        self.role = "Predictive Validator"
        self.deviation_threshold = 0.20  # 20% deviation triggers escalation
        
    def predict_expected_inventory(self, inventory_record: Dict) -> Dict:
        """
        Predict what inventory should exist based on production and consumption
        """
        production_rate = inventory_record.get("production_rate", 0)
        consumption_rate = inventory_record.get("consumption_rate", 0)
        
        # Simple prediction model (can be enhanced with ML)
        expected_stock = production_rate - consumption_rate
        
        # Add historical baseline if available
        if "expected_stock" in inventory_record:
            expected_stock = inventory_record["expected_stock"]
        
        return {
            "supplier_id": inventory_record["supplier_id"],
            "predicted_stock": max(0, expected_stock),
            "production_rate": production_rate,
            "consumption_rate": consumption_rate
        }
    
    def validate_inventory(self, processed_data: List[Dict]) -> Dict:
        """
        Compare reported vs predicted inventory
        """
        validations = []
        high_deviations = []
        
        for record in processed_data:
            if record.get("data_quality") == "poor":
                continue  # Skip poor quality data
            
            reported = record["reported_stock"]
            expected = record.get("expected_stock", 0)
            
            # Calculate deviation
            if expected > 0:
                deviation = abs(reported - expected) / expected
            else:
                deviation = 0
            
            validation_result = {
                "supplier_id": record["supplier_id"],
                "supplier_name": record["supplier_name"],
                "tier": record["tier"],
                "reported_stock": reported,
                "expected_stock": expected,
                "deviation": round(deviation, 3),
                "deviation_percentage": round(deviation * 100, 2)
            }
            
            # Flag high deviations
            if deviation > self.deviation_threshold:
                validation_result["flag"] = "high_deviation"
                validation_result["escalate"] = True
                high_deviations.append(validation_result)
            else:
                validation_result["flag"] = "normal"
                validation_result["escalate"] = False
            
            validations.append(validation_result)
        
        return {
            "agent": self.name,
            "validations": validations,
            "high_deviations": high_deviations,
            "total_validated": len(validations),
            "high_deviation_count": len(high_deviations)
        }
    
    def get_reasoning(self) -> str:
        """Return agent's reasoning process"""
        return """
        Validation Agent Reasoning:
        1. Calculate expected inventory: production_rate - consumption_rate
        2. Compare reported vs expected inventory
        3. Calculate deviation percentage
        4. If deviation > 20%, flag as high_deviation
        5. Escalate high deviations to Risk Analysis Agent
        6. Pass all validations for risk scoring
        """
