<p align="center"><img src="assets/logo.svg" width="50%" alt="whitebox logo" /></p>

# Whitebox - Machine learning monitoring platform

## What is Whitebox?

Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes.

## Why use Whitebox?

- Deploying a machine learning model in production is not the end of the lifecycle. You need data to iterate and improve.
- Solve data privacy by monitoring data at the edge and only return aggregated data for reporting and alerting.

# How to use

```mermaid
sequenceDiagram
    actor user
    participant whitebox

    user->>user: Import sdk
    note over user, whitebox: Configure model and monitors
    user->>whitebox: Create project
    user->>whitebox: Register model via SDK
    whitebox-->>user: model_id
    user->>whitebox: Register model training set
    user->>whitebox: Register model test set
    user->>whitebox: Configure monitors so you can get alerts

    note over user, whitebox: You can now start monitoring metrics and get alerts
    user->>whitebox: Log inferences
    whitebox-->>user: Monitor metrics
    whitebox-->>user: Get alerted
```

# Version 1.0 features

- API and SDK
- Supported model types: Binary, Multi-class
- Supported data types: tabular
- XAI: Feature importance on inference
- Available monitors through API
  - Data drift per feature compared to training
    - For numeric fields: Jensen–Shannon divergence
    - For categorical fields: Hellinger distance
  - Prediction / concept drift per feature compared to training
  - Missing values for model input data
  - Model performance monitoring:
    - Mean Squared Error
    - Root Mean Squared Error
    - Mean Absolute Error
    - Precision
    - Recall
    - F1
    - Accuracy
    - True Positive Count
    - True Negative Count
    - False Positive Count
    - False Negative Count
- Alerts accessible through API via pull

# Set up locally for development

Install packages:

```bash
python -m venv .venv
pip install -r requirements.txt
```

Run the server:

```bash
ENV=dev uvicorn src.main:app --reload
```

Run tests:

```bash
ENV=test pytest -s
```
