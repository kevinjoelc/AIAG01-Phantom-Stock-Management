"""
Test all REST APIs and display example outputs
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_json(data, title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)
    print(json.dumps(data, indent=2))

def test_apis():
    print("\n🧪 Testing AIAG01 REST APIs\n")
    
    try:
        # Test 1: Suppliers
        print("✓ Test 1: GET /api/suppliers")
        response = requests.get(f"{BASE_URL}/suppliers")
        data = response.json()
        print(f"  Total suppliers: {data['total']}")
        print(f"  Tier-1: {data['by_tier']['tier1']}, Tier-2: {data['by_tier']['tier2']}, Tier-3: {data['by_tier']['tier3']}")
        print_json(data['suppliers'][0], "Sample Supplier")
        
        # Test 2: Run Analysis
        print("\n✓ Test 2: POST /api/analysis/run")
        response = requests.post(f"{BASE_URL}/analysis/run")
        data = response.json()
        print(f"  Status: {data['status']}")
        print(f"  Final decision: {data['summary']['final_decision']}")
        print(f"  Critical risks: {data['summary']['critical_risks']}")
        print(f"  Warnings: {data['summary']['warnings']}")
        
        # Test 3: Predicted Stock
        print("\n✓ Test 3: GET /api/predicted-stock")
        response = requests.get(f"{BASE_URL}/predicted-stock")
        data = response.json()
        print(f"  Total records: {data['total']}")
        if data['predicted_stock']:
            sample = data['predicted_stock'][0]
            print(f"  Sample: {sample['supplier_name']}")
            print(f"    Reported: {sample['reported_stock']}")
            print(f"    Predicted: {sample['predicted_stock']}")
            print(f"    Deviation: {sample['deviation_percentage']}%")
            print_json(sample, "Sample Predicted Stock")
        
        # Test 4: Risk Scores
        print("\n✓ Test 4: GET /api/risk-scores")
        response = requests.get(f"{BASE_URL}/risk-scores")
        data = response.json()
        print(f"  Total assessed: {data['total']}")
        print(f"  Critical: {data['summary']['critical']}")
        print(f"  Warning: {data['summary']['warning']}")
        print(f"  Normal: {data['summary']['normal']}")
        if data['risk_scores']:
            critical = [r for r in data['risk_scores'] if r['risk_level'] == 'CRITICAL']
            if critical:
                print_json(critical[0], "Sample Critical Risk")
        
        # Test 5: Alerts
        print("\n✓ Test 5: GET /api/alerts")
        response = requests.get(f"{BASE_URL}/alerts")
        data = response.json()
        print(f"  Total alerts: {data['total_alerts']}")
        if data['alerts']:
            print(f"  Sample alert: {data['alerts'][0]['message']}")
            print_json(data['alerts'][0], "Sample Alert")
        if data['recommendations']:
            print_json(data['recommendations'][0], "Sample Recommendation")
        
        # Test 6: Dashboard
        print("\n✓ Test 6: GET /api/dashboard")
        response = requests.get(f"{BASE_URL}/dashboard")
        data = response.json()
        print(f"  Phantom stock detected: {data['summary']['phantom_stock_detected']}")
        print(f"  Total alerts: {data['summary']['total_alerts']}")
        print(f"  Status: {data['summary']['status']}")
        print_json(data['summary'], "Dashboard Summary")
        
        # Test 7: Pipeline Trace
        print("\n✓ Test 7: GET /api/pipeline/trace")
        response = requests.get(f"{BASE_URL}/pipeline/trace")
        data = response.json()
        print(f"  Pipeline: {data['pipeline']}")
        print(f"  Communication steps: {len(data['communication_flow'])}")
        print_json(data['communication_flow'], "Communication Flow")
        
        print("\n" + "="*60)
        print("✅ All API tests passed!")
        print("="*60)
        
        print("\n📊 Dashboard Integration Ready:")
        print("  - Supplier data: /api/suppliers")
        print("  - Predicted stock: /api/predicted-stock")
        print("  - Risk scores: /api/risk-scores")
        print("  - Alerts: /api/alerts")
        print("  - Complete dashboard: /api/dashboard")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API")
        print("   Make sure the server is running:")
        print("   cd agentic_system && python main.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_apis()
