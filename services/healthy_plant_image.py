"""
Service for generating healthy plant images using Google AI.
"""
import base64
import io
import mimetypes
from typing import Optional, Tuple
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_IMAGE_MODEL, validate_config


def generate_healthy_plant_image(plant_name: str) -> Tuple[bytes, str]:
    """
    Generate an image of a healthy version of the plant.
    
    Args:
        plant_name: Name or category of the plant
        
    Returns:
        Tuple of (image_bytes, mime_type)
    """
    validate_config()
    
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    user_prompt = f"Generate a high-quality, realistic image of a healthy {plant_name} plant. The image should show the plant in its optimal condition with vibrant, healthy leaves."
    
    system_instruction = """Generate a realistic, high-quality image of the plant based on the input given by the user.
Input: plant_species_or_category
Output: A photorealistic image of a healthy plant"""

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
            response_modalities=[
                "IMAGE",
                "TEXT",
            ],
            system_instruction=[
                types.Part.from_text(text=system_instruction),
            ],
        )

        image_data = None
        mime_type = "image/png"
        
        for chunk in client.models.generate_content_stream(
            model=GEMINI_IMAGE_MODEL,
            contents=contents,
            config=generate_content_config,
        ):
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                image_data = inline_data.data
                mime_type = inline_data.mime_type or "image/png"
                break
        
        if image_data is None:
            raise Exception("No image data received from API")
        
        return image_data, mime_type
        
    except Exception as e:
        raise Exception(f"Error generating healthy plant image: {str(e)}")

