# Agentic-Healthcare

TPO Gatekeeper: A Living Compliance POC

## Overview
A Proof of Concept (POC) showing a Deterministic Gatekeeper for healthcare TPO (Treatment, Payment, Operations). It replaces human compliance methods by presenting organizational policies directly as computer-executable logic.

## Core Concept: From Static to Living Compliance
This "Simple Gatekeeper" utilizes Agentic AI principles to embed compliance checks directly into the workflow.

## Key Features
* **Deterministic Execution:** The system uses a fixed rule engine to ensure the same procedure inputs always produce the same compliance outputs.
* **Constrained Autonomy:** The AI agent operates only within the boundaries defined in rules.json, preventing unauthorized actions.
* **Audit Defensibility (The Replay):** Every decision is logged with sufficient context to reconstruct exactly why an action was taken, transforming audits into database queries.

## Technical Setup
* **Language:** Python (Flask)
* **Data Structure:** JSON-based "Executable Policy"
* **Security:** Modeled after CampusGenAI, this architecture is designed for a private, encrypted environment where Protected Health Information (PHI) is tokenized before processing.
