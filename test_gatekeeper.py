import requests
import json

# The URL of your live Flask server
URL = "http://127.0.0.1:5001/validate_claim"

def run_test(claim_data, description):
    print(f"--- Testing: {description} ---")
    response = requests.post(URL, json=claim_data)
    result = response.json()
    print(f"Status: {result['status']}")
    print(f"Reason: {result['reason']}\n")

# Scenario A: Valid Claim (No Authorization Required)
claim_a = {
    "payer": "BlueShield",
    "procedure_code": "99213",  # Standard Office Visit
    "patient_name": "John Doe"
}

# Scenario B: Violation Claim (CT Scan Missing Auth ID)
# Based on your rules.json, code 70450 requires an Auth ID
claim_b = {
    "payer": "BlueShield",
    "procedure_code": "70450", 
    "patient_name": "Jane Smith"
    # missing auth_id!
}

if __name__ == "__main__":
    run_test(claim_a, "Standard claim with no special requirements")
    run_test(claim_b, "CT Scan claim missing required Prior Authorization")
