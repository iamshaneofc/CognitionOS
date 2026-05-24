import unittest
import numpy as np
import polars as pl
from datetime import datetime
from services.ingestion.pipelines import TelemetryIngestor
from services.analytics.models import BehavioralDriftDetector
from services.cognitive.sentiment import JournalCognitiveParser
from services.governance.auditor import EthicalGovernanceAuditor
from services.agents.orchestrator import CognitiveAgentOrchestrator

class TestCognitionOSFoundation(unittest.TestCase):
    
    def test_telemetry_ingestor_and_fragmentation(self):
        """Verify ingestion parsing structures and Polars-based switch counting."""
        ingestor = TelemetryIngestor(anonymize=True)
        raw_events = [
            {"user_id": "u1", "timestamp": "2026-05-24T10:00:00", "event_type": "app_switch", "app_category": "social", "duration_seconds": 120.0},
            {"user_id": "u1", "timestamp": "2026-05-24T10:15:00", "event_type": "app_switch", "app_category": "productivity", "duration_seconds": 300.0},
            {"user_id": "u1", "timestamp": "2026-05-24T10:30:00", "event_type": "app_switch", "app_category": "social", "duration_seconds": 60.0}
        ]
        df = ingestor.process_raw_stream(raw_events)
        self.assertEqual(df.height, 3)
        
        # Calculate attention fragmentation (expected 2 app switches in 60 mins -> index of 2.0)
        index = ingestor.calculate_attention_fragmentation(df, window_minutes=60)
        self.assertEqual(index, 2.0)

    def test_behavioral_drift_detector(self):
        """Test baseline fit scaling and drift detection thresholds."""
        detector = BehavioralDriftDetector(deviation_threshold=1.5)
        # Create normal mock historical metrics: 12 days, 3 features (sleep, screen, switches)
        history = np.random.normal(loc=5.0, scale=0.5, size=(15, 3))
        detector.establish_user_baseline(history)
        self.assertTrue(detector.baseline_fitted)

        # Normal query metrics (close to center)
        current = np.array([5.0, 5.0, 5.0])
        dist, alert = detector.calculate_drift_score(current)
        self.assertFalse(alert)

        # Outlier query metrics (highly drifted)
        outlier = np.array([12.0, 1.0, 15.0])
        dist, alert = detector.calculate_drift_score(outlier)
        self.assertTrue(dist > 1.5)

    def test_nlp_pii_anonymizer(self):
        """Ensure sensitive PII (emails) are scrubbed before cognitive text indexing."""
        parser = JournalCognitiveParser()
        raw_text = "My name is John Doe and you can contact me at john.doe@email.com."
        clean_text = parser.anonymize_text(raw_text)
        
        self.assertNotIn("john.doe@email.com", clean_text)
        self.assertIn("[EMAIL_REDACTED]", clean_text)

    def test_ethical_governance_auditing(self):
        """Validate dynamic consent rules and model bias variance triggers."""
        auditor = EthicalGovernanceAuditor(bias_threshold=0.10)
        
        # Consent tracking profiles
        consent_profile = {"allow_nlp_sentiment": True, "allow_biometric_ingest": False}
        check1 = auditor.verify_consent(consent_profile, ["allow_nlp_sentiment"])
        self.assertTrue(check1["eligible"])
        
        check2 = auditor.verify_consent(consent_profile, ["allow_nlp_sentiment", "allow_biometric_ingest"])
        self.assertFalse(check2["eligible"])
        self.assertIn("allow_biometric_ingest", check2["revoked"])

        # Bias variance testing
        compl = auditor.audit_model_bias(
            prediction_distribution={"joy": 0.4, "sadness": 0.6},
            baseline_distribution={"joy": 0.38, "sadness": 0.62}
        )
        self.assertTrue(compl["is_compliant"])

    def test_agent_orchestration_loop(self):
        """Ensure LangGraph workflow compiler completes successfully."""
        orchestrator = CognitiveAgentOrchestrator()
        initial_state = {
            "user_id": "usr_7",
            "telemetry_metrics": {"cognitive_overload_index": 0.45, "attention_fragmentation_index": 5.0},
            "nlp_sentiment": {"fatigue": 0.3},
            "synthesized_context": "",
            "proposed_recommendations": [],
            "ethical_approved_recommendations": [],
            "compliance_errors": []
        }
        output = orchestrator.execute_pipeline(initial_state)
        self.assertIn("synthesized_context", output)
        self.assertGreater(len(output["ethical_approved_recommendations"]), 0)

if __name__ == "__main__":
    unittest.main()
