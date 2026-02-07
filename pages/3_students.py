"""
Student Outcomes page - Student assessment and attendance data.

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
from data.queries import get_student_scores_by_subject, get_attendance_trend
from styles.design_system import (
    inject_css,
    hero_metric,
    status_bar,
    divider,
    section_title,
    insight_card,
    metric_card,
    grade_row,
    COLORS,
    plotly_layout_defaults,
    score_color
)

st.set_page_config(
    page_title="Student Outcomes | Taleemabad",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === INJECT DESIGN SYSTEM ===
inject_css()


def main():
    filters = render_sidebar()

    # === PAGE HEADER ===
    st.markdown("""
    <div style="margin-bottom: 1rem;">
        <div style="font-size: 0.625rem; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.15em;">TALEEMABAD</div>
        <div style="font-size: 1.5rem; font-weight: 600; color: #1A1A1A; margin-top: 0.25rem;">Student Outcomes</div>
        <div style="font-size: 0.875rem; color: #6B7280;">Assessment & Attendance Analytics by Region</div>
    </div>
    """, unsafe_allow_html=True)

    # === REGION TABS ===
    tab_ict, tab_bal, tab_rwp, tab_moawin, tab_rumi = render_region_tabs()

    with tab_ict:
        render_region_students("ICT", filters)

    with tab_bal:
        render_region_students("Balochistan", filters)

    with tab_rwp:
        render_region_students("Rawalpindi", filters)

    with tab_moawin:
        render_region_students("Moawin", filters)

    with tab_rumi:
        render_region_students("Rumi", filters)


def render_region_students(region: str, filters: dict):
    """Render student outcomes for a specific region."""
    # Update filters with specific region
    region_filters = {**filters, "region": region}

    if region == "ICT":
        render_ict_students(region_filters)

    elif region == "Balochistan":
        render_balochistan_students(region_filters)

    elif region == "Rawalpindi":
        render_rwp_students(region_filters)

    elif region == "Moawin":
        render_moawin_students(region_filters)

    elif region == "Rumi":
        render_rumi_students(region_filters)


def render_ict_students(filters):
    """ICT student data - from BigQuery."""

    # === HERO ===
    st.markdown(
        hero_metric(
            "90,000",
            "Students Reached",
            "Federal Capital — NIETE ICT Programme (2024-2026)",
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("9,981", "Teachers Trained"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("2,423", "Observations"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("62.5M", "App Events"), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("$10.62", "Cost/Student", COLORS['success']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            '<strong>NIETE ICT</strong> represents Taleemabad\'s largest implementation. '
            'Variable cost of <strong>$10.62 per student per year</strong> demonstrates scalability '
            'of the digital coaching model.',
            border_color=COLORS['info'],
            title="Programme Highlight"
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === DATA SOURCE NOTE ===
    st.markdown("""
    <div style="background: #F3F4F6; padding: 1rem; border-radius: 8px; font-size: 0.875rem; color: #6B7280;">
        <strong>Data Source:</strong> BigQuery analytics_events and TEACH_TOOL_OBSERVATION tables.
        Student-level assessment data not available — teacher observation data shown.
    </div>
    """, unsafe_allow_html=True)


def render_balochistan_students(filters):
    """Balochistan student data - Winter School FLN program."""

    # === HERO ===
    st.markdown(
        hero_metric(
            "3,100",
            "Students in Winter School",
            "Foundational Literacy & Numeracy Programme",
            color=COLORS['warning']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("95", "Schools"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("522", "AI Sessions"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("6%", "Student Talk Time", COLORS['error']), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("13%", "Open Questions", COLORS['error']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === CRITICAL INSIGHT ===
    st.markdown(
        insight_card(
            'Student participation is <strong style="color: #EF4444;">critically low</strong>. '
            'Only <strong>6%</strong> student talk time (target: 40%). '
            'Teachers ask <strong>87% closed-ended</strong> questions. '
            'This limits student learning potential.',
            border_color=COLORS['error'],
            title="Urgent: Participation Crisis"
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === FLN FOCUS ===
    st.markdown(section_title("FLN Focus Areas"), unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            insight_card(
                '''<table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
                    <tr><td style="padding:0.5rem 0; font-weight:600;">Reading</td><td style="padding:0.5rem 0;">Letter recognition, syllables, words</td></tr>
                    <tr><td style="padding:0.5rem 0; font-weight:600;">Comprehension</td><td style="padding:0.5rem 0;">Story understanding, picture narration</td></tr>
                    <tr><td style="padding:0.5rem 0; font-weight:600;">Vocabulary</td><td style="padding:0.5rem 0;">Word meaning, sentence construction</td></tr>
                </table>''',
                border_color=COLORS['info'],
                title="Literacy Components"
            ),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            insight_card(
                '''<table style="width:100%; border-collapse:collapse; font-size:0.875rem;">
                    <tr><td style="padding:0.5rem 0; font-weight:600;">Number Sense</td><td style="padding:0.5rem 0;">Counting, number recognition</td></tr>
                    <tr><td style="padding:0.5rem 0; font-weight:600;">Operations</td><td style="padding:0.5rem 0;">Addition, subtraction basics</td></tr>
                    <tr><td style="padding:0.5rem 0; font-weight:600;">Problem Solving</td><td style="padding:0.5rem 0;">Word problems, reasoning</td></tr>
                </table>''',
                border_color=COLORS['warning'],
                title="Numeracy Components"
            ),
            unsafe_allow_html=True
        )


def render_rwp_students(filters):
    """Rawalpindi student data - Prevail longitudinal study."""

    # === HERO ===
    st.markdown(
        hero_metric(
            "37,000",
            "Students Targeted",
            "Prevail Rawalpindi Longitudinal Study (2025-2027)",
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("21", "Schools"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("143", "Teachers"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("444K", "App Events"), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("$3.53", "Cost/Student", COLORS['success']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === STUDY INFO ===
    st.markdown(
        insight_card(
            'Prevail longitudinal study tracks student outcomes over <strong>24 months</strong>. '
            'Baseline assessments begin Q2 2026. Cost of <strong>$3.53 per student per year</strong> '
            '(variable only) demonstrates extreme scalability.',
            border_color=COLORS['info'],
            title="Research Design"
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #DBEAFE; border-left: 3px solid #3B82F6; padding: 1rem; border-radius: 0 8px 8px 0;">
        <strong>Coming Soon:</strong> Baseline student assessment data expected Q2 2026 as part of
        Georgetown University / World Bank evaluation partnership.
    </div>
    """, unsafe_allow_html=True)


def render_moawin_students(filters):
    """Moawin/SchoolPilot student data - attendance and scores."""

    # === HERO ===
    st.markdown(
        hero_metric(
            "18,758",
            "Students Enrolled",
            "SchoolPilot Moawin Programme — 236 schools",
            color=COLORS['success']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("236", "Schools"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("602", "Teachers"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("87.5%", "Avg Attendance", COLORS['success']), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("67.2%", "Avg Score", COLORS['warning']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === TABS ===
    tab1, tab2 = st.tabs(["By Subject", "Attendance"])

    with tab1:
        render_subject_scores(filters)

    with tab2:
        render_attendance(filters)


def render_rumi_students(filters):
    """Rumi reading assessment data."""

    # === HERO ===
    st.markdown(
        hero_metric(
            "34%",
            "Students Reading at Grade Level",
            "Based on 186 Rumi reading assessments",
            color=COLORS['error']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("186", "Assessments"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("109", "Students"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("52", "Avg WCPM", COLORS['warning']), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("1,871", "Teachers Using Rumi"), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # WCPM by Grade
    st.markdown(section_title("Words Correct Per Minute by Grade"), unsafe_allow_html=True)

    grade_data = [
        {"grade": "Grade 1", "wcpm": 28, "target": 40},
        {"grade": "Grade 2", "wcpm": 42, "target": 60},
        {"grade": "Grade 3", "wcpm": 58, "target": 80},
        {"grade": "Grade 4", "wcpm": 71, "target": 100},
        {"grade": "Grade 5", "wcpm": 85, "target": 120},
    ]

    grades = [d['grade'] for d in grade_data]
    wcpms = [d['wcpm'] for d in grade_data]
    targets = [d['target'] for d in grade_data]

    colors = [COLORS['success'] if w >= t * 0.8 else COLORS['warning'] if w >= t * 0.6 else COLORS['error']
              for w, t in zip(wcpms, targets)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=grades,
        y=wcpms,
        marker_color=colors,
        marker_line_width=0,
        text=[f'{w}' for w in wcpms],
        textposition='outside',
        textfont=dict(size=11, color='#6B7280', family="Inter, -apple-system, sans-serif"),
        hovertemplate='%{x}: %{y} WCPM<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=grades,
        y=targets,
        mode='markers',
        marker=dict(symbol='line-ew', size=20, color='#9CA3AF', line_width=2),
        name='Target',
        hovertemplate='Target: %{y} WCPM<extra></extra>'
    ))

    base_layout = plotly_layout_defaults(height=280)
    base_layout['xaxis'] = dict(showgrid=False, tickfont=dict(size=12, color='#374151'))
    base_layout['yaxis'] = dict(
        showgrid=True,
        gridcolor='#F3F4F6',
        zeroline=False,
        title=None,
        tickfont=dict(size=11, color='#6B7280')
    )
    fig.update_layout(
        **base_layout,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Critical alert
    st.markdown(
        insight_card(
            'Only <strong>34%</strong> of assessed students read at grade level. '
            'All grades are below WCPM targets. National data shows 80% of Pakistani primary students '
            'cannot read appropriately.',
            border_color=COLORS['error'],
            title="Reading Crisis"
        ),
        unsafe_allow_html=True
    )


def render_subject_scores(filters):
    """Subject score breakdown."""

    st.markdown(section_title("Performance by Subject"), unsafe_allow_html=True)

    scores_data = get_student_scores_by_subject(filters)

    subjects = [d['subject'] for d in scores_data]
    avg_scores = [d['avg_score'] for d in scores_data]

    colors = [score_color(s, 70) for s in avg_scores]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=subjects,
        x=avg_scores,
        orientation='h',
        marker_color=colors,
        marker_line_width=0,
        text=[f'{s:.0f}%' for s in avg_scores],
        textposition='outside',
        textfont=dict(size=11, color='#6B7280', family="Inter, -apple-system, sans-serif"),
        hovertemplate='%{y}: %{x:.1f}%<extra></extra>'
    ))

    base_layout = plotly_layout_defaults(height=280)
    base_layout['margin'] = dict(t=10, b=40, l=100, r=60)
    base_layout['xaxis'] = dict(
        range=[0, 100],
        showgrid=True,
        gridcolor='#F3F4F6',
        zeroline=False,
        ticksuffix='%',
        tickfont=dict(size=11, color='#6B7280')
    )
    base_layout['yaxis'] = dict(showgrid=False, autorange='reversed', tickfont=dict(size=12, color='#374151'))
    fig.update_layout(
        **base_layout,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Detailed table
    st.markdown(section_title("Detailed Breakdown"), unsafe_allow_html=True)

    for d in scores_data:
        sc = score_color(d['avg_score'], 70)
        st.markdown(
            grade_row(d["subject"], d["avg_score"], sc),
            unsafe_allow_html=True
        )


def render_attendance(filters):
    """Attendance trends with smooth spline curves."""

    st.markdown(section_title("Daily Attendance Rate"), unsafe_allow_html=True)

    trend_data = get_attendance_trend(filters)

    dates = [d['date'] for d in trend_data]
    rates = [d['rate'] for d in trend_data]

    target = 85
    avg_attendance = sum(rates) / len(rates) if rates else 0

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=rates,
        mode='lines',
        name='Attendance',
        line=dict(color=COLORS['info'], width=2, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.06)'
    ))

    fig.add_hline(
        y=target,
        line_dash="dash",
        line_color=COLORS['success'],
        annotation_text=f"Target: {target}%",
        annotation_position="right",
        annotation_font=dict(color=COLORS['success'], size=11, family="Inter, -apple-system, sans-serif")
    )

    base_layout = plotly_layout_defaults(height=280)
    base_layout['xaxis'] = dict(showgrid=False)
    base_layout['yaxis'] = dict(
        range=[0, 100],
        showgrid=True,
        gridcolor='#F3F4F6',
        zeroline=False,
        ticksuffix='%',
        tickfont=dict(size=11, color='#6B7280')
    )
    fig.update_layout(
        **base_layout,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    delta_color = COLORS['success'] if avg_attendance >= target else COLORS['error']

    with col1:
        st.markdown(
            metric_card(f"{avg_attendance:.1f}%", "Average", delta_color),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card(f"{max(rates):.0f}%", "Best Day", COLORS['success']),
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            metric_card(f"{min(rates):.0f}%", "Lowest Day", COLORS['error']),
            unsafe_allow_html=True
        )


if __name__ == "__main__":
    main()
