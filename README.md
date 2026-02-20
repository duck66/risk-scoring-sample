# Fraud Risk Scoring Module

## Overview

Python script with rule-based fraud risk scoring engine.

## Usage

### Risk assessment

```bash
python3 risk_assessment.py
```

### Risk Classification

| Score Range | Risk Level | Action  |
|------------|------------|---------|
| ≥ 80       | High       | REJECT  |
| 50–79      | Medium     | REVIEW  |
| < 50       | Low        | APPROVE |