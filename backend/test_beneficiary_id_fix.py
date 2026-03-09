#!/usr/bin/env python3
"""
Test script to verify beneficiary_id fix
Run this after deploying the backend changes
"""

import requests
import json

# Configuration
API_BASE_URL = "https://tq8jtogxth.execute-api.ap-south-1.amazonaws.com/prod"
# You'll need a valid token for authenticated endpoints
AUTH_TOKEN = "your-auth-token-here"

def test_get_complaints():
    """Test GET /api/v1/complaints"""
    print("\n" + "="*60)
    print("TEST 1: GET /api/v1/complaints")
    print("="*60)
    
    url = f"{API_BASE_URL}/api/v1/complaints"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        complaints = response.json()
        print(f"Total Complaints: {len(complaints)}")
        
        # Check if all complaints have beneficiary_id
        missing_count = 0
        for complaint in complaints:
            if not complaint.get('beneficiary_id') or complaint.get('beneficiary_id') == 'N/A':
                missing_count += 1
                print(f"  ❌ Missing beneficiary_id: {complaint.get('complaint_id')}")
            else:
                print(f"  ✅ {complaint.get('complaint_id')}: {complaint.get('beneficiary_id')}")
        
        if missing_count == 0:
            print("\n✅ SUCCESS: All complaints have valid beneficiary_id")
        else:
            print(f"\n⚠️  WARNING: {missing_count} complaints missing beneficiary_id")
    else:
        print(f"❌ FAILED: {response.text}")

def test_create_complaint_with_beneficiary():
    """Test POST /create-complaint with beneficiary_id"""
    print("\n" + "="*60)
    print("TEST 2: POST /create-complaint (with beneficiary_id)")
    print("="*60)
    
    url = f"{API_BASE_URL}/create-complaint"
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    params = {
        "beneficiary_id": "BEN-TEST-001",
        "description": "Test complaint with beneficiary ID"
    }
    
    response = requests.post(url, headers=headers, params=params)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        if result.get('beneficiary_id') == 'BEN-TEST-001':
            print("\n✅ SUCCESS: Beneficiary ID stored correctly")
        else:
            print(f"\n❌ FAILED: Expected BEN-TEST-001, got {result.get('beneficiary_id')}")
    else:
        print(f"❌ FAILED: {response.text}")

def test_create_complaint_without_beneficiary():
    """Test POST /create-complaint without beneficiary_id (should auto-generate)"""
    print("\n" + "="*60)
    print("TEST 3: POST /create-complaint (without beneficiary_id)")
    print("="*60)
    
    url = f"{API_BASE_URL}/create-complaint"
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    params = {
        "beneficiary_id": "UNKNOWN",
        "description": "Test complaint without beneficiary ID - should auto-generate"
    }
    
    response = requests.post(url, headers=headers, params=params)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        beneficiary_id = result.get('beneficiary_id')
        if beneficiary_id and beneficiary_id.startswith('BEN-') and beneficiary_id != 'UNKNOWN':
            print(f"\n✅ SUCCESS: Auto-generated beneficiary_id: {beneficiary_id}")
        else:
            print(f"\n❌ FAILED: Invalid beneficiary_id: {beneficiary_id}")
    else:
        print(f"❌ FAILED: {response.text}")

def test_submit_complaint():
    """Test POST /api/v1/complaints"""
    print("\n" + "="*60)
    print("TEST 4: POST /api/v1/complaints (form submission)")
    print("="*60)
    
    url = f"{API_BASE_URL}/api/v1/complaints"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "complaint_type": "duplicate_beneficiary",
        "description": "Test complaint via form submission",
        "subject_beneficiary_id": "",  # Empty - should auto-generate
        "location": {
            "district": "Mumbai",
            "state": "Maharashtra",
            "pincode": "400001"
        },
        "submitter_name": "Test User",
        "submitter_phone": "+919876543210",
        "is_anonymous": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        
        beneficiary_id = result.get('beneficiary_id')
        if beneficiary_id and beneficiary_id.startswith('BEN-'):
            print(f"\n✅ SUCCESS: Auto-generated beneficiary_id: {beneficiary_id}")
        else:
            print(f"\n❌ FAILED: Invalid beneficiary_id: {beneficiary_id}")
    else:
        print(f"❌ FAILED: {response.text}")

def test_health_check():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("TEST 0: Health Check")
    print("="*60)
    
    url = f"{API_BASE_URL}/health"
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("✅ API is healthy")
    else:
        print("❌ API is not responding")

def main():
    print("\n" + "="*60)
    print("BENEFICIARY ID FIX - TEST SUITE")
    print("="*60)
    
    # Test 0: Health check
    test_health_check()
    
    # Test 1: Get all complaints (should all have beneficiary_id)
    test_get_complaints()
    
    # Test 2: Create complaint with beneficiary_id
    # Note: Requires authentication token
    if AUTH_TOKEN != "your-auth-token-here":
        test_create_complaint_with_beneficiary()
        test_create_complaint_without_beneficiary()
        test_submit_complaint()
    else:
        print("\n⚠️  Skipping authenticated tests (no token provided)")
        print("   Set AUTH_TOKEN variable to run authenticated tests")
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
