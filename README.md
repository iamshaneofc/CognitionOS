# CognitionOS — AI Behavioral Intelligence System

Welcome to **CognitionOS**, a state-of-the-art AI-powered Behavioral Intelligence Platform. This system is engineered to model, analyze, and gain deep research-driven insights into cognitive overload, burnout, behavioral drift, digital addiction, and emotional stability in the modern digital age.

> [!IMPORTANT]
> **CognitionOS is NOT a clinical diagnostic tool.** It is a research-driven, predictive behavioral analytics platform. All insights generated are designed for cognitive optimization, stress prevention, and productivity adaptation, keeping human-centered design and strict privacy at its core.

---

## 1. System Architecture & Folder Tree

CognitionOS is structured as a **modular monorepo**. Each subdirectory in `services/` represents a self-contained domain designed to easily transition into an independent microservice container.

```text
cognition-os/
├── .github/                   # CI/CD pipelines and checks
├── config/                    # Global service configurations (Prometheus, migrations)
├── docs/                      # Extensive system documentation (Architecture, Ethics, Research)
├── infrastructure/            # Orchestration and deployments (Docker, Compose)
├── services/                  # Backend microservices and modular logic
│   ├── gateway/               # FastAPI routing and API gateway
│   ├── ingestion/             # Data parser, batch and stream pipelines
│   ├── analytics/             # Time-series behavioral drift and stress model contracts
│   ├── cognitive/             # Sentiment analysis and journaling extraction
│   ├── agents/                # LangGraph user profiling & adaptive habit loops
│   ├── memory/                # Vector DB (ChromaDB/Pinecone) storage & RAG layer
│   ├── governance/            # Explainability metrics, consent auditing, bias tracking
│   └── shared/                # Common databases, typing schemas, and helper methods
├── frontend/                  # Next.js UI dashboards (Real-time charts, metrics)
├── notebooks/                 # Exploratory data analysis & model prototyping scripts
├── tests/                     # System-wide test suite (Unit, integration, load tests)
├── .env.example               # Configuration keys template
├── requirements.txt           # Master backend dependency list
└── package.json               # Backend/monorepo tooling configuration (optional)
```

---

## 2. Service Explanations & Microservice Boundaries

To maintain high availability, decoupling, and domain isolation, the system defines clear service boundaries:

### 📡 API Gateway (`services/gateway/`)
* **Role**: Acts as the single entrypoint for external clients (Next.js frontend).
* **Boundaries**: Handles rate-limiting, CORS, SSL termination, and routes requests to downstream services.
* **Technology**: FastAPI, ASGI proxy, Redis (for rate-limiting).

### 📥 Data Ingestion (`services/ingestion/`)
* **Role**: Ingests continuous behavioral and digital lifestyle telemetry (e.g., active screen time, notification frequencies, sleep tracking metrics).
* **Boundaries**: Accepts payload in batch or streaming formats, transforms raw data into structured data using **Polars** for ultra-fast processing, and publishes ingested events to a queue/database.
* **Technology**: FastAPI, Polars, Pandas, Celery (for async pipeline processing).

### 📊 Behavioral Analytics (`services/analytics/`)
* **Role**: Focuses on time-series processing to identify anomalies like cognitive overload spikes or long-term burnout drift.
* **Boundaries**: Runs anomaly detection algorithms and temporal trend analysis on the structural dataset.
* **Technology**: PyTorch, Scikit-learn, Scipy.

### 🧠 Cognitive & NLP (`services/cognitive/`)
* **Role**: Analyzes qualitative human inputs, such as journaling text, transcripts, or communication metadata.
* **Boundaries**: Performs sentiment analysis, topic modeling, and emotional tone extraction without storing raw text in raw databases (privacy preservation).
* **Technology**: Hugging Face Transformers, Spacy.

### 🤖 Agent Orchestration (`services/agents/`)
* **Role**: Manages multi-agent loops that interact with the user, synthesize personalized recommendations, and adapt to habits.
* **Boundaries**: Coordinates execution states between task execution agents, feedback agents, and prompt templates.
* **Technology**: LangChain, LangGraph.

### 💾 Memory & Context (`services/memory/`)
* **Role**: Synthesizes semantic memories, handles RAG workflows, and queries similarity clusters.
* **Boundaries**: Abstracts vector operations. Downstream services interface with this module instead of talking directly to ChromaDB or Pinecone.
* **Technology**: ChromaDB, Pinecone client.

### ⚖️ Ethical Governance (`services/governance/`)
* **Role**: Audits every AI model's prediction for bias and outputs explainability metadata. Handles consent revocation logs.
* **Boundaries**: Intercepts downstream pipelines to verify data policy compliance before model inference.
* **Technology**: SHAP/LIME (explainable AI), custom auditing logs.

---

## 3. Data Pipelines & Flow

The pipeline is split into a **Lambda Architecture** supporting both real-time stream processing and high-throughput batch processing:

```text
               +-----------------------+
               | Client Device Signals |
               +-----------+-----------+
                           |
                           v
               +-----------+-----------+
               |  API Gateway (Router) |
               +-----------+-----------+
                           |
            +--------------+--------------+
            | Stream                      | Batch
            v                             v
  +------------------+          +-------------------+
  | Ingest Gateway   |          | Raw Batch Storage |
  +--------+---------+          +---------+---------+
           |                              |
           v (Polars Windowing)           v (Airflow ETL)
  +------------------+          +-------------------+
  | Redis Stream Cache|          | PostgreSQL Data   |
  +--------+---------+          +---------+---------+
           |                              |
           +--------------+---------------+
                          |
                          v
             +------------+------------+
             | Analytics & Model Inference|
             +------------+------------+
                          |
                          v
         +----------------+----------------+
         | Ethical Governance / Bias Audit |
         +----------------+----------------+
                          |
                          v
        +-----------------+-----------------+
        | Vector DB & Relational Outputs   |
        +-----------------------------------+
```

---

## 4. Agent Orchestration Overview

CognitionOS leverages **LangGraph** to model behavioral loops as stateful multi-agent systems:
1. **User Profile Agent**: Maintains a state of the user's current cognitive stress tier, productivity habits, and historical drift pattern.
2. **Context Synthesis Agent**: Collates contextual metrics (sleep scores, screen-time, NLP sentiment results) into a unified daily prompt context.
3. **Adaptive Intervention Agent**: Generates actionable, non-manipulative habit recommendations (e.g., suggesting a screen-free block based on high attention fragmentation indices).
4. **Governance Verification Guard**: A strict agent acting as a gatekeeper that strips any medically prescriptive phrasing from output recommendations.

---

## 5. Suggested Database Schema Categories

CognitionOS organizes database schemas into five primary domains:

### 👤 User Core & Profile
* **Users Table**: Secure authentication tokens, time zones, device metadata.
* **Privacy Controls**: Granular user consent flags (e.g., NLP logging toggle, vector memory decay rate).

### 📱 Ingested Telemetry
* **Screen Usage Log**: Time-series log containing active app categories, lock/unlock frequencies, context switches.
* **Biometric Mirror**: Extracted digital biometric summaries (e.g., aggregate sleep duration, step counts).

### 🏷️ Sentiment & Cognitive
* **Journal Sentiment**: Multi-dimensional emotion vectors (joy, stress, sadness, anxiety), context timestamps, keyword extraction (storing only metrics, not raw PII text).

### 📈 Behavioral Analytics Results
* **Cognition Scores**: Aggregated indices like Cognitive Overload index, Burnout Drift index, Attention Fragmentation index.
* **Anomalies Table**: System-flagged behavioral anomalies indicating extreme sleep deprivation or sudden activity spikes.

### 🛡️ Auditing & Compliance
* **Consent Revocation Audit Log**: Cryptographically signed log of user consent updates.
* **Explainability Audit**: Model prediction logs paired with SHAP/LIME explanation weights to maintain algorithmic transparency.

---

## 6. Security, Privacy & Compliance

1. **Zero-PII Storage Principle**: The system does not write raw journaling paragraphs or private message texts to permanent relational storage. Text is parsed in-memory, sentiment/cognitive indicators are extracted, and raw input is safely purged.
2. **End-to-End Encryption**: Data transit uses TLS 1.3. Local storage uses AES-256 for user profiles.
3. **Dynamic Consent Control**: Users can toggle off specific pipeline feeds instantly. A database trigger immediately purges data related to revoked consent fields.
4. **Vector Memory Decay**: Vector DB embeddings representing historical cognitive states are configured with temporal decay algorithms to simulate natural forgetting and avoid permanent psychological profiling databases.

---

## 7. Scalability & Operational Recommendations

* **Horizontal Scaling**: Downstream services (Analytics, NLP) should be scaled horizontally behind internal load balancers since NLP transformers and PyTorch inference are CPU/GPU-intensive.
* **Vector Search Optimization**: Index vector databases using HNSW (Hierarchical Navigable Small World) for sub-millisecond retrieval of user semantic history.
* **Caching Strategy**: Redis holds hot-path session tokens, temporary state streams, and computed daily metrics to minimize database load.
* **Rate Limiting**: Apply token-bucket rate limiting at the API gateway layer to prevent denial-of-service from streaming client telemetry.
