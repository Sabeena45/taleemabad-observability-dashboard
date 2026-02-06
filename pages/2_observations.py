"""
Observations page - AI vs Human observation comparison.

Design: Minimalist, insight-first approach following Tufte principles.
Uses centralized design system for consistent styling.
"""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from data.queries import get_observation_counts, get_observation_trend
from styles.design_system import (
    inject_css,
    hero_metric,
    status_bar,
    divider,
    section_title,
    insight_card,
    metric_card,
    obs_card,
    COLORS,
    plotly_layout_defaults,
    score_color
)

st.set_page_config(
    page_title="Observations | Taleemabad",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === INJECT DESIGN SYSTEM ===
inject_css()


def main():
    filters = render_sidebar()

    # === STATUS BAR ===
    st.markdown(status_bar(filters["region"], "Observations"), unsafe_allow_html=True)

    # Get data
    obs_counts = get_observation_counts(filters)

    # === HERO: AI Multiplier ===
    if obs_counts['human_count'] > 0:
        multiplier = obs_counts['ai_count'] / obs_counts['human_count']
    else:
        multiplier = obs_counts['ai_count']

    st.markdown(
        hero_metric(
            f"{multiplier:.1f}×",
            "AI Observation Multiplier",
            f'{obs_counts["ai_count"]} AI sessions vs {obs_counts["human_count"]} human observations',
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            metric_card(str(obs_counts["ai_count"]), "AI Sessions", COLORS['info']),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card(str(obs_counts["human_count"]), "Human Observations", COLORS['success']),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            metric_card(str(obs_counts["total"]), "Total"),
            unsafe_allow_html=True
        )

    st.markdown(divider(), unsafe_allow_html=True)

    # === TABS ===
    tab1, tab2, tab3 = st.tabs(["Trends", "Comparison", "Recent"])

    with tab1:
        render_trend_view(filters)

    with tab2:
        render_comparison_view(filters)

    with tab3:
        render_recent_observations(filters)


def render_trend_view(filters):
    """Weekly observation trend with smooth spline curves."""

    st.markdown(section_title("Weekly Volume"), unsafe_allow_html=True)

    trend_data = get_observation_trend(filters)

    weeks = [d['week'] for d in trend_data]
    ai_counts = [d['ai'] for d in trend_data]
    human_counts = [d['human'] for d in trend_data]

    fig = go.Figure()

    # AI trend - spline with subtle area fill
    fig.add_trace(go.Scatter(
        x=weeks,
        y=ai_counts,
        mode='lines+markers',
        name='AI',
        line=dict(color=COLORS['info'], width=2, shape='spline'),
        marker=dict(size=6, color=COLORS['info'], line=dict(color='white', width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.06)'
    ))

    # Human trend - spline without fill
    fig.add_trace(go.Scatter(
        x=weeks,
        y=human_counts,
        mode='lines+markers',
        name='Human',
        line=dict(color=COLORS['success'], width=2, shape='spline'),
        marker=dict(size=6, color=COLORS['success'], line=dict(color='white', width=1.5))
    ))

    base_layout = plotly_layout_defaults(height=280)
    fig.update_layout(
        **base_layout,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=11, family="Inter, -apple-system, sans-serif")
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#F3F4F6', zeroline=False),
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Insight
    total_ai = sum(ai_counts)
    total_human = sum(human_counts)

    st.markdown(
        insight_card(
            f'Over this period: <strong style="color: {COLORS["info"]};">{total_ai}</strong> AI sessions '
            f'delivered <strong>{total_ai / max(total_human, 1):.1f}×</strong> the coverage of '
            f'<strong style="color: {COLORS["success"]};">{total_human}</strong> human observations.'
        ),
        unsafe_allow_html=True
    )


def render_comparison_view(filters):
    """AI vs Human comparison - strengths and limitations."""

    st.markdown(section_title("Strengths & Limitations"), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            insight_card(
                '''<table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">24-48 hour feedback turnaround</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Consistent scoring criteria</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Unlimited scalability</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Non-intrusive (natural teaching)</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#F59E0B;">⚠</td><td style="padding:0.5rem 0;">Audio-only analysis</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#F59E0B;">⚠</td><td style="padding:0.5rem 0;">Cannot see visual aids</td></tr>
                </table>''',
                border_color=COLORS['info'],
                title="AI Observations (Rumi)"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            insight_card(
                '''<table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Full classroom context</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Visual + non-verbal cues</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Relationship building</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#10B981;">✓</td><td style="padding:0.5rem 0;">Real-time intervention</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#F59E0B;">⚠</td><td style="padding:0.5rem 0;">Expensive (travel, time)</td></tr>
                    <tr><td style="padding:0.5rem 0; color:#F59E0B;">⚠</td><td style="padding:0.5rem 0;">Infrequent (quarterly)</td></tr>
                </table>''',
                border_color=COLORS['success'],
                title="Human Observations"
            ),
            unsafe_allow_html=True
        )

    # Agreement analysis for Balochistan
    if filters['region'] == 'Balochistan' or filters['region'] == 'Combined':
        st.markdown(divider(), unsafe_allow_html=True)

        st.markdown(section_title("AI-Human Agreement (Balochistan Winter School)"), unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                metric_card("46%", "Agreement Rate", COLORS['warning']),
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                metric_card("12%", "AI Rated Higher", COLORS['muted']),
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                metric_card("42%", "Human Rated Higher", COLORS['error']),
                unsafe_allow_html=True
            )

        st.markdown(
            insight_card(
                f'<strong style="color: {COLORS["warning"]};">54 percentage point gap</strong> between AI and human ratings. '
                'AI may be more critical OR human coaches may be more lenient. Further validation needed.',
                border_color=COLORS['warning'],
                title="Key Finding"
            ),
            unsafe_allow_html=True
        )


def render_recent_observations(filters):
    """Recent observations list with styled cards."""

    st.markdown(section_title("Recent Activity"), unsafe_allow_html=True)

    # Sample data
    observations = [
        {"date": "2026-01-21", "type": "AI", "school": "GMS Rawalpindi #12", "teacher": "Mahjabeen", "subject": "Mathematics", "score": 72},
        {"date": "2026-01-20", "type": "AI", "school": "GMS Islamabad #5", "teacher": "Fatima", "subject": "English", "score": 68},
        {"date": "2026-01-19", "type": "Human", "school": "GPS Balochistan #8", "teacher": "Ahmed", "subject": "Science", "score": 75},
        {"date": "2026-01-18", "type": "AI", "school": "GMS Rawalpindi #3", "teacher": "Ayesha", "subject": "Urdu", "score": 71},
        {"date": "2026-01-17", "type": "Human", "school": "GPS Balochistan #2", "teacher": "Zara", "subject": "Mathematics", "score": 65},
    ]

    for obs in observations:
        obs_type = obs['type']
        border_color = COLORS['info'] if obs_type == 'AI' else COLORS['success']
        sc = score_color(obs['score'], 70)

        st.markdown(
            obs_card(
                teacher=obs["teacher"],
                school=obs["school"],
                subject=obs["subject"],
                score=obs["score"],
                date=obs["date"],
                obs_type=obs_type,
                border_color=border_color,
                score_color=sc
            ),
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
