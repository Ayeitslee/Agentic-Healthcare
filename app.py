from flask import Flask, request, jsonify
import json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# Load the "Living Policy" from rules.json
def load_rules():
    with open('rules.json', 'r') as f:
        return json.load(f)

@app.route('/validate_claim', methods=['POST'])
def validate_claim():
    # 1. Generate the correct Eastern Time timestamp
    eastern = ZoneInfo("America/New_York")
    timestamp = datetime.now(eastern).isoformat()
    
    data = request.json
    rules = load_rules()
    payer = data.get('payer')
    procedure_code = data.get('procedure_code')
    auth_id = data.get('auth_id')
    
    # Deterministic Execution: Match procedure against payer rules
    payer_rules = rules['payer_contracts'].get(payer, {})
    required_auths = [r['code'] for r in payer_rules.get('prior_authorization_required', [])]
    
    status = "Approved"
    reason = "All compliance checks passed."
    
    if procedure_code in required_auths and not auth_id:
        status = "Flagged"
        reason = f"Deterministic Rule Violation: Prior Authorization Required for code {procedure_code}."

    # 2. Audit Defensibility: Log the decision sequence
    log_entry = {
        "timestamp": timestamp, # Using the variable defined above
        "input": data,
        "result": status,
        "reasoning_steps": reason
    }
    
    # Open and write the log
    with open('audit_log.json', 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

    # 3. Return the response (Make sure this is NOT indented inside the 'with' block)
    return jsonify({
        "status": status, 
        "reason": reason,
        "timestamp": timestamp
    })

@app.route('/')
def home():
    return "Gatekeeper API is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)