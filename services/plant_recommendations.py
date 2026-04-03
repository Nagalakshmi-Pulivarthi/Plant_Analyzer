"""
Service for generating plant problem diagnosis and recommendations using Google AI.
"""
import json
import os
from typing import Dict, Any
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_RECOMMENDATIONS_MODEL, validate_config


def get_recommendations(plant_observations: Dict[str, Any], context: str = "") -> Dict[str, Any]:
    """
    Analyze plant observations and generate problem diagnosis and recommendations.

    Args:
        plant_observations: Dictionary containing plant observation data from Gemini
        context: Optional path-specific instruction injected by the graph node.
                 Tells the LLM what type of condition to focus on
                 (viral, fungal, pest, stress, or healthy care).

    Returns:
        Dictionary containing problem description, recommendations, and final summary
    """
    validate_config()

    client = genai.Client(api_key=GEMINI_API_KEY)

    # Convert observations to JSON string for input
    observations_json = json.dumps(plant_observations, indent=2)

    # Inject path-specific context if provided by the graph node
    context_block = f"\nContext from analysis routing:\n{context}\n" if context else ""

    user_prompt = f"""Analyze the following plant observation data and provide diagnosis and recommendations:
{context_block}
{observations_json}

Based on this information, identify any problems and provide actionable recommendations."""

    system_instruction = """You are a plant specialist. Use the provided JSON input to analyze the plant image, diagnose any issues, and generate recommendations. Include relevant icons for each recommendation (e.g., water → 💧, sunlight → ☀️, fertilizer → 🌱, pruning → ✂️, temperature → 🌡️). 
Output must be in JSON format only, following this structure:

{
  "ProblemDescription": "Detailed description of identified problems",
  "Recommendations": [
    {
      "Icon": "💧",
      "Heading": "Watering",
      "Description": "Detailed recommendation about watering"
    }
  ],
  "FinalSummary": "A comprehensive summary of the diagnosis and recommendations"
}

Do not add any extra text outside the JSON response. 
Do not include sources."""

    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=user_prompt),
                ],
            ),
        ]
        
        generate_content_config = types.GenerateContentConfig(
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
        
        # Parse JSON response
        # Sometimes the response might have markdown code blocks
        if "```json" in full_response:
            full_response = full_response.split("```json")[1].split("```")[0].strip()
        elif "```" in full_response:
            full_response = full_response.split("```")[1].split("```")[0].strip()
        
        result = json.loads(full_response)
        return result
        
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing recommendations JSON: {str(e)}\nResponse: {full_response}")
    except Exception as e:
        raise Exception(f"Error generating recommendations: {str(e)}")

