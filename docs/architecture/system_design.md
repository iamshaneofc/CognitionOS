# CognitionOS System Design

This document details the architecture, design choices, and data flow pipelines for **CognitionOS**.

---

## 1. Multi-Service Communication Protocol

To ensure decoupling and low latency, CognitionOS separates real-time ingestion from compute-intensive NLP and AI modeling:

1. **Gateway Router**: Central FastAPI router which acts as a reverse proxy. It rate-limits requests at the edge and routes them asynchronously.
2. **Event Brokers**: Redis Streams or RabbitMQ handle telemetry event queues. Ingestion workers subscribe to these queues to process events out-of-band.
3. **Internal REST / gRPC**: Downstream services (Analytics, Agents, memory) interact using internal REST APIs or gRPC for low-overhead communication.

---

## 2. In-Memory Data Scrubbing (Privacy-First NLP)

To prevent persistent data stores from holding private text narratives (e.g., chat logs or journaling inputs), CognitionOS mandates a **transient text processing flow**:

```text
[Raw User Journal] 
       │
       ▼
[NLP Gateway Router] ── (Memory Only) ──► [SpaCy NER Model]
                                                   │
                                            (PII Redaction)
                                                   │
                                                   ▼
[Downstream LLM Embedding] ◄──────────────── [Scrubbed Text]
       │
  (Vector Index)
       │
       ▼
[ChromaDB Vector Store]
```

* **Rule**: Raw text containing entity tokens (`PERSON`, `LOC`, `EMAIL`, etc.) is processed in volatile memory. 
* Only the calculated multi-dimensional emotional state arrays and the vector embedding representing semantic context are written to permanent databases.

---

## 3. Core Database Schemas

### Relational Database (PostgreSQL)

```sql
-- User Profile & Identity Control
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    timezone VARCHAR(100) DEFAULT 'UTC',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Granular Consent Policies (Dynamic Privacy Rules)
CREATE TABLE user_consent_profiles (
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    allow_nlp_sentiment BOOLEAN DEFAULT TRUE,
    allow_biometric_ingest BOOLEAN DEFAULT TRUE,
    allow_screen_telemetry BOOLEAN DEFAULT TRUE,
    consent_updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

-- Ingested Behavior Telemetry Metadata (Aggregation target)
CREATE TABLE daily_behavior_metrics (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    cognitive_overload_index DOUBLE PRECISION DEFAULT 0.0,
    attention_fragmentation_index DOUBLE PRECISION DEFAULT 0.0,
    active_screentime_minutes INTEGER DEFAULT 0,
    sleep_duration_hours DOUBLE PRECISION DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, date)
);
```

### Vector Database (ChromaDB/Pinecone)

* **Collection Name**: `user_semantic_memory`
* **Vector Dimension**: 1536 (OpenAI text-embedding-3-small) or 384 (all-MiniLM-L6-v2)
* **Metadata Schema**:
  * `user_id`: UUID
  * `timestamp`: Epoch integer
  * `cognitive_tier`: String (`nominal`, `overloaded`, `drifted`)
  * `emotional_tone`: Primary sentiment string

---

## 4. Operational Scaling Blueprint

1. **GPU Allocation for NLP & Agents**:
   * Deploy the NLP parser (`services/cognitive/`) and Agent Orchestrator (`services/agents/`) onto nodes equipped with NVIDIA T4 or A10G GPUs to handle token generation latency.
2. **Sharding PostgreSQL Telemetry Tables**:
   * Telemetry logs scale exponentially. Table partitioning must be implemented, sharding the tables by `user_id` and partitioning by `date` ranges.
3. **Auto-decaying Vector Indexes**:
   * To prevent vector database cost explosion and respect "the right to be forgotten," execute a cron task daily to decay and delete semantic vectors older than 180 days.
