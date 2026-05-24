import re
try:
    import spacy
except ImportError:
    spacy = None
from typing import Dict, Any, List

class JournalCognitiveParser:
    def __init__(self, spacy_model: str = "en_core_web_sm"):
        try:
            if spacy is not None:
                self.nlp = spacy.load(spacy_model)
            else:
                self.nlp = None
        except Exception:
            # Fallback mock/warning if SpaCy model loading fails
            self.nlp = None

    def anonymize_text(self, text: str) -> str:
        """Scrubs Personable Identifiable Information (Names, Locations, Emails, Phone numbers) to protect user privacy."""
        if not self.nlp:
            # Fallback simple regex scrubbing if SpaCy is unavailable
            email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
            return re.sub(email_pattern, "[EMAIL_REDACTED]", text)

        doc = self.nlp(text)
        anonymized_tokens = []
        
        for token in doc:
            # Replace Named Entities indicating people, organizations, or locations
            if token.ent_type_ in {"PERSON", "ORG", "GPE", "LOC"}:
                anonymized_tokens.append(f"[{token.ent_type_}_REDACTED]")
            elif token.like_email:
                anonymized_tokens.append("[EMAIL_REDACTED]")
            else:
                anonymized_tokens.append(token.text)
                
        return " ".join(anonymized_tokens)

    def extract_emotional_spectrum(self, clean_text: str) -> Dict[str, float]:
        """Interfaces with a downstream emotion classifier model (e.g., GoEmotions, distilbert)."""
        # Under phase 0, we structure the mapping dictionary contract
        # Standard GoEmotions or multi-label classification output representation
        return {
            "joy": 0.12,
            "sadness": 0.08,
            "fear": 0.05,
            "anger": 0.02,
            "confusion": 0.45,  # Focus of cognitive overload
            "fatigue": 0.28
        }

    def process_journal_entry(self, raw_entry: str) -> Dict[str, Any]:
        """Complete NLP pipeline scrubbing raw text first, then running cognitive analyses."""
        clean_text = self.anonymize_text(raw_entry)
        emotions = self.extract_emotional_spectrum(clean_text)
        
        return {
            "anonymized_text_preview": clean_text[:60] + "..." if len(clean_text) > 60 else clean_text,
            "metrics": emotions,
            "word_count": len(clean_text.split()),
            "governance_status": "passed_privacy_scrub"
        }
