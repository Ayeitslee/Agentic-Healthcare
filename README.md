# Agentic-Healthcare

TPO Gatekeeper: A Rule Validator

## Overview
A Proof of Concept (POC) showing a Deterministic Gatekeeper for healthcare TPO (Treatment, Payment, Operations). It replaces human compliance methods by computer-executable logic.

This TPO Rule Validator utilizes agentic AI principles to embed real-time compliance checks directly into the system, automatically verifying whether incoming codes and transactions are valid.

## Key Features
* **Deterministic Execution:** The system uses a fixed rule engine to ensure the same procedure inputs always produce the same compliance outputs.
* **Constrained Autonomy:** The AI agent operates only within the boundaries defined in rules.json, preventing unauthorized actions.
* **Audit Defensibility (The Replay):** Manual compliance audits into simple database queries

## Technical Setup
* **Language:** Python (Flask)
* **Data Structure:** JSON-based "Executable Policy"
* **Security:** This architecture is designed for a private, encrypted environment where Protected Health Information (PHI) is tokenized before processing.
