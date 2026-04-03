"""
FastAPI backend for Plant Leaf Analyzer V2.
Orchestration is handled by the LangGraph workflow in graph/graph.py.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict, Any
import os

from graph import plant_analysis_graph
from config import MAX_IMAGE_SIZE_MB, ALLOWED_IMAGE_TYPES

app = FastAPI(
    title="Plant Leaf Analyzer",
    description="Web application for analyzing plant leaf images and providing diagnosis",
    version="2.0.0"
)

# CORS middleware (kept for API access from other origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page."""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Plant Leaf Analyzer API is running", "note": "Static files not found"}


@app.post("/analyze")
async def analyze_plant(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Analyze a plant leaf image using the LangGraph workflow.

    The graph handles:
    1. Plant observation  — identify plant, detect issues
    2. Conditional routing — viral | fungal_bacterial | pest | stress | healthy
    3. Targeted recommendations — path-specific advice
    4. Severity assessment — score, prognosis, priority actions, recovery timeline

    Returns:
        plant_observations, analysis_path, recommendations, severity_assessment
    """
    try:
        # Read and validate image
        image_bytes = await file.read()

        if not image_bytes or len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty or could not be read. Please ensure you're uploading a valid image file."
            )

        if file.content_type and file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )

        size_mb = len(image_bytes) / (1024 * 1024)
        if size_mb > MAX_IMAGE_SIZE_MB:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {MAX_IMAGE_SIZE_MB}MB"
            )

        # Invoke the LangGraph workflow
        # The graph runs all nodes and routing internally
        final_state = plant_analysis_graph.invoke(
            {"image_bytes": image_bytes}
        )

        # Build response from final state
        result = {
            "plant_observations": final_state.get("plant_observations"),
            "analysis_path":      final_state.get("analysis_path"),
            "recommendations":    final_state.get("recommendations"),
            "severity_assessment": final_state.get("severity_assessment"),
        }

        return JSONResponse(content=result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing plant: {str(e)}"
        )


@app.post("/analyze/observations")
async def analyze_observations_only(
    file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Analyze plant leaf image and return only observations (without recommendations or healthy image).
    Useful for testing or partial analysis.
    """
    try:
        # Read image bytes first (before validation to ensure file is readable)
        image_bytes = await file.read()
        
        # Validate that file was read successfully
        if not image_bytes or len(image_bytes) == 0:
            raise HTTPException(
                status_code=400,
                detail="File is empty or could not be read. Please ensure you're uploading a valid image file."
            )
        
        # Validate file type (check content_type, but also allow if None and validate by file signature)
        if file.content_type and file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Allowed types: {', '.join(ALLOWED_IMAGE_TYPES)}"
            )
        
        # Analyze plant leaf
        plant_observations = analyze_plant_leaf(image_bytes)
        
        return JSONResponse(content=plant_observations)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing plant: {str(e)}"
        )

