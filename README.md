# Clinic Appointment Assistant

An Amazon Bedrock AgentCore assistant that looks up clinic appointments and simulates sending appointment reminders. The project demonstrates PII protection for outbound data and stored records.

## Setup

1. Clone the repository and move into the project:

`git clone <repository-url>`

`cd <repository-name>`

2. Create and activate a virtual environment:

`python -m venv .venv`

`source .venv/bin/activate`

3. Install the project:

`pip install -e .`

Create your .env file from the .env.example

4. Configure AWS credentials and the required AWS permissions for Amazon Bedrock Guardrails and Amazon Comprehend.

5. Set the required environment variables, including `GUARDRAIL_ID` and `GUARDRAIL_VERSION`.

## Run

Start the local AgentCore development environment:

```bash
agentcore dev
```

Use the AgentCore Web UI to test appointment lookups and reminder requests.

**Run environment:** Tested under `agentcore dev` locally; not deployed.

## PII Controls

* **Outbound:** An allow-list limits the fields sent to the simulated reminder provider, and Bedrock Guardrails checks the payload.
* **Inbound:** Appointment lookup intentionally returns the original record to demonstrate the inbound PII leak.
* **Storage:** Amazon Comprehend detects and redacts PII before records are persisted to `appointmentlog.json`.

## Tests

Run the tests with:

```bash
python -m pytest
```
