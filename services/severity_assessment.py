"""
Service for assessing plant condition severity using Google Gemini.
Produces a severity score, prognosis, priority actions, and recovery timeline
based on the plant observations from the analysis step.
"""
import json
from typing import Dict, Any
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_RECOMMENDATIONS_MODEL, validate_config


def assess_severity(plant_observations: Dict[str, Any], analysis_path: str) -> Dict[str, Any]:
    """
    Assess the severity of the plant's condition based on observations.

    Args:
        plant_observations: Structured observations from analyze_plant_leaf()
        analysis_path: The routing decision — viral | fungal_bacterial |
                       pest | stress | healthy

    Returns:
        Dictionary containing:
            severity_score    → int 1-10 (1=minimal, 10=critical)
            severity_label    → "Low" | "Moderate" | "High" | "Critical"
            prognosis         → honest recovery outlook
            priority_actions  → ordered list of what to do first
            recovery_timeline → expected timeframe if actions are followed
    """
    validate_config()

    client = genai.Client(api_key=GEMINI_API_KEY)

    observations_json = json.dumps(plant_observations, indent=2)

    # Tailor the prompt context based on routing path
    path_context = {
        "viral": (
            "This plant has been identified as having a VIRAL infection. "
            "Viral infections in plants have no chemical cure. "
            "Severity should reflect spread risk and plant viability. "
            "Priority actions must focus on isolation, removal of infected material, "
            "and preventing spread to nearby plants."
        ),
        "fungal_bacterial": (
            "This plant has a FUNGAL or BACTERIAL infection. "
            "These are treatable with appropriate intervention. "
            "Severity should reflect how advanced the infection is. "
            "Priority actions must focus on treatment, pruning, and recovery."
        ),
        "pest": (
            "This plant has visible PEST DAMAGE. "
            "Severity should reflect the extent of infestation and damage. "
            "Priority actions must focus on pest identification, removal, "
            "and prevention of reinfestation."
        ),
        "stress": (
            "This plant is showing ENVIRONMENTAL STRESS (water or sunlight). "
            "Stress conditions are reversible with correct care adjustments. "
            "Severity should reflect how long the stress has been occurring. "
            "Priority actions must focus on immediate environment correction."
        ),
        "healthy": (
            "This plant appears HEALTHY with no significant issues detected. "
            "Severity score should be very low (1-2). "
            "Priority actions should focus on maintaining current health "
            "and preventive care."
        ),
    }

    context = path_context.get(analysis_path, path_context["healthy"])

    user_prompt = f"""Assess the severity of this plant's condition based on the observations below.

{context}

Plant Observations:
{observations_json}

Provide a structured severity assessment. Be honest and precise.
Do not exaggerate severity. Do not downplay serious conditions."""

    system_instruction = """You are a plant health specialist conducting a severity assessment.
Based on the plant observations provided, return a structured JSON severity report.

Scoring guide:
  1-2  → Minimal. Plant is healthy or very minor issue.
  3-4  → Low. Small issue, easily corrected.
  5-6  → Moderate. Noticeable problem, needs attention soon.
  7-8  → High. Serious condition, act quickly.
  9-10 → Critical. Severe damage, plant survival at risk.

Return ONLY valid JSON in this exact format:
{
  "severity_score": 6,
  "severity_label": "Moderate",
  "prognosis": "Good chance of recovery if treated within the next week.",
  "priority_actions": [
    "1. Remove all visibly infected leaves immediately",
    "2. Apply copper-based fungicide to remaining foliage",
    "3. Improve air circulation around the plant",
    "4. Avoid overhead watering to reduce moisture on leaves"
  ],
  "recovery_timeline": "Expect visible improvement in 2-3 weeks with consistent treatment."
}

Do not add any text outside the JSON."""

    try:
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_prompt)],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=0,  # deterministic — same input always produces same score
            system_instruction=[
                types.Part.from_text(text=system_instruction),
            ],
        )

        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=GEMINI_RECOMMENDATIONS_MODEL,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.text:
                full_response += chunk.text

        # Strip markdown code blocks if present
        if "```json" in full_response:
            full_response = full_response.split("```json")[1].split("```")[0].strip()
        elif "```" in full_response:
            full_response = full_response.split("```")[1].split("```")[0].strip()

        result = json.loads(full_response)
        return result

    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing severity assessment JSON: {str(e)}\nResponse: {full_response}")
    except Exception as e:
        raise Exception(f"Error assessing severity: {str(e)}")
