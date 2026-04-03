"""
PlantAnalysisState — the shared state object that travels through
every node in the LangGraph workflow.
"""
from typing import Dict, Any, Optional
from typing_extensions import TypedDict


class PlantAnalysisState(TypedDict, total=False):
    """
    Single typed object carrying all data through the plant analysis graph.
    Each node reads from this state and writes its result back to it.

    total=False means all fields are optional at initialization.
    Only image_bytes is required at the start — everything else
    gets filled as the graph runs through each node.
    """

    # --- INPUT ---
    # Raw image bytes uploaded by the user
    image_bytes: bytes

    # --- NODE 1 OUTPUT ---
    # Structured observations returned by analyze_plant_leaf()
    # Contains: plant_name, plant_family, indoor_or_outdoor,
    #           bacteria_or_fungus_detected, leaf_health,
    #           nutrient_deficiency_signs, pest_damage,
    #           water_or_sunlight_stress, damage_type
    plant_observations: Optional[Dict[str, Any]]

    # --- ROUTING ---
    # Set by the conditional edge after observe_plant_node
    # Values:
    #   "viral"            → isolation + damage control recommendations
    #   "fungal_bacterial" → treatment + recovery recommendations
    #   "pest"             → pest removal + prevention recommendations
    #   "stress"           → watering/light fix + recovery recommendations
    #   "healthy"          → optimal care + prevention recommendations
    analysis_path: Optional[str]

    # --- NODE 2 OUTPUT ---
    # Recommendations returned by get_recommendations()
    # Contains: ProblemDescription, Recommendations[], FinalSummary
    recommendations: Optional[Dict[str, Any]]

    # --- NODE 3 OUTPUT ---
    # Severity assessment returned by assess_severity()
    # Contains: severity_score (1-10), severity_label, prognosis,
    #           priority_actions[], recovery_timeline
    severity_assessment: Optional[Dict[str, Any]]
