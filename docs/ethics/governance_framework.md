# Ethical Governance Framework for CognitionOS

This framework establishes the mandatory ethical bounds, privacy standards, and architectural constraints governing **CognitionOS**.

---

## 1. Non-Clinical Boundaries (Wellness vs. Diagnosis)

> [!WARNING]
> **CognitionOS is strictly forbidden from generating clinical diagnostic statements.**

1. **Self-Referral Focus**: Models must output indicators in terms of *behavioral metrics* (e.g., "Attention Fragmentation is high") rather than *clinical labels* (e.g., "Attention Deficit Hyperactivity Disorder").
2. **Output Filtering**: All recommendation and habit agent outputs must pass through the `GovernanceVerificationGuard` filter to intercept and strip out clinical terms (e.g., "depressed," "therapy," "diagnose").
3. **Emergency Escalation**: If metrics indicate severe, acute distress patterns (detected via sentiment frequency indicators), the system must bypass recommendations and display local crisis support resources instead.

---

## 2. Dynamic Consent & Data Autonomy

1. **Instant Revocation**: Users have absolute authority over their telemetry pipelines. Toggling off tracking in the client portal must:
   * Instantly disconnect ingestion webhooks.
   * Purge related database records for that feature identifier within 1 hour.
2. **Vector Memory Decay (Forgetting Principle)**:
   * To prevent the creation of permanent psychological profiles, vector database memories are configured with an exponential age-decay formula:
     $$\text{Embedding Relevance} = e^{-\lambda t}$$
   * Semantic history older than 6 months is completely expunged.

---

## 3. Explainability & Transparency (Explainable AI)

1. **No Black-Box Interventions**: Recommendations cannot be sent to users without a linked explainability audit. The user must be able to view *why* an intervention was proposed.
   * Example: "We suggest scheduling a screen break because your focus shift rate increased by 40% over your normal baseline this morning."
2. **Feature Attribution Auditing**:
   * Downstream models must output SHAP (SHapley Additive exPlanations) or LIME scores indicating which variables (e.g., notification count, sleep duration) contributed to the classification.
   * These weights are stored in the `ExplainabilityAudit` Postgres logs for evaluation by system researchers.

---

## 4. Anti-Manipulation and Positive Habit Loops

1. **No Attention Harvesting**: The system must never utilize notifications to increase app retention or gamify user interaction. All alerts should occur at designated context-aware times and respect user focus settings.
2. **Behavioral Autonomy**: Interventions must support user choice. Recommendations must offer options (e.g., "Would you prefer a 10-minute walk or a 5-minute breathing exercise?") rather than prescriptive commands.
