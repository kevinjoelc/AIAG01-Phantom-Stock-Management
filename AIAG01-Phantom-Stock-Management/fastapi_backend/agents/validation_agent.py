"""
Validation Agent - Predicts expected inventory and detects deviations
"""
from typing import Dict, List

def validation_agent(processed_data: List[Dict]) -> Dict:
    validations = []
    high_deviations = []
    deviation_threshold = 0.20
    
    for record in processed_data:
        if record.get("data_quality") == "poor":
            continue
        
        reported = record["reported_stock"]
        expected = record.get("expected_stock", 0)
        
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
        
        if deviation > deviation_threshold:
            validation_result["flag"] = "high_deviation"
            validation_result["escalate"] = True
            high_deviations.append(validation_result)
        else:
            validation_result["flag"] = "normal"
            validation_result["escalate"] = False
        
        validations.append(validation_result)
    
    return {
        "agent": "Validation Agent",
        "validations": validations,
        "high_deviations": high_deviations,
        "total_validated": len(validations),
        "high_deviation_count": len(high_deviations)
    }
