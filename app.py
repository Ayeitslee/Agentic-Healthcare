from flask import Flask, request, jsonify
import json
from datetime import datetime
from zoneinfo import ZoneInfo

app = Flask(__name__)

# Load the Living Policy
def load_rules():
    with open('rules.json', 'r') as f:
        return json.load(f)

@app.route('/validate_claim', methods=['POST'])
def validate_claim():

    eastern = ZoneInfo("America/New_York")
    timestamp = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p %Z")

    data = request.get_json(silent=True)

    if data is None:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    rules = load_rules()

    payer = data.get('payer')
    procedure_code = data.get('procedure_code')
    auth_id = data.get('auth_id')

    payer_rules = rules['payer_contracts'].get(payer, {})
    required_auths = [
        r['code']
        for r in payer_rules.get('prior_authorization_required', [])
    ]

    status = "Approved"
    reason = "All compliance checks passed."

    if procedure_code in required_auths and not auth_id:
        status = "Flagged"
        reason = f"Deterministic Rule Violation: Prior Authorization Required for code {procedure_code}."

    # Audit Log
    log_entry = {
        "timestamp": timestamp,
        "input": data,
        "result": status,
        "reasonings": reason
    }

    with open('audit_log.json', 'a') as f:
        f.write(json.dumps(log_entry) + "\n")

    # Optional console output
    print(f"[{timestamp}] {status} - {payer} - {procedure_code}")

    return jsonify({
        "status": status,
        "reason": reason,
        "timestamp": timestamp
    })


@app.route('/')
def home():
    eastern = ZoneInfo("America/New_York")
    startup = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    return f"Gatekeeper API is actively online! Current Time: {startup}"


if __name__ == '__main__':
    eastern = ZoneInfo("America/New_York")
    startup = datetime.now(eastern).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    print(f"Gatekeeper API started at {startup}")
    app.run(debug=True, port=5000)