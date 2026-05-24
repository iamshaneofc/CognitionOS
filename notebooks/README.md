# CognitionOS Research & Modeling Notebooks

This folder is dedicated to research prototyping, exploratory data analysis (EDA), and machine learning experiment modeling.

## Prototyping Best Practices

1. **Keep Experiments Tracked**: Every model training run should be logged to MLflow or Weights & Biases using variables specified in the `.env` configuration file.
2. **Handle PII Safely**: Never load raw patient or user text files in git-tracked notebooks. Use mock generators or anonymized CSVs from the sandbox datasets folder.
3. **Save Artifacts**: Export trained PyTorch weights and scaler files (`.pt` or `.pkl`) directly to MLflow registry paths instead of local workspace directories.
