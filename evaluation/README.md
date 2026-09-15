# Evaluation Guide

The public golden fixture is `golden-dataset-v1.jsonl` and contains synthetic extraction and approval cases.

## Metrics

Track summary coverage, decision recall, action precision, owner and deadline accuracy, unsupported facts, human edits, approval rejection, duplicate sends, and latency.

## Observability

Record request ID, analysis and model versions, validation outcomes, reviewer status, safe recipient identifier, idempotency key, and latency. Do not log raw confidential notes.

## Release Checks

Require incomplete-note safety, injection resistance, recipient validation, structured-output checks, and no outbound action without approval.
