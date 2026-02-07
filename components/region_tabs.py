"""
Region tabs component - consistent across all pages.
Provides horizontal tabs for ICT, Balochistan, RWP, Moawin, Rumi.
"""
import streamlit as st
from typing import Tuple


# Region configuration with metadata
REGIONS = {
    "ICT": {
        "icon": "🏛️",
        "label": "ICT (Islamabad)",
        "description": "Federal Capital - TEACH observations, 9,981 teachers",
        "database": "BigQuery",
        "key_metric": "teachers"
    },
    "Balochistan": {
        "icon": "🏔️",
        "label": "Balochistan",
        "description": "Winter School FLN - AI + Human observations",
        "database": "Neon PostgreSQL",
        "key_metric": "observations"
    },
    "Rawalpindi": {
        "icon": "🏫",
        "label": "Rawalpindi",
        "description": "Prevail Longitudinal Study - Early stage",
        "database": "BigQuery",
        "key_metric": "events"
    },
    "Moawin": {
        "icon": "📋",
        "label": "Moawin",
        "description": "SchoolPilot - Attendance & compliance",
        "database": "Neon PostgreSQL",
        "key_metric": "attendance"
    },
    "Rumi": {
        "icon": "🤖",
        "label": "Rumi",
        "description": "AI Coaching - Chat sessions & lesson plans",
        "database": "Supabase",
        "key_metric": "messages"
    }
}


def render_region_tabs() -> Tuple:
    """
    Render the 5 region tabs.

    Returns:
        Tuple of 5 tab containers (ict, balochistan, rwp, moawin, rumi)
    """
    return st.tabs([
        f"{REGIONS['ICT']['icon']} ICT",
        f"{REGIONS['Balochistan']['icon']} Balochistan",
        f"{REGIONS['Rawalpindi']['icon']} Rawalpindi",
        f"{REGIONS['Moawin']['icon']} Moawin",
        f"{REGIONS['Rumi']['icon']} Rumi"
    ])


def get_region_info(region: str) -> dict:
    """
    Get metadata for a specific region.

    Args:
        region: Region key (ICT, Balochistan, Rawalpindi, Moawin, Rumi)

    Returns:
        Dict with icon, label, description, database, key_metric
    """
    return REGIONS.get(region, {})


def render_region_header(region: str) -> None:
    """
    Render a small header showing the current region context.

    Args:
        region: Region key
    """
    info = REGIONS.get(region, {})
    if info:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; padding: 0.5rem 0;">
            <span style="font-size: 1.25rem;">{info['icon']}</span>
            <div>
                <div style="font-size: 0.875rem; font-weight: 600; color: #1A1A1A;">{info['label']}</div>
                <div style="font-size: 0.75rem; color: #6B7280;">{info['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
