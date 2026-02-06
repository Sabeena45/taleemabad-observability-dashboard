"""
Summary cards component showing key metrics.
Uses centralized design system for consistent styling.
"""
import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.queries import get_summary_metrics
from styles.design_system import metric_card, COLORS


def render_summary_cards(filters: dict):
    """
    Render summary metric cards at the top of the dashboard.

    Args:
        filters: Dictionary of selected filter values
    """
    # Get metrics (will be replaced with live data)
    metrics = get_summary_metrics(filters)

    # Create 6-column layout for cards
    cols = st.columns(6)

    cards = [
        {
            "label": "Schools",
            "value": str(metrics.get("schools", 236)),
            "color": None
        },
        {
            "label": "Teachers",
            "value": str(metrics.get("teachers", 599)),
            "color": None
        },
        {
            "label": "AI Sessions",
            "value": str(metrics.get("ai_sessions", 128)),
            "color": COLORS['info']
        },
        {
            "label": "Human Obs",
            "value": str(metrics.get("human_observations", 576)),
            "color": COLORS['success']
        },
        {
            "label": "Avg Score",
            "value": f"{metrics.get('avg_score', 72.3)}%",
            "color": COLORS['success']
        },
        {
            "label": "Students",
            "value": f"{metrics.get('students', 16898):,}",
            "color": None
        }
    ]

    for col, card in zip(cols, cards):
        with col:
            st.markdown(
                metric_card(card["value"], card["label"], card.get("color")),
                unsafe_allow_html=True
            )
