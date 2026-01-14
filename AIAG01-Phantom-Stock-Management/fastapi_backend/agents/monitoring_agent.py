"""
Supply Monitoring Agent - Data validation and quality checks
"""
from datetime import datetime
from typing import Dict, List

def monitoring_agent(inventory_data: List[Dict]) -> Dict:
    processed_data = []
    anomalies = []
    
    for record in inventory_data:
        quality_issues = []
        
        if record["reported_stock"] < 0:
            quality_issues.append("negative_stock")
        
        if record["production_rate"] <= 0:
            quality_issues.append("invalid_production_rate")
        
        if quality_issues:
            anomalies.append({
                "supplier_id": record["supplier_id"],
                "issues": quality_issues,
                "severity": "high"
            })
        
        processed_record = {
            **record,
            "monitored_at": datetime.now().isoformat(),
            "data_quality": "poor" if quality_issues else "good",
            "quality_issues": quality_issues
        }
        
        processed_data.append(processed_record)
    
    return {
        "agent": "Supply Monitoring Agent",
        "processed_data": processed_data,
        "anomalies": anomalies,
        "total_records": len(processed_data),
        "anomaly_count": len(anomalies)
    }
