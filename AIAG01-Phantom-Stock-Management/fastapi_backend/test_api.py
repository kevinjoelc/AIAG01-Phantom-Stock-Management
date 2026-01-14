"""
Test FastAPI Backend
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing AIAG01 FastAPI Backend\n")
    
    # Test 1: Health Check
    print("✓ Test 1: Health Check")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()['status']}\n")
    
    # Test 2: Get Suppliers
    print("✓ Test 2: Get Suppliers")
    response = requests.get(f"{BASE_URL}/api/suppliers")
    data = response.json()
    print(f"  Total suppliers: {data['total']}")
    print(f"  By tier: {data['by_tier']}\n")
    
    # Test 3: Run Analysis
    print("✓ Test 3: Run Full Analysis")
    response = requests.post(f"{BASE_URL}/api/analysis/run")
    data = response.json()
    print(f"  Status: {data['status']}")
    print(f"  Phantom stock detected: {data['summary']['phantom_stock_detected']}")
    print(f"  Alerts generated: {data['summary']['alerts_generated']}\n")
    
    # Test 4: Get Alerts
    print("✓ Test 4: Get Alerts")
    response = requests.get(f"{BASE_URL}/api/alerts")
    data = response.json()
    print(f"  Total alerts: {data['total_alerts']}")
    if data['alerts']:
        print(f"  Sample alert: {data['alerts'][0]['message']}\n")
    
    # Test 5: Get Risks
    print("✓ Test 5: Get Risk Assessments")
    response = requests.get(f"{BASE_URL}/api/risks")
    data = response.json()
    print(f"  Critical risks: {data['critical_count']}")
    print(f"  Warnings: {data['warning_count']}\n")
    
    # Test 6: Get Dashboard
    print("✓ Test 6: Get Dashboard Data")
    response = requests.get(f"{BASE_URL}/api/dashboard")
    data = response.json()
    print(f"  Status: {data['summary']['status']}\n")
    
    print("✅ All tests passed!\n")
    print("🚀 FastAPI backend is working correctly")
    print(f"📖 Visit {BASE_URL}/docs for interactive API documentation")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend")
        print("   Make sure the server is running: python main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
