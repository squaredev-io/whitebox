<p align="center"><img src="assets/logo.svg" width="50%" alt="whitebox logo" /></p>

# Whitebox - Machine learning monitoring platform

## What is Whitebox?

Whitebox is an open source E2E ML monitoring platform with edge capabilities that plays nicely with kubernetes.

## Why use Whitebox?

Deploying a machine learning model in production is not the end of the lifecycle. You need data to iterate and improve.

# How to use

## Run the server

> 👉 Coming soon. You can use development environment described below until everything is ready

## Using the SDK

> 👉 Coming soon

## High level diagram of model set up

All you have to do is register a model and send inference data through the SDK.

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
    user->>whitebox: Setup monitors

    note over user, whitebox: You can now start monitoring metrics and get alerts
    user->>whitebox: Log inferences
    whitebox-->>user: Monitor metrics
    whitebox-->>user: Get alerted
```

# Features

## Planned

- [ ] Minimum viable API
- [ ] Supported model types: Binary classification, Multi-class classification
- [ ] Supported data types: structured
- [ ] Feature importance on inference using SHAP values (XAI)
- [ ] Monitors set up through API
- [ ] Alerts accessible through API via pull
- [ ] Grafana integration

## Coming soon

- Whitebox UI
- Regression models
- Data segments
- Edge / privacy features

## Available metrics

- Data drift per feature compared to training
- Prediction / concept drift per feature compared to training
- Missing values for model input data
- Model performance monitoring (classification):
  - Precision
  - Recall
  - F1
  - Accuracy
  - Confusion matrix

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

# Contributing

We happily welcome contributions to Whitebox. Open issues with ideas
