"""
Service for analyzing plant leaf images using Google AI Studio (Gemini).
"""
import json
from io import BytesIO
from typing import Dict, Any
from PIL import Image
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_OBSERVATIONS_MODEL, validate_config


def _detect_image_format(image_bytes: bytes) -> str:
    """Detect image format from bytes."""
    try:
        # Use Pillow to detect image format
        image = Image.open(BytesIO(image_bytes))
        format_map = {
            'JPEG': 'image/jpeg',
            'PNG': 'image/png',
            'GIF': 'image/gif',
            'WEBP': 'image/webp'
        }
        return format_map.get(image.format, 'image/jpeg')  # Default to JPEG
    except Exception:
        # If detection fails, default to JPEG
        return 'image/jpeg'


def analyze_plant_leaf(image_bytes: bytes) -> Dict[str, Any]:
    """
    Analyze a plant leaf image and return observations.
    
    Args:
        image_bytes: The image file as bytes
        
    Returns:
        Dictionary containing plant_name, plant_family, indoor_or_outdoor, bacteria_or_fungus_detected,
        leaf_health, nutrient_deficiency_signs, pest_damage, water_or_sunlight_stress, and damage_type
    """
    validate_config()
    
    # Validate image bytes
    if image_bytes is None:
        raise ValueError("Image bytes are None")
    if not isinstance(image_bytes, bytes):
        raise ValueError(f"Expected bytes, got {type(image_bytes)}")
    if len(image_bytes) == 0:
        raise ValueError("Image bytes are empty (length is 0)")
    
    # Validate and process image before encoding
    try:
        # Verify image can be opened and processed
        image = Image.open(BytesIO(image_bytes))
        # Convert to RGB if necessary (handles RGBA, LA, P, etc.)
        if image.mode in ('RGBA', 'LA'):
            # Create a white background for transparency
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[-1] if len(image.split()) > 1 else None)
            image = rgb_image
        elif image.mode != 'RGB':
            # Convert any other mode (P, CMYK, etc.) to RGB
            image = image.convert('RGB')
        
        # Save processed image to bytes as JPEG
        output = BytesIO()
        image.save(output, format='JPEG', quality=95, optimize=True)
        processed_image_bytes = output.getvalue()
    except Exception as e:
        raise ValueError(f"Invalid image data: {str(e)}")
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Use JPEG MIME type since we're always converting to JPEG
    image_mime = 'image/jpeg'
    
    system_instruction = """You are a Plant Leaf Health Analyzer. Analyze a single plant-leaf image and return a structured, evidence-based assessment. Base all conclusions only on what is visually observable in the image.
Input
{Image}: Base 64 string of the image

For each field, provide 1–2 sentence justifications tied to visible features such as color, spots, texture, holes, patterns, or shape. If a field cannot be determined, use "Unknown" or "Unclear" and briefly state why.

Return your answer strictly in the JSON format below. Do not include any extra text.

JSON Output Format
{
  "plant_name": "",
  "plant_family": "",
  "indoor_or_outdoor": "",
  "bacteria_or_fungus_detected": "",
  "leaf_health": "",
  "nutrient_deficiency_signs": "",
  "pest_damage": "",
  "water_or_sunlight_stress": "",
  "damage_type": "",
  "identification_confidence": 0
}

Field Guidelines

plant_name: Common and scientific name (e.g., "Tomato (Solanum lycopersicum)")

plant_family: Taxonomic family (e.g., "Solanaceae")

indoor_or_outdoor: Likely environment ("Indoor" or "Outdoor")

bacteria_or_fungus_detected: Any visible infection (e.g., "Powdery Mildew", "None")

leaf_health: Overall health summary (e.g., "Healthy", "Moderate chlorosis", "Severe necrosis")

nutrient_deficiency_signs: Signs of nutrient issues (e.g., "Nitrogen deficiency – yellowing")

pest_damage: Visible insect/pest damage (e.g., "Chewing holes from caterpillars")

water_or_sunlight_stress: Signs of water/light stress (e.g., "Underwatered – curling")

damage_type: Physical/mechanical damage (e.g., "Wind damage", "Mechanical tear")

identification_confidence: Integer 0-100 representing how confident you are in the plant identification.
  Score based on:
    - Image clarity (blurry or dark image = lower score)
    - Leaf visibility (partial leaf, multiple plants = lower score)
    - Distinctiveness of the species (common, easily identified = higher score)
    - Stress/damage obscuring features (heavy damage = lower score)
  Guide: 90-100 = very certain | 70-89 = confident | 50-69 = uncertain | below 50 = very uncertain"""

    try:
        # Create image part for Gemini
        image_part = types.Part.from_bytes(
            data=processed_image_bytes,
            mime_type=image_mime
        )
        
        # Create user prompt
        user_prompt = "Analyze this plant leaf image and provide the detailed analysis in the specified JSON format."
        
        # Configure generation settings
        generate_content_config = types.GenerateContentConfig(
            top_p=1,
            system_instruction=[
                types.Part.from_text(text=system_instruction)
            ],
        )
        
        # Create contents with image and text
        contents = [
            types.Content(
                role="user",
                parts=[
                    image_part,
                    types.Part.from_text(text=user_prompt)
                ]
            )
        ]
        
        # Generate content using Gemini
        response = client.models.generate_content(
            model=GEMINI_OBSERVATIONS_MODEL,
            contents=contents,
            config=generate_content_config
        )
        
        # Extract text content from response
        if not response.text:
            raise ValueError("No response text from Gemini API")
        
        content = response.text
        
        # Try to parse JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract JSON from markdown code blocks
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
                result = json.loads(json_str)
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
                result = json.loads(json_str)
            else:
                # Last resort: try to find JSON object in the text
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    raise ValueError("Could not parse JSON from response")
        
        return result
        
    except Exception as e:
        raise Exception(f"Error analyzing plant leaf: {str(e)}")

