import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_phantom_detection():
    print("=" * 50)
    print("PHANTOM STOCK DETECTION TEST")
    print("=" * 50)
    
    # Run analysis
    print("\n[1/4] Running agent pipeline...")
    try:
        response = requests.post(f"{BASE_URL}/analysis/run")
        print(f"✓ Pipeline completed: {response.json()['status']}")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return
    
    # Check risk scores
    print("\n[2/4] Checking risk scores...")
    response = requests.get(f"{BASE_URL}/risk-scores")
    data = response.json()
    critical = data['summary']['critical']
    warning = data['summary']['warning']
    normal = data['summary']['normal']
    print(f"✓ Critical: {critical} | Warning: {warning} | Normal: {normal}")
    
    # Check predicted stock
    print("\n[3/4] Analyzing stock deviations...")
    response = requests.get(f"{BASE_URL}/predicted-stock")
    data = response.json()
    high_deviations = [s for s in data['predicted_stock'] 
                       if abs(s['deviation_percentage']) > 30]
    print(f"✓ High deviations (>30%): {len(high_deviations)}")
    
    if high_deviations:
        print("\n  Suppliers with high deviations:")
        for s in high_deviations:
            print(f"    - {s['supplier_name']}: {s['deviation_percentage']:.1f}% "
                  f"({s['deviation']:,} units)")
    
    # Check alerts
    print("\n[4/4] Checking alerts...")
    response = requests.get(f"{BASE_URL}/alerts")
    data = response.json()
    phantom_alerts = [a for a in data['alerts'] 
                      if 'phantom' in a['message'].lower()]
    print(f"✓ Phantom stock alerts: {len(phantom_alerts)}")
    
    # Summary
    print("\n" + "=" * 50)
    print("DETECTION SUMMARY")
    print("=" * 50)
    print(f"Critical Suppliers: {critical}")
    print(f"Warning Suppliers: {warning}")
    print(f"Normal Suppliers: {normal}")
    print(f"High Deviations: {len(high_deviations)}")
    print(f"Phantom Alerts: {len(phantom_alerts)}")
    
    if critical > 0 or len(phantom_alerts) > 0:
        print("\n✅ PHANTOM STOCK DETECTED!")
        print("\nAffected Suppliers:")
        for alert in phantom_alerts:
            print(f"  - {alert['supplier_name']}: {alert['message']}")
    else:
        print("\n✓ No phantom stock detected (all suppliers normal)")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_phantom_detection()
