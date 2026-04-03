# Plant Analyzer V2

A full-stack web application that analyzes plant leaf images using AI to deliver condition-specific diagnosis, severity assessment, and targeted care recommendations.

Built with **FastAPI**, **LangGraph**, and **Google Gemini 2.0 Flash**.

---

## What's New in V2

V1 was a simple sequential pipeline — every plant followed the same path regardless of its condition.

V2 wraps a **LangGraph StateGraph** around the pipeline, introducing:

- **Conditional routing** — 5 specialized paths based on detected condition
- **Severity assessment** — scored 1–10 with priority actions and recovery timeline
- **Identification confidence score** — 0–100 with a warning banner for uncertain identifications
- **Condition-differentiated recommendations** — viral infections get isolation advice, not fungicide advice
- **Indoor/outdoor context injection** — environment-aware advice on every path

---

## How It Works

```
[Upload Image]
      ↓
[observe_plant_node]     → identifies plant, detects issues, confidence score
      ↓
[Conditional Routing]
      │
      ├── Healthy        → care tips only (no severity assessment)
      │
      ├── Viral          → isolation + containment advice
      │        ↓
      │   [severity_assessment_node]
      │
      ├── Fungal/Bacterial → treatment + recovery advice
      │        ↓
      │   [severity_assessment_node]
      │
      ├── Pest           → pest control + prevention advice
      │        ↓
      │   [severity_assessment_node]
      │
      └── Stress         → environment correction advice
               ↓
          [severity_assessment_node]
```

Routing decisions are made by developer-written logic, not by the LLM. The LLM generates text — the graph decides what to do next.

---

## Features

- **Plant Identification** — common name, scientific name, family, indoor/outdoor suitability
- **5-Path Conditional Routing** — healthy / viral / fungal-bacterial / pest / stress
- **Severity Assessment** — score (1–10), label, prognosis, priority actions, recovery timeline
- **Identification Confidence** — 0–100 score with low-confidence warning banner
- **Targeted Recommendations** — each condition type gets specialist advice, not generic output
- **Viral Infection Handling** — correctly routes to isolation advice (viral infections have no cure)
- **Drag & Drop Upload** — supports JPG, PNG, WEBP up to 10MB
- **Responsive UI** — works on desktop and mobile

---

## Tech Stack

| Layer     | Technology                        |
|-----------|-----------------------------------|
| Backend   | FastAPI (Python)                  |
| Graph     | LangGraph (StateGraph)            |
| AI        | Google Gemini 2.0 Flash           |
| Frontend  | HTML / CSS / Vanilla JavaScript   |
| Server    | Uvicorn                           |
| Images    | Pillow (preprocessing)            |

---

## Project Structure

```
Plant_Analyzer_V2/
├── api/
│   ├── __init__.py
│   └── main.py                     # FastAPI endpoint — invokes the graph
├── graph/
│   ├── __init__.py                 # Exports plant_analysis_graph
│   ├── state.py                    # PlantAnalysisState (TypedDict)
│   ├── nodes.py                    # Node wrapper functions
│   └── graph.py                    # StateGraph — nodes, edges, routing logic
├── services/
│   ├── __init__.py
│   ├── plant_observations.py       # Gemini: identifies plant, detects issues
│   ├── plant_recommendations.py    # Gemini: condition-specific recommendations
│   └── severity_assessment.py      # Gemini: severity score + priority actions
├── static/
│   ├── index.html                  # Frontend HTML
│   ├── styles.css                  # Frontend styles
│   └── app.js                      # Frontend logic
├── config.py                       # API keys and model configuration
├── requirements.txt                # Python dependencies
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key ([get one here](https://aistudio.google.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nagalakshmi-Pulivarthi/Plant_Analyzer.git
   cd Plant_Analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**

   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Run the Application

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser at `http://localhost:8000`

---

## API

### `POST /analyze`

Accepts a plant leaf image and returns the full analysis.

**Request:** Multipart form data with a `file` field (JPG, PNG, or WEBP)

**Response:**
```json
{
  "plant_observations": {
    "plant_name": "Tomato (Solanum lycopersicum)",
    "plant_family": "Solanaceae",
    "indoor_or_outdoor": "Outdoor",
    "bacteria_or_fungus_detected": "Powdery Mildew",
    "leaf_health": "Moderate fungal infection",
    "nutrient_deficiency_signs": "None detected",
    "pest_damage": "None detected",
    "water_or_sunlight_stress": "None detected",
    "damage_type": "Fungal",
    "identification_confidence": 85
  },
  "analysis_path": "fungal_bacterial",
  "recommendations": { ... },
  "severity_assessment": {
    "severity_score": 6,
    "severity_label": "Moderate",
    "prognosis": "Good chance of recovery if treated within the next week.",
    "priority_actions": ["..."],
    "recovery_timeline": "Expect visible improvement in 2-3 weeks."
  }
}
```

---

## V1 vs V2 — Architecture Comparison

| Feature                     | V1                          | V2                              |
|-----------------------------|-----------------------------|---------------------------------|
| Architecture                | Sequential pipeline         | LangGraph StateGraph            |
| Decision making             | None — always same path     | 2 levels of conditional routing |
| Condition awareness         | Generic prompts             | 5 specialized paths             |
| Viral infection handling    | Given fungicide advice      | Isolation path (no cure)        |
| Severity assessment         | Not present                 | Score 1–10 + actions + timeline |
| Identification confidence   | Not present                 | 0–100 + warning banner          |
| Indoor/outdoor usage        | Detected, ignored           | Injected into all prompts       |
| State management            | Loose variables             | Typed PlantAnalysisState        |
| Frontend                    | Streamlit                   | HTML / CSS / Vanilla JS         |

---

## License

Portfolio and demonstration purposes. Fork freely.
