"""
Summary cards component showing key metrics.
"""
import streamlit as st
from data.queries import get_summary_metrics


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
            "icon": "🏫",
            "label": "Schools",
            "value": metrics.get("schools", 236),
            "delta": None,
            "help": "Total active schools in SchoolPilot"
        },
        {
            "icon": "👩‍🏫",
            "label": "Teachers",
            "value": metrics.get("teachers", 599),
            "delta": None,
            "help": "Total registered teachers"
        },
        {
            "icon": "🤖",
            "label": "AI Sessions",
            "value": metrics.get("ai_sessions", 128),
            "delta": "+12",
            "help": "Rumi coaching sessions completed"
        },
        {
            "icon": "👁️",
            "label": "Human Obs",
            "value": metrics.get("human_observations", 576),
            "delta": "+8",
            "help": "Human coach observations"
        },
        {
            "icon": "📊",
            "label": "Avg Score",
            "value": f"{metrics.get('avg_score', 72.3)}%",
            "delta": "+2.1%",
            "help": "Average teaching quality score"
        },
        {
            "icon": "👨‍🎓",
            "label": "Students",
            "value": f"{metrics.get('students', 16898):,}",
            "delta": None,
            "help": "Total students in SchoolPilot"
        }
    ]

    for col, card in zip(cols, cards):
        with col:
            render_card(
                icon=card["icon"],
                label=card["label"],
                value=card["value"],
                delta=card.get("delta"),
                help_text=card.get("help")
            )


def render_card(icon: str, label: str, value, delta: str = None, help_text: str = None):
    """
    Render a single metric card.

    Args:
        icon: Emoji icon
        label: Metric label
        value: Metric value
        delta: Change indicator (optional)
        help_text: Hover help text (optional)
    """
    delta_html = ""
    if delta:
        color = "#10B981" if delta.startswith("+") else "#EF4444"
        delta_html = f'<span style="color: {color}; font-size: 0.875rem; margin-left: 8px;">{delta}</span>'

    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <span style="font-size: 1.5rem;">{icon}</span>
            <span class="metric-label">{label}</span>
        </div>
        <div>
            <span class="metric-value">{value}</span>
            {delta_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Add spacing
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
