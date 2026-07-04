from flask import Flask, request, jsonify
import json
import datetime

app = Flask(__name__)

# Load the "Living Policy" from rules.json
def load_rules():
    with open('rules.json', 'r') as f:
        return json.load(f)

@app.route('/validate_claim', methods=['POST'])
def validate_claim():
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

    # Audit Defensibility: Log the decision sequence
    log_entry = {
        "timestamp": str(datetime.datetime.now()),
        "input": data,
        "result": status,
        "reasoning_steps": reason
    }
    with open('audit_log.json', 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

    return jsonify({"status": status, "reason": reason})

if __name__ == '__main__':
    app.run(debug=True)
