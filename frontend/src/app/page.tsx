"use client";

import React, { useState } from "react";
import { 
  Activity, 
  BrainCircuit, 
  Cpu, 
  ShieldAlert, 
  Database, 
  Sparkles, 
  Clock, 
  Layers, 
  Scale, 
  Search,
  MessageSquareDiff,
  Flame,
  UserCheck
} from "lucide-react";

export default function Home() {
  const [selectedService, setSelectedService] = useState<string>("gateway");

  const serviceRegistry = [
    { id: "gateway", name: "FastAPI Gateway", status: "Healthy", port: "8000", load: "2.4%", desc: "Central request routing, OAuth2 security layers, and client request rate limiting." },
    { id: "ingestion", name: "Data Ingestion", status: "Active", port: "8001", load: "14.2 ms latency", desc: "Batch and stream processing of telemetry events (screen events, biometrics) using Polars." },
    { id: "analytics", name: "Behavioral Analytics", status: "Monitoring", port: "8002", load: "0.08s inf", desc: "Time-series processing of burnout indicators, sleep balance, and cognitive overload drift." },
    { id: "cognitive", name: "Cognitive NLP Engine", status: "Idle", port: "8003", load: "0%", desc: "LLM embedding generation, sentiment analysis of journals, and thematic extraction loops." },
    { id: "agents", name: "Agent Orchestrator", status: "Listening", port: "8004", load: "3 tasks active", desc: "LangGraph-driven state loops modifying user habit loops and context synthesis." },
    { id: "memory", name: "Context Memory Layer", status: "Synchronized", port: "8005", load: "42k vectors", desc: "Maintains semantic long-term memory structures across vector database boundaries." },
    { id: "governance", name: "Ethical Governance", status: "Auditing", port: "8006", load: "0.00% bias variance", desc: "Strictly audits generated alerts, checks bias bounds, and executes user consent rules." }
  ];

  return (
    <div className="min-h-screen p-6 md:p-12 z-10 relative">
      {/* Top Header */}
      <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-10 pb-6 border-b border-white/5">
        <div>
          <div className="flex items-center gap-3 mb-1">
            <span className="px-2 py-0.5 text-xs font-semibold uppercase tracking-wider rounded bg-state-optimal/10 text-state-optimal border border-state-optimal/20 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-state-optimal animate-pulse"></span>
              Phase 0 Active
            </span>
            <span className="text-gray-500 text-xs">v0.1.0 (Alpha Build)</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight font-sans text-transparent bg-clip-text bg-gradient-to-r from-white via-gray-200 to-gray-400">
            CognitionOS Portal
          </h1>
        </div>

        <div className="flex gap-4 items-center">
          <div className="glass-panel px-4 py-2 rounded-lg flex items-center gap-3">
            <Activity className="w-4 h-4 text-state-optimal" />
            <div className="text-left">
              <p className="text-[10px] text-gray-400 uppercase tracking-wider">Telemetry Rate</p>
              <p className="text-sm font-semibold text-white">418 events/sec</p>
            </div>
          </div>
          <div className="glass-panel px-4 py-2 rounded-lg flex items-center gap-3">
            <Database className="w-4 h-4 text-state-recovery" />
            <div className="text-left">
              <p className="text-[10px] text-gray-400 uppercase tracking-wider">Sync State</p>
              <p className="text-sm font-semibold text-white">Synced (ChromaDB)</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Grid Layout */}
      <main className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        
        {/* Left Side: System Status Grid & Simulated Metrics */}
        <section className="col-span-1 lg:col-span-8 space-y-8">
          
          {/* Main Anomaly / Critical Signals Indicator Widget */}
          <div className="glass-panel p-6 rounded-xl relative overflow-hidden">
            <div className="absolute top-0 right-0 w-[150px] h-[150px] bg-gradient-to-bl from-state-overload/10 to-transparent rounded-bl-full pointer-events-none"></div>
            <div className="flex items-start justify-between mb-6">
              <div>
                <h2 className="text-lg font-semibold tracking-tight text-white mb-1 flex items-center gap-2">
                  <BrainCircuit className="w-5 h-5 text-accent-neon" />
                  Real-time Behavioral Analytics Pipeline
                </h2>
                <p className="text-xs text-gray-400">Continuous assessment of behavioral metrics and cognitive indicators.</p>
              </div>
              <span className="text-xs px-2.5 py-1 rounded bg-white/5 border border-white/10 text-gray-300 font-mono">Simulated telemetry stream</span>
            </div>

            {/* Cognitive Stats Dashboard Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-lg bg-bg-darker border border-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs text-gray-400 font-medium">Cognitive Overload</span>
                  <Flame className="w-4 h-4 text-state-overload" />
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-white">32.4%</span>
                  <span className="text-[10px] text-state-optimal font-medium">-1.2% /hr</span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-state-overload h-full rounded-full" style={{ width: "32.4%" }}></div>
                </div>
              </div>

              <div className="p-4 rounded-lg bg-bg-darker border border-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs text-gray-400 font-medium">Attention Fragmentation</span>
                  <Cpu className="w-4 h-4 text-state-drift" />
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-white">64.8%</span>
                  <span className="text-[10px] text-state-overload font-medium">+8.5% /hr</span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-state-drift h-full rounded-full" style={{ width: "64.8%" }}></div>
                </div>
              </div>

              <div className="p-4 rounded-lg bg-bg-darker border border-white/5">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-xs text-gray-400 font-medium">Recovery & Sleep Score</span>
                  <Clock className="w-4 h-4 text-state-recovery" />
                </div>
                <div className="flex items-baseline gap-2">
                  <span className="text-2xl font-bold text-white">88.2%</span>
                  <span className="text-[10px] text-state-optimal font-medium">Optimal</span>
                </div>
                <div className="w-full bg-white/5 h-1.5 rounded-full mt-3 overflow-hidden">
                  <div className="bg-state-optimal h-full rounded-full" style={{ width: "88.2%" }}></div>
                </div>
              </div>
            </div>
          </div>

          {/* Microservice Directory and Inter-service status */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold tracking-tight text-white flex items-center gap-2">
              <Layers className="w-5 h-5 text-state-recovery" />
              Service Framework & Boundaries (Phase 0)
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {serviceRegistry.map((srv) => (
                <button
                  key={srv.id}
                  onClick={() => setSelectedService(srv.id)}
                  className={`glass-panel p-4 rounded-lg text-left transition-all ${
                    selectedService === srv.id 
                      ? "border-accent-neon ring-1 ring-accent-neon bg-accent-glow"
                      : "glass-panel-hover"
                  }`}
                >
                  <div className="flex justify-between items-start mb-2">
                    <span className="font-semibold text-white text-sm">{srv.name}</span>
                    <span className={`text-[10px] px-2 py-0.5 rounded font-mono ${
                      srv.status === 'Healthy' || srv.status === 'Active' || srv.status === 'Synchronized'
                        ? 'bg-state-optimal/10 text-state-optimal'
                        : 'bg-state-drift/10 text-state-drift'
                    }`}>
                      {srv.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-400 line-clamp-2 mb-3">{srv.desc}</p>
                  <div className="flex justify-between items-center text-[10px] font-mono text-gray-500">
                    <span>Port: {srv.port}</span>
                    <span>Metrics: {srv.load}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

        </section>

        {/* Right Side: Selected Service Detail & Governance Board */}
        <section className="col-span-1 lg:col-span-4 space-y-8">
          
          {/* Selected Service Detailed View */}
          <div className="glass-panel p-6 rounded-xl">
            <h2 className="text-sm font-semibold uppercase tracking-wider text-gray-400 mb-4 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-accent-neon animate-pulse" />
              Boundary Inspector
            </h2>

            {(() => {
              const active = serviceRegistry.find(s => s.id === selectedService) || serviceRegistry[0];
              return (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-bold text-white">{active.name}</h3>
                    <p className="text-xs text-gray-500 font-mono">Service Key: services/{active.id}/</p>
                  </div>
                  <p className="text-sm text-gray-300 leading-relaxed bg-bg-darker p-3 rounded border border-white/5">
                    {active.desc}
                  </p>
                  <div className="space-y-2 border-t border-white/5 pt-4 text-xs">
                    <div className="flex justify-between">
                      <span className="text-gray-400">Communication Mode</span>
                      <span className="text-white font-semibold">REST API / Event Driven</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Security Layer</span>
                      <span className="text-white font-semibold">JWT + SSL Encryption</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-400">Downstream Links</span>
                      <span className="text-white font-semibold">db, redis, memory</span>
                    </div>
                  </div>
                </div>
              );
            })()}
          </div>

          {/* Ethical Governance Audit Panel */}
          <div className="glass-panel p-6 rounded-xl border-l-4 border-l-state-optimal relative overflow-hidden">
            <div className="flex items-center gap-3 mb-4">
              <Scale className="w-5 h-5 text-state-optimal" />
              <h2 className="text-sm font-semibold uppercase tracking-wider text-gray-400">Ethical Control Board</h2>
            </div>
            
            <div className="space-y-3 text-xs">
              <div className="flex items-start gap-2 bg-state-optimal/5 p-2 rounded border border-state-optimal/10">
                <UserCheck className="w-4 h-4 text-state-optimal shrink-0 mt-0.5" />
                <p className="text-gray-300">
                  <strong className="text-white">Strict Non-Clinical Policy:</strong> Cognitive score analysis triggers warning triggers without diagnostic medical statements.
                </p>
              </div>

              <div className="flex items-start gap-2 bg-state-overload/5 p-2 rounded border border-state-overload/10">
                <ShieldAlert className="w-4 h-4 text-state-overload shrink-0 mt-0.5" />
                <p className="text-gray-300">
                  <strong className="text-white">Anonymizer Guard:</strong> Active in-memory processing forces automated PII scrub before saving database records.
                </p>
              </div>
            </div>
          </div>

        </section>
      </main>

      {/* Footer */}
      <footer className="mt-16 pt-6 border-t border-white/5 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-gray-500">
        <p>© 2026 CognitionOS System Architect portal. All design paths ready for future implementation layers.</p>
        <div className="flex gap-4">
          <a href="#" className="hover:text-white transition-colors">Architecture Documentation</a>
          <span className="text-white/10">|</span>
          <a href="#" className="hover:text-white transition-colors">Ethics Policy</a>
        </div>
      </footer>
    </div>
  );
}
