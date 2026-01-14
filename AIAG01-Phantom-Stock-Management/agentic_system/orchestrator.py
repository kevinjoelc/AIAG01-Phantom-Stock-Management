"""
Agent Orchestrator - Manages agent communication pipeline
"""
from agents.monitoring_agent import MonitoringAgent
from agents.validation_agent import ValidationAgent
from agents.risk_agent import RiskAgent
from agents.supervisor_agent import SupervisorAgent
from models.messages import AgentMessage

class AgentOrchestrator:
    """
    Orchestrates communication between autonomous agents
    
    Pipeline: MonitoringAgent → ValidationAgent → RiskAgent → SupervisorAgent
    """
    
    def __init__(self):
        # Initialize all agents
        self.monitoring_agent = MonitoringAgent()
        self.validation_agent = ValidationAgent()
        self.risk_agent = RiskAgent()
        self.supervisor_agent = SupervisorAgent()
        
        # Store agent outputs for transparency
        self.agent_outputs = {}
    
    def run_pipeline(self, inventory_data: list) -> dict:
        """
        Execute the full agent pipeline
        
        Flow:
        1. Raw data → MonitoringAgent
        2. MonitoringAgent output → ValidationAgent
        3. ValidationAgent output → RiskAgent
        4. RiskAgent output → SupervisorAgent
        5. SupervisorAgent output → Final result
        """
        print("\n" + "="*60)
        print("STARTING AGENTIC PIPELINE")
        print("="*60 + "\n")
        
        # Step 1: MonitoringAgent processes raw data
        print("STEP 1: MonitoringAgent")
        print("-" * 60)
        initial_message = AgentMessage(
            sender="DataSource",
            data={"inventory_data": inventory_data}
        )
        monitoring_output = self.monitoring_agent.execute(initial_message)
        self.agent_outputs["monitoring"] = monitoring_output.to_dict()
        
        # Step 2: ValidationAgent receives MonitoringAgent output
        print("\nSTEP 2: ValidationAgent")
        print("-" * 60)
        validation_output = self.validation_agent.execute(monitoring_output)
        self.agent_outputs["validation"] = validation_output.to_dict()
        
        # Step 3: RiskAgent receives ValidationAgent output
        print("\nSTEP 3: RiskAgent")
        print("-" * 60)
        risk_output = self.risk_agent.execute(validation_output)
        self.agent_outputs["risk"] = risk_output.to_dict()
        
        # Step 4: SupervisorAgent receives RiskAgent output
        print("\nSTEP 4: SupervisorAgent")
        print("-" * 60)
        supervisor_output = self.supervisor_agent.execute(risk_output)
        self.agent_outputs["supervisor"] = supervisor_output.to_dict()
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETE")
        print("="*60 + "\n")
        
        # Return comprehensive result
        return {
            "status": "complete",
            "pipeline": [
                "MonitoringAgent → ValidationAgent → RiskAgent → SupervisorAgent"
            ],
            "agent_outputs": self.agent_outputs,
            "summary": {
                "total_records": monitoring_output.metadata["total_records"],
                "anomalies": monitoring_output.metadata["anomaly_count"],
                "high_deviations": validation_output.metadata["high_deviation_count"],
                "critical_risks": risk_output.metadata["critical_count"],
                "warnings": risk_output.metadata["warning_count"],
                "total_alerts": supervisor_output.metadata["total_alerts"],
                "final_decision": supervisor_output.data["decision"]
            }
        }
    
    def get_agent_reasoning(self) -> dict:
        """Get reasoning from all agents"""
        return {
            "monitoring": self.monitoring_agent.get_reasoning(),
            "validation": self.validation_agent.get_reasoning(),
            "risk": self.risk_agent.get_reasoning(),
            "supervisor": self.supervisor_agent.get_reasoning()
        }
