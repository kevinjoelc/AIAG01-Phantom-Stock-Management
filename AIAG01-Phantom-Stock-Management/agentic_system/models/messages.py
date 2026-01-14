"""
Agent Communication Models
Defines input/output contracts for agent communication
"""
from typing import List, Dict, Optional
from datetime import datetime

class AgentMessage:
    """Base message for agent communication"""
    def __init__(self, sender: str, data: Dict, metadata: Optional[Dict] = None):
        self.sender = sender
        self.data = data
        self.metadata = metadata or {}
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "sender": self.sender,
            "data": self.data,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }

class MonitoringOutput(AgentMessage):
    """Output from Monitoring Agent"""
    def __init__(self, processed_data: List[Dict], anomalies: List[Dict], stats: Dict):
        super().__init__(
            sender="MonitoringAgent",
            data={
                "processed_data": processed_data,
                "anomalies": anomalies
            },
            metadata=stats
        )

class ValidationOutput(AgentMessage):
    """Output from Validation Agent"""
    def __init__(self, validations: List[Dict], high_deviations: List[Dict], stats: Dict):
        super().__init__(
            sender="ValidationAgent",
            data={
                "validations": validations,
                "high_deviations": high_deviations
            },
            metadata=stats
        )

class RiskOutput(AgentMessage):
    """Output from Risk Agent"""
    def __init__(self, risk_assessments: List[Dict], critical_risks: List[Dict], 
                 warnings: List[Dict], stats: Dict):
        super().__init__(
            sender="RiskAgent",
            data={
                "risk_assessments": risk_assessments,
                "critical_risks": critical_risks,
                "warnings": warnings
            },
            metadata=stats
        )

class SupervisorOutput(AgentMessage):
    """Output from Supervisor Agent"""
    def __init__(self, alerts: List[Dict], recommendations: List[Dict], 
                 decision: str, stats: Dict):
        super().__init__(
            sender="SupervisorAgent",
            data={
                "alerts": alerts,
                "recommendations": recommendations,
                "decision": decision
            },
            metadata=stats
        )
