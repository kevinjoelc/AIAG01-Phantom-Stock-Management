"""
Test script to verify AIAG01 system functionality
Run this to ensure everything works before demo
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.supplier_simulator import SupplierSimulator
from agents.supply_monitoring_agent import SupplyMonitoringAgent
from agents.validation_agent import ValidationAgent
from agents.risk_analysis_agent import RiskAnalysisAgent
from agents.supervisor_agent import SupervisorAgent

def test_system():
    print("🧪 Testing AIAG01 Phantom Stock Management System\n")
    
    # Test 1: Simulator
    print("✓ Test 1: Supplier Simulator")
    simulator = SupplierSimulator()
    suppliers = simulator.get_all_suppliers()
    print(f"  Generated {len(suppliers)} suppliers")
    assert len(suppliers) == 8, "Should have 8 suppliers"
    
    # Test 2: Inventory Data
    print("✓ Test 2: Inventory Data Generation")
    inventory_data = simulator.generate_inventory_data(days_back=10)
    print(f"  Generated {len(inventory_data)} inventory records")
    assert len(inventory_data) > 0, "Should have inventory data"
    
    # Test 3: Supply Monitoring Agent
    print("✓ Test 3: Supply Monitoring Agent")
    monitoring_agent = SupplyMonitoringAgent()
    monitoring_output = monitoring_agent.process_inventory_data(inventory_data)
    print(f"  Processed {monitoring_output['total_records']} records")
    print(f"  Found {monitoring_output['anomaly_count']} anomalies")
    
    # Test 4: Validation Agent
    print("✓ Test 4: Validation Agent")
    validation_agent = ValidationAgent()
    validation_output = validation_agent.validate_inventory(monitoring_output["processed_data"])
    print(f"  Validated {validation_output['total_validated']} records")
    print(f"  Found {validation_output['high_deviation_count']} high deviations")
    
    # Test 5: Risk Analysis Agent
    print("✓ Test 5: Risk Analysis Agent")
    risk_agent = RiskAnalysisAgent()
    risk_output = risk_agent.analyze_risks(validation_output["validations"])
    print(f"  Assessed {risk_output['total_assessed']} risks")
    print(f"  Critical: {risk_output['critical_count']}, Warnings: {risk_output['warning_count']}")
    
    # Test 6: Supervisor Agent
    print("✓ Test 6: Supervisor Agent")
    supervisor_agent = SupervisorAgent()
    supervisor_output = supervisor_agent.verify_and_decide(risk_output, monitoring_output)
    print(f"  Generated {supervisor_output['total_alerts']} alerts")
    print(f"  Critical alerts: {supervisor_output['critical_alerts']}")
    
    # Test 7: Full Pipeline
    print("✓ Test 7: Full Agent Pipeline")
    summary = supervisor_agent.generate_summary({
        "monitoring": monitoring_output,
        "validation": validation_output,
        "risk_analysis": risk_output,
        "supervisor": supervisor_output
    })
    print(f"  Status: {summary['summary']['status']}")
    print(f"  Phantom stock detected: {summary['summary']['phantom_stock_detected']}")
    
    print("\n✅ All tests passed! System is ready for demo.\n")
    
    # Display sample alert
    if supervisor_output['alerts']:
        print("📋 Sample Alert:")
        alert = supervisor_output['alerts'][0]
        print(f"  Severity: {alert['severity']}")
        print(f"  Message: {alert['message']}")
        if 'risk_score' in alert:
            print(f"  Risk Score: {alert['risk_score']}")
    
    print("\n🚀 Ready to run: python backend/app.py")

if __name__ == "__main__":
    try:
        test_system()
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
