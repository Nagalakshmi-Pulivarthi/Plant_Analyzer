"""
LangGraph StateGraph — the plant analysis workflow.

Graph structure:
    [observe_plant_node]
            ↓
    [route_by_condition]       ← Conditional Edge (Level 1 + Level 2 combined)
            ├── viral          → [viral_node]            → [severity_assessment_node]
            ├── fungal_bacterial→ [fungal_bacterial_node] → [severity_assessment_node]
            ├── pest           → [pest_node]             → [severity_assessment_node]
            ├── stress         → [stress_node]           → [severity_assessment_node]
            └── healthy        → [care_tips_node]        → [severity_assessment_node]
"""
from langgraph.graph import StateGraph, START, END

from graph.state import PlantAnalysisState
from graph.nodes import (
    observe_plant_node,
    viral_node,
    fungal_bacterial_node,
    pest_node,
    stress_node,
    care_tips_node,
    severity_assessment_node,
)


# ---------------------------------------------------------------------------
# CONDITIONAL EDGE — Route by plant condition
# Reads plant_observations from state and decides which Node 2 to run.
# This is the intelligence layer — developer-controlled routing logic.
# ---------------------------------------------------------------------------
def route_by_condition(state: PlantAnalysisState) -> str:
    """
    Reads plant observations and decides which recommendation path to take.

    Level 1: Is there any issue?
        NO  → healthy → care_tips_node
        YES → go to Level 2

    Level 2: What type of issue?
        viral infection detected  → viral_node
        fungal/bacterial detected → fungal_bacterial_node
        pest damage detected      → pest_node
        water/sunlight stress     → stress_node
    """
    obs = state["plant_observations"]

    bacteria_or_fungus = obs.get("bacteria_or_fungus_detected", "None").lower()
    pest_damage        = obs.get("pest_damage", "None").lower()
    stress             = obs.get("water_or_sunlight_stress", "None").lower()
    leaf_health        = obs.get("leaf_health", "").lower()

    # --- LEVEL 1: Is there any issue? ---
    no_issue = (
        bacteria_or_fungus in ("none", "no", "") and
        pest_damage        in ("none", "no", "") and
        stress             in ("none", "no", "") and
        any(word in leaf_health for word in ("healthy", "no issue", "normal", "good"))
    )

    if no_issue:
        return "healthy"

    # --- LEVEL 2: What type of issue? ---

    # Check for viral infection first (most critical — no cure)
    if "viral" in bacteria_or_fungus or "virus" in bacteria_or_fungus:
        return "viral"

    # Fungal or bacterial infection
    if bacteria_or_fungus not in ("none", "no", ""):
        return "fungal_bacterial"

    # Pest damage
    if pest_damage not in ("none", "no", ""):
        return "pest"

    # Environmental stress (water or sunlight)
    if stress not in ("none", "no", ""):
        return "stress"

    # Fallback — something was flagged but unclear, treat as stress
    return "stress"


# ---------------------------------------------------------------------------
# HELPER — Sets analysis_path in state before entering Node 2
# This ensures severity_assessment_node knows which path was taken
# ---------------------------------------------------------------------------
def set_viral_path(state: PlantAnalysisState) -> dict:
    return {"analysis_path": "viral"}

def set_fungal_bacterial_path(state: PlantAnalysisState) -> dict:
    return {"analysis_path": "fungal_bacterial"}

def set_pest_path(state: PlantAnalysisState) -> dict:
    return {"analysis_path": "pest"}

def set_stress_path(state: PlantAnalysisState) -> dict:
    return {"analysis_path": "stress"}

def set_healthy_path(state: PlantAnalysisState) -> dict:
    return {"analysis_path": "healthy"}


# ---------------------------------------------------------------------------
# BUILD THE GRAPH
# ---------------------------------------------------------------------------
def build_graph():
    """
    Constructs and compiles the plant analysis StateGraph.
    Returns a compiled graph ready to be invoked.
    """
    graph = StateGraph(PlantAnalysisState)

    # --- Register all nodes ---
    graph.add_node("observe_plant",        observe_plant_node)
    graph.add_node("set_viral",            set_viral_path)
    graph.add_node("set_fungal_bacterial", set_fungal_bacterial_path)
    graph.add_node("set_pest",             set_pest_path)
    graph.add_node("set_stress",           set_stress_path)
    graph.add_node("set_healthy",          set_healthy_path)
    graph.add_node("viral",                viral_node)
    graph.add_node("fungal_bacterial",     fungal_bacterial_node)
    graph.add_node("pest",                 pest_node)
    graph.add_node("stress",               stress_node)
    graph.add_node("care_tips",            care_tips_node)
    graph.add_node("severity_assessment",  severity_assessment_node)

    # --- Entry point ---
    graph.add_edge(START, "observe_plant")

    # --- Conditional edge after observe_plant ---
    graph.add_conditional_edges(
        "observe_plant",
        route_by_condition,
        {
            "viral":            "set_viral",
            "fungal_bacterial": "set_fungal_bacterial",
            "pest":             "set_pest",
            "stress":           "set_stress",
            "healthy":          "set_healthy",
        }
    )

    # --- Each path setter connects to its recommendation node ---
    graph.add_edge("set_viral",            "viral")
    graph.add_edge("set_fungal_bacterial", "fungal_bacterial")
    graph.add_edge("set_pest",             "pest")
    graph.add_edge("set_stress",           "stress")
    graph.add_edge("set_healthy",          "care_tips")

    # --- Diseased/stressed paths go to severity assessment ---
    graph.add_edge("viral",            "severity_assessment")
    graph.add_edge("fungal_bacterial", "severity_assessment")
    graph.add_edge("pest",             "severity_assessment")
    graph.add_edge("stress",           "severity_assessment")

    # --- Healthy path skips severity — goes directly to END ---
    graph.add_edge("care_tips", END)

    # --- Exit after severity ---
    graph.add_edge("severity_assessment", END)

    return graph.compile()


# Compiled graph instance — imported by api/main.py
plant_analysis_graph = build_graph()
