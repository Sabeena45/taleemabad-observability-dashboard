"""
Student Outcomes page - Student assessment and attendance data.

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

    # === STATUS BAR ===
    st.markdown(status_bar(filters["region"], "Student Outcomes"), unsafe_allow_html=True)

    # === HERO: Reading Crisis ===
    on_track_pct = 34

    st.markdown(
        hero_metric(
            f"{on_track_pct}%",
            "Students Reading at Grade Level",
            "National data shows 80% of Pakistani primary students cannot read appropriately",
            color=COLORS['error']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("16,898", "Total Students"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("7,278", "Assessments"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("67.2%", "Avg Score", COLORS['warning']), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("71.8%", "Pass Rate", COLORS['success']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === TABS ===
    tab1, tab2, tab3 = st.tabs(["By Subject", "Attendance", "Reading"])

    with tab1:
        render_subject_scores(filters)

    with tab2:
        render_attendance(filters)

    with tab3:
        render_reading_assessments(filters)


def render_subject_scores(filters):
    """Subject score breakdown."""

    st.markdown(section_title("Performance by Subject"), unsafe_allow_html=True)

    scores_data = get_student_scores_by_subject(filters)

    # Horizontal bar chart
    subjects = [d['subject'] for d in scores_data]
    avg_scores = [d['avg_score'] for d in scores_data]

    # Color based on performance
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

    # Simple data table using grade_row helper
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

    # Spline with subtle area fill
    fig.add_trace(go.Scatter(
        x=dates,
        y=rates,
        mode='lines',
        name='Attendance',
        line=dict(color=COLORS['info'], width=2, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.06)'
    ))

    # Target line
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


def render_reading_assessments(filters):
    """Rumi reading assessment data."""

    st.markdown(section_title("Rumi Reading Assessments"), unsafe_allow_html=True)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(metric_card("186", "Assessments"), unsafe_allow_html=True)

    with col2:
        st.markdown(metric_card("109", "Students"), unsafe_allow_html=True)

    with col3:
        st.markdown(metric_card("52", "Avg WCPM", COLORS['warning']), unsafe_allow_html=True)

    with col4:
        st.markdown(metric_card("34%", "On Track", COLORS['error']), unsafe_allow_html=True)

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

    # Color based on target (80% = success, 60% = warning, below = error)
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

    # Target markers
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
            'All grades are below WCPM targets. Focused reading intervention is urgently needed.',
            border_color=COLORS['error'],
            title="Reading Crisis"
        ),
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
