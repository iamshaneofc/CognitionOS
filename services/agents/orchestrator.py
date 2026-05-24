from typing import Dict, Any, List, TypedDict

try:
    from langgraph.graph import StateGraph, END
except ImportError:
    # Lightweight mock framework for LangGraph orchestrations
    class MockStateGraph:
        def __init__(self, state_schema):
            self.nodes = {}
            self.edges = []
            self.entry_point = None
        def add_node(self, name, func):
            self.nodes[name] = func
        def add_edge(self, start, end):
            self.edges.append((start, end))
        def set_entry_point(self, name):
            self.entry_point = name
        def compile(self):
            class CompiledWorkflow:
                def __init__(self, parent):
                    self.parent = parent
                def invoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
                    curr = self.parent.entry_point
                    # Walk through sequential edges until END
                    visited = set()
                    while curr and curr != 'end':
                        if curr in visited:
                            break
                        visited.add(curr)
                        node_func = self.parent.nodes[curr]
                        updates = node_func(state)
                        state.update(updates)
                        
                        next_node = None
                        for start, end in self.parent.edges:
                            if start == curr:
                                next_node = end
                                break
                        curr = next_node
                    return state
            return CompiledWorkflow(self)
            
    StateGraph = MockStateGraph
    END = 'end'


# Define the state dictionary passed between agent nodes
class AgentState(TypedDict):
    user_id: str
    telemetry_metrics: Dict[str, Any]
    nlp_sentiment: Dict[str, float]
    synthesized_context: str
    proposed_recommendations: List[str]
    ethical_approved_recommendations: List[str]
    compliance_errors: List[str]

class CognitiveAgentOrchestrator:
    def __init__(self):
        # Initialize LangGraph StateGraph
        self.workflow = StateGraph(AgentState)
        self._build_graph()

    def context_synthesizer_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 1: Combines multi-source metrics into a descriptive context prompt."""
        metrics = state.get("telemetry_metrics", {})
        sentiment = state.get("nlp_sentiment", {})
        
        context_summary = (
            f"User shows cognitive load index of {metrics.get('cognitive_overload_index', 0.0)}. "
            f"Active screen-time switched categories {metrics.get('attention_fragmentation_index', 0.0)} times/hr. "
            f"Emotional spectrum highlights sadness: {sentiment.get('sadness', 0.0)}, fatigue: {sentiment.get('fatigue', 0.0)}."
        )
        return {"synthesized_context": context_summary}

    def intervention_generator_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 2: Proposes adaptive habits or focus blocks based on synthesized context."""
        context = state.get("synthesized_context", "")
        recommendations = []
        
        if "cognitive load index of 0.3" in context or "fatigue" in context:
            recommendations.append("Schedule 20-minute screen-free rest cycle to allow visual pathways to refresh.")
        else:
            recommendations.append("All digital indicators within nominal bounds. Keep going!")
            
        return {"proposed_recommendations": recommendations}

    def ethics_guard_node(self, state: AgentState) -> Dict[str, Any]:
        """Node 3: Audits proposed recommendations to block medical diagnostics or manipulative patterns."""
        proposed = state.get("proposed_recommendations", [])
        approved = []
        errors = []
        
        # Regex or classifier check for medical diagnosis claims (clinical-free policy compliance)
        medical_keywords = ["diagnose", "clinical", "depression", "therapy", "medicate", "anxiety disorder"]
        
        for rec in proposed:
            if any(keyword in rec.lower() for keyword in medical_keywords):
                errors.append(f"Rejected recommendation containing diagnostic text: {rec}")
            else:
                approved.append(rec)
                
        return {
            "ethical_approved_recommendations": approved,
            "compliance_errors": errors
        }

    def _build_graph(self):
        """Constructs the nodes and edge paths on the StateGraph execution flow."""
        self.workflow.add_node("synthesize_context", self.context_synthesizer_node)
        self.workflow.add_node("generate_intervention", self.intervention_generator_node)
        self.workflow.add_node("ethics_guard", self.ethics_guard_node)

        # Set execution path: Synthesize -> Generate -> Ethics -> End
        self.workflow.set_entry_point("synthesize_context")
        self.workflow.add_edge("synthesize_context", "generate_intervention")
        self.workflow.add_edge("generate_intervention", "ethics_guard")
        self.workflow.add_edge("ethics_guard", END)

        # Compile graph structure
        self.app = self.workflow.compile()

    def execute_pipeline(self, initial_state: AgentState) -> Dict[str, Any]:
        """Runs the compiled LangGraph execution loop."""
        return self.app.invoke(initial_state)
