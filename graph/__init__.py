"""
graph package — LangGraph workflow for Plant Analyzer V2.

Exports the compiled graph instance for use in api/main.py.
"""
from graph.graph import plant_analysis_graph

__all__ = ["plant_analysis_graph"]
