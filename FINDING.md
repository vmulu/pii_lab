# PII Lab

## Leak Analysis

| Leak                           | Crossed? | Closed? | What it catches                                                                                     | What it misses                                                  |
| ------------------------------ | -------- | ------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **OUT — Third-party provider Appointment Reminder Service** | Yes      | Yes     | Allow-list limits the payload to necessary fields, and Bedrock Guardrails checks it before sending. | May miss some sensitive information or misuse by the recipient. |
| **IN — Appointment lookup**    | Yes      | No      | Looks up appointments by ID.                                                                        | Returns the original record, including accidental PII.          |
| **STORED — Persisted records** | Yes      | Yes     | Comprehend detects and redacts PII before storage.                                                  | May miss some PII formats or types.                             |

## Fail Open vs. Fail Closed

If AWS protection services are unavailable, failing closed prevents unprotected data from being sent or stored, but may interrupt functionality. Failing open keeps the application running but risks exposing PII. For this lab, outbound transfers and storage should fail closed.

## With One More Day

I would add more tests for different PII formats and AWS service failures, verify that all storage paths redact data, and explore reducing unnecessary PII returned by the appointment lookup without breaking functionality.

