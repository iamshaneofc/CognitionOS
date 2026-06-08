import time
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from shared.config import settings

# Initialize FastAPI instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="CognitionOS API Gateway and routing service layer.",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Set CORS origins for frontend client dashboards
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten in production config
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# System Observability metrics definitions
REQUEST_COUNT = Counter("gateway_requests_total", "Total requests received", ["method", "endpoint", "http_status"])
REQUEST_LATENCY = Histogram("gateway_request_latency_seconds", "Request latencies", ["endpoint"])

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    """Timing and response instrumentation middleware for Prometheus."""
    start_time = time.time()
    endpoint = request.url.path
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
    
    return response

@app.get("/")
async def root():
    return {
        "status": "online",
        "service": "api_gateway",
        "system": settings.PROJECT_NAME,
        "phase": 0
    }

@app.get("/metrics")
def metrics():
    """Expose application metrics to Prometheus scraping agents."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# --- Service Route Registrations (Stubs pointing to services directories) ---

@app.post("/api/v1/ingest", tags=["ingestion"])
async def ingest_telemetry(payload: dict):
    """Router stub forwarding active device telemetry to ingestion queues."""
    return {
        "status": "accepted",
        "payload_received": len(payload),
        "target_processor": "services.ingestion"
    }

@app.get("/api/v1/analytics/cognitive-score/{user_id}", tags=["analytics"])
async def get_cognitive_load(user_id: str):
    """Fetch computed overload indices, attention fragmentation indicators, and sleep metrics."""
    return {
        "user_id": user_id,
        "cognitive_overload_index": 0.32,
        "attention_fragmentation_index": 0.65,
        "burnout_drift_alert": False,
        "timestamp": time.time()
    }

@app.post("/api/v1/cognitive/analyze-journal", tags=["cognitive"])
async def analyze_journal(payload: dict):
    """Processes subjective user journal data and outputs sentiment metrics (scrubs PII)."""
    return {
        "sentiment_polarity": 0.15,
        "primary_emotional_state": "anxious_overload",
        "pii_anonymized": True,
        "governance_check": "passed"
    }

@app.post("/api/v1/agents/recommendation", tags=["agents"])
async def run_habit_agent(payload: dict):
    """Triggers LangGraph multi-agent loop to generate personalized habit feedback."""
    return {
        "recommendation": "Suggest scheduling a 30-minute visual rest block. High attention drift patterns noticed.",
        "ethical_boundary_check": "passed",
        "agent_nodes_traversed": ["context_synth_agent", "adaptive_feedback_agent", "ethics_guard_agent"]
    }

@app.get("/api/v1/governance/audit-logs", tags=["governance"])
async def get_audit_logs():
    """Retrieve local ethical compliance logs, model bias analysis metrics, and consent updates."""
    return {
        "logs": [
            {"timestamp": time.time(), "action": "consent_modification", "user_id": "usr_90", "details": "revoked GPS tracking"},
            {"timestamp": time.time(), "action": "model_bias_audit", "model": "SentimentModelV1", "variance": 0.04, "threshold_passed": True}
        ]
    }
