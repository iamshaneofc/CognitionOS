import polars as pl
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime

class TelemetryEvent(BaseModel):
    user_id: str
    timestamp: datetime
    event_type: str  # e.g., "screen_lock", "notification_received", "app_switch"
    app_category: str  # e.g., "social", "productivity", "communication"
    duration_seconds: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class TelemetryIngestor:
    def __init__(self, anonymize: bool = True):
        self.anonymize = anonymize

    def process_raw_stream(self, raw_events: List[Dict[str, Any]]) -> pl.DataFrame:
        """Parses, scrub-filters, and structures raw JSON streams into structured Polars DataFrames."""
        if not raw_events:
            return pl.DataFrame()

        # Validate with Pydantic first
        validated_events = []
        for e in raw_events:
            try:
                event = TelemetryEvent(**e)
                # Apply in-memory anonymization rules if toggled
                if self.anonymize:
                    event.metadata.pop("device_serial", None)
                    event.metadata.pop("location_coordinates", None)
                validated_events.append(event.model_dump())
            except Exception:
                # In production, route bad events to a Dead Letter Queue (DLQ)
                continue

        # Load into Polars DataFrame
        df = pl.DataFrame(validated_events)
        return self._normalize_schema(df)

    def _normalize_schema(self, df: pl.DataFrame) -> pl.DataFrame:
        """Ensure standard formatting and columns names on telemetry tables."""
        return df.with_columns([
            pl.col("timestamp").cast(pl.Datetime),
            pl.col("duration_seconds").cast(pl.Float64)
        ])

    def calculate_attention_fragmentation(self, df: pl.DataFrame, window_minutes: int = 60) -> float:
        """Computes focus disruption indices based on count of app context-switches in a temporal window."""
        if df.is_empty():
            return 0.0
        
        # Sort by timestamp
        sorted_df = df.sort("timestamp")
        
        # Calculate shifts in app category (app switches)
        app_switches = sorted_df.filter(
            pl.col("app_category") != pl.col("app_category").shift(1)
        ).height
        
        # Return switch frequency (switches per hour index)
        return float(app_switches / (window_minutes / 60.0))
