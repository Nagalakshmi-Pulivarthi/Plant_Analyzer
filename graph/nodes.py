"""
LangGraph Nodes — thin wrappers around existing services.
Each node reads what it needs from PlantAnalysisState,
calls its service, and writes the result back to state.

Services are NOT modified. Nodes are just the bridge between
the graph and the existing business logic.
"""
from graph.state import PlantAnalysisState
from services.plant_observations import analyze_plant_leaf
from services.plant_recommendations import get_recommendations
from services.severity_assessment import assess_severity


# ---------------------------------------------------------------------------
# NODE 1 — Observe Plant
# Reads:  state.image_bytes
# Calls:  analyze_plant_leaf()
# Writes: state.plant_observations
# ---------------------------------------------------------------------------
def observe_plant_node(state: PlantAnalysisState) -> dict:
    """
    Analyzes the plant leaf image using Gemini.
    Returns structured observations about plant identity and health.
    """
    observations = analyze_plant_leaf(state["image_bytes"])
    return {"plant_observations": observations}


# ---------------------------------------------------------------------------
# NODE 2 VARIANTS — Recommendations (one per routing path)
# Reads:  state.plant_observations
# Calls:  get_recommendations() with path-specific prompt context
# Writes: state.recommendations
# ---------------------------------------------------------------------------
def viral_node(state: PlantAnalysisState) -> dict:
    """
    Recommendations for viral infection.
    Focus: isolation, damage control, preventing spread.
    No treatment claims — viral infections have no chemical cure.
    """
    obs = state["plant_observations"]
    context = (
        "IMPORTANT: This plant has a VIRAL infection. "
        "Viral infections in plants have NO chemical cure. "
        "Do NOT recommend fungicides or antibiotics. "
        "ONLY provide recommendations directly related to the viral infection: "
        "isolating the plant, removing infected material, disinfecting tools, "
        "and preventing spread to nearby plants. "
        "Do NOT generate generic care tips unrelated to the infection. "
        "Be honest that the plant may not recover fully."
    )
    return {"recommendations": get_recommendations(obs, context)}


def fungal_bacterial_node(state: PlantAnalysisState) -> dict:
    """
    Recommendations for fungal or bacterial infection.
    Focus: treatment options, pruning, recovery steps.
    """
    obs = state["plant_observations"]
    detected = obs.get("bacteria_or_fungus_detected", "fungal/bacterial infection")
    context = (
        f"This plant has been diagnosed with: {detected}. "
        "ONLY provide recommendations that directly address THIS specific infection. "
        "Do NOT generate generic care tips for issues not observed. "
        "Focus strictly on: the correct treatment for this infection type, "
        "how to prune or remove affected areas, improving conditions to prevent spread, "
        "and a realistic recovery timeline."
    )
    return {"recommendations": get_recommendations(obs, context)}


def pest_node(state: PlantAnalysisState) -> dict:
    """
    Recommendations for pest damage.
    Focus: pest identification, removal, prevention of reinfestation.
    """
    obs = state["plant_observations"]
    detected = obs.get("pest_damage", "pest damage")
    context = (
        f"This plant has: {detected}. "
        "ONLY provide recommendations that directly address THIS specific pest problem. "
        "Do NOT generate generic care tips for issues not observed. "
        "Focus strictly on: identifying the pest from the description, "
        "targeted removal steps, and preventing reinfestation."
    )
    return {"recommendations": get_recommendations(obs, context)}


def stress_node(state: PlantAnalysisState) -> dict:
    """
    Recommendations for environmental stress (water or sunlight).
    Focus: immediate environment correction and recovery.
    """
    obs = state["plant_observations"]
    stress_detail   = obs.get("water_or_sunlight_stress", "environmental stress")
    nutrient_detail = obs.get("nutrient_deficiency_signs", "None")
    indoor_outdoor  = obs.get("indoor_or_outdoor", "unknown").lower()

    # Build a focused list of ONLY the issues actually detected
    detected_issues = [f"Environmental stress: {stress_detail}"]
    if nutrient_detail.lower() not in ("none", "no", ""):
        detected_issues.append(f"Nutrient deficiency: {nutrient_detail}")

    issues_text = "\n".join(f"- {i}" for i in detected_issues)

    context = (
        f"This is an {indoor_outdoor} plant with the following SPECIFIC issues detected:\n"
        f"{issues_text}\n\n"
        "ONLY provide recommendations that directly address these detected issues. "
        "Do NOT recommend treatments for problems that were NOT observed. "
        "Do NOT generate a generic full care guide. "
        "Each recommendation card must map directly to one of the issues listed above."
    )
    return {"recommendations": get_recommendations(obs, context)}


def care_tips_node(state: PlantAnalysisState) -> dict:
    """
    Recommendations for healthy plants.
    Focus: optimal care, maintenance, and preventive tips.
    """
    obs = state["plant_observations"]
    plant_name     = obs.get("plant_name", "this plant")
    indoor_outdoor = obs.get("indoor_or_outdoor", "unknown").lower()

    context = (
        f"This {indoor_outdoor} plant ({plant_name}) is HEALTHY — no issues detected. "
        "Do NOT invent problems or recommend treatments for issues that do not exist. "
        f"Provide care tips specifically tailored to {plant_name} as an {indoor_outdoor} plant: "
        "correct watering frequency, ideal light level, fertilization schedule, "
        "and seasonal maintenance. Keep advice practical and specific to this plant species."
    )
    return {"recommendations": get_recommendations(obs, context)}


# ---------------------------------------------------------------------------
# NODE 3 — Severity Assessment
# Reads:  state.plant_observations, state.analysis_path
# Calls:  assess_severity()
# Writes: state.severity_assessment
# ---------------------------------------------------------------------------
def severity_assessment_node(state: PlantAnalysisState) -> dict:
    """
    Assesses the severity of the plant's condition.
    Produces: severity score (1-10), prognosis,
              priority actions, and recovery timeline.
    """
    obs = state["plant_observations"]
    path = state["analysis_path"]
    assessment = assess_severity(obs, path)
    return {"severity_assessment": assessment}
