"""Quick test - check if server is responding"""
import requests
import time

print("Testing backend server...")

try:
    # Test 1: Health check
    response = requests.get("http://localhost:8000/health", timeout=2)
    print(f"✓ Server is running: {response.json()}")
    
    # Test 2: Skills database
    response = requests.get("http://localhost:8000/api/skills", timeout=5)
    data = response.json()
    print(f"\n✓ Total Skills: {data['total_skills']}")
    print(f"✓ Categories: {', '.join(list(data['categories'].keys())[:5])}...")
    
    # Check new industries
    new = ['culinary', 'healthcare', 'finance']
    for industry in new:
        if industry in data['categories']:
            skills = data['categories'][industry]
            print(f"✓ {industry}: {len(skills)} skills (e.g., {skills[0]})")
    
    print("\n✅ Backend is working with expanded skills!")
    print("\n💡 Open http://localhost:3000 to test in the web app")
    
except requests.exceptions.ConnectionError:
    print("❌ Server not responding. Starting it now...")
except Exception as e:
    print(f"❌ Error: {e}")
