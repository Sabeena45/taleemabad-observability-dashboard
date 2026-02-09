"""
Observations page - AI vs Human observation comparison.

Design: Minimalist, insight-first approach following Tufte principles.
Uses centralized design system for consistent styling.
Region tabs at top for cross-region analysis.
"""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from components.region_tabs import render_region_tabs, REGIONS
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

    # === PAGE HEADER ===
    st.markdown(
        '<div style="margin-bottom: 1rem;">'
        '<div style="font-size: 0.625rem; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.15em;">TALEEMABAD</div>'
        '<div style="font-size: 1.5rem; font-weight: 600; color: #1A1A1A; margin-top: 0.25rem;">Observations</div>'
        '<div style="font-size: 0.875rem; color: #6B7280;">AI vs Human Coaching Analytics by Region</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # === REGION TABS ===
    tab_ict, tab_bal, tab_rwp, tab_moawin, tab_rumi = render_region_tabs()

    with tab_ict:
        render_region_observations("ICT", filters)

    with tab_bal:
        render_region_observations("Balochistan", filters)

    with tab_rwp:
        render_region_observations("Rawalpindi", filters)

    with tab_moawin:
        render_region_observations("Moawin", filters)

    with tab_rumi:
        render_region_observations("Rumi", filters)


def render_region_observations(region: str, filters: dict):
    """Render observation analytics for a specific region."""
    # Update filters with specific region
    region_filters = {**filters, "region": region}

    # Region-specific observation data
    if region == "ICT":
        obs_counts = {"ai_count": 0, "human_count": 2423, "total": 2423}
        render_ict_observations(region_filters, obs_counts)

    elif region == "Balochistan":
        obs_counts = {"ai_count": 522, "human_count": 54, "total": 576}
        render_balochistan_observations(region_filters, obs_counts)

    elif region == "Rawalpindi":
        obs_counts = {"ai_count": 0, "human_count": 0, "total": 0}
        render_rwp_observations(region_filters, obs_counts)

    elif region == "Moawin":
        render_moawin_observations(region_filters)

    elif region == "Rumi":
        render_rumi_observations(region_filters)


def render_ict_observations(filters, obs_counts):
    """ICT observations - TEACH tool data from BigQuery."""

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{obs_counts['human_count']:,}",
            "TEACH Observations",
            "Federal Capital classroom observations (2020-2024)",
            color=COLORS['success']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            metric_card("9,981", "Teachers Observed", COLORS['info']),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card("3.12", "Avg Score (Certified)", COLORS['success']),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            metric_card("2.80", "Avg Score (Non-Certified)", COLORS['warning']),
            unsafe_allow_html=True
        )

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            '<strong>10.2% improvement</strong> in classroom observation scores for certified teachers vs non-certified. '
            'Effect size: 0.46 (medium-large), demonstrating <strong>$50-100 per teacher</strong> ROI.',
            border_color=COLORS['success'],
            title="Certification Impact"
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === DATA SOURCE NOTE ===
    st.markdown(
        '<div style="background: #F3F4F6; padding: 1rem; border-radius: 8px; font-size: 0.875rem; color: #6B7280;">'
        '<strong>Data Source:</strong> BigQuery TEACH_TOOL_OBSERVATION_CLEANED table. '
        'Human coach observations only - AI observation system not deployed in ICT.'
        '</div>',
        unsafe_allow_html=True
    )


def render_balochistan_observations(filters, obs_counts):
    """Balochistan observations - AI + Human from Neon PostgreSQL."""

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
    tab1, tab2, tab3 = st.tabs(["Trends", "AI vs Human", "Recent"])

    with tab1:
        render_trend_view(filters)

    with tab2:
        render_comparison_view(filters)

    with tab3:
        render_recent_observations(filters, "Balochistan")


def render_rwp_observations(filters, obs_counts):
    """Rawalpindi observations - early stage."""

    st.markdown(
        '<div style="text-align: center; padding: 4rem 2rem; background: #F9FAFB; border-radius: 12px; margin: 2rem 0;">'
        '<div style="font-size: 3rem; margin-bottom: 1rem;">&#127979;</div>'
        '<div style="font-size: 1.25rem; font-weight: 600; color: #1A1A1A; margin-bottom: 0.5rem;">'
        'Observation System Launching Soon'
        '</div>'
        '<div style="font-size: 0.875rem; color: #6B7280; max-width: 400px; margin: 0 auto;">'
        'Rawalpindi Prevail longitudinal study is in early deployment phase. '
        'Observation data collection will begin Q2 2026.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Current stats
    st.markdown(divider(), unsafe_allow_html=True)
    st.markdown(section_title("Current Status"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(metric_card("21", "Schools Enrolled", COLORS['info']), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("143", "Teachers Onboarded", COLORS['success']), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("444K", "App Events", COLORS['warning']), unsafe_allow_html=True)


def render_moawin_observations(filters):
    """Moawin/SchoolPilot - not observation-focused."""

    info = REGIONS.get("Moawin", {})

    st.markdown(
        '<div style="text-align: center; padding: 4rem 2rem; background: #F9FAFB; border-radius: 12px; margin: 2rem 0;">'
        '<div style="font-size: 3rem; margin-bottom: 1rem;">' + info.get('icon', '📋') + '</div>'
        '<div style="font-size: 1.25rem; font-weight: 600; color: #1A1A1A; margin-bottom: 0.5rem;">'
        'Different Data Focus'
        '</div>'
        '<div style="font-size: 0.875rem; color: #6B7280; max-width: 400px; margin: 0 auto;">'
        'SchoolPilot tracks attendance, compliance, and student scores &mdash; not classroom observations.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="background: #FEF3C7; border-left: 3px solid #F59E0B; padding: 1rem; border-radius: 0 8px 8px 0; margin-top: 1rem;">'
        '<strong>Recommendation:</strong> View the <strong>Students</strong> page for Moawin attendance and assessment data.'
        '</div>',
        unsafe_allow_html=True
    )

    # Quick stats
    st.markdown(divider(), unsafe_allow_html=True)
    st.markdown(section_title("Moawin Coverage"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(metric_card("236", "Schools", COLORS['info']), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("602", "Teachers", COLORS['success']), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("87.5%", "Avg Attendance", COLORS['success']), unsafe_allow_html=True)


def render_rumi_observations(filters):
    """Rumi - AI coaching conversations, not classroom observations."""

    # Rumi-specific metrics
    st.markdown(
        hero_metric(
            "40,728",
            "Coaching Messages",
            "WhatsApp-based AI coaching conversations",
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            metric_card("1,871", "Active Teachers", COLORS['success']),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card("5,044", "Chat Sessions", COLORS['info']),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            metric_card("1,815", "Lesson Plans", COLORS['warning']),
            unsafe_allow_html=True
        )

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            'Rumi provides <strong>continuous AI coaching</strong> via WhatsApp, offering lesson planning support '
            'and teaching guidance. Unlike observation tools, Rumi engages teachers in <strong>proactive coaching conversations</strong>.',
            border_color=COLORS['info'],
            title="How Rumi Works"
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === SESSION TREND ===
    st.markdown(section_title("Weekly Activity"), unsafe_allow_html=True)

    # Sample trend data
    weeks = ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"]
    sessions = [420, 580, 650, 720, 680, 750, 810, 870]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weeks,
        y=sessions,
        mode='lines+markers',
        name='Sessions',
        line=dict(color=COLORS['info'], width=2, shape='spline'),
        marker=dict(size=6, color=COLORS['info'], line=dict(color='white', width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.06)'
    ))

    base_layout = plotly_layout_defaults(height=240)
    base_layout['showlegend'] = False
    fig.update_layout(**base_layout)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


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
    base_layout['legend'] = dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='right',
        x=1,
        font=dict(size=11, family="Inter, -apple-system, sans-serif")
    )
    fig.update_layout(**base_layout)

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

    # Agreement analysis
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
            metric_card("12%", "AI Rated Higher", COLORS['text_muted']),
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


def render_recent_observations(filters, region: str):
    """Recent observations list with styled cards."""

    st.markdown(section_title("Recent Activity"), unsafe_allow_html=True)

    # Region-specific sample data
    if region == "Balochistan":
        observations = [
            {"date": "2026-01-21", "type": "AI", "school": "GPS Quetta #12", "teacher": "Fatima", "subject": "Mathematics", "score": 68},
            {"date": "2026-01-20", "type": "AI", "school": "GPS Zhob #5", "teacher": "Saima", "subject": "English", "score": 62},
            {"date": "2026-01-19", "type": "Human", "school": "GPS Quetta #8", "teacher": "Ahmed", "subject": "Science", "score": 75},
            {"date": "2026-01-18", "type": "AI", "school": "GPS Pishin #3", "teacher": "Ayesha", "subject": "Urdu", "score": 65},
            {"date": "2026-01-17", "type": "Human", "school": "GPS Loralai #2", "teacher": "Zara", "subject": "Mathematics", "score": 72},
        ]
    else:
        observations = [
            {"date": "2026-01-21", "type": "AI", "school": "GMS Rawalpindi #12", "teacher": "Mahjabeen", "subject": "Mathematics", "score": 72},
            {"date": "2026-01-20", "type": "AI", "school": "GMS Islamabad #5", "teacher": "Fatima", "subject": "English", "score": 68},
            {"date": "2026-01-19", "type": "Human", "school": "GPS Balochistan #8", "teacher": "Ahmed", "subject": "Science", "score": 75},
            {"date": "2026-01-18", "type": "AI", "school": "GMS Rawalpindi #3", "teacher": "Ayesha", "subject": "Urdu", "score": 71},
            {"date": "2026-01-17", "type": "Human", "school": "GPS Balochistan #2", "teacher": "Zara", "subject": "Mathematics", "score": 65},
        ]

    for obs in observations:
        obs_type = obs['type']

        st.markdown(
            obs_card(
                teacher=obs["teacher"],
                school=obs["school"],
                subject=obs["subject"],
                score=obs["score"],
                date=obs["date"],
                obs_type=obs_type
            ),
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
