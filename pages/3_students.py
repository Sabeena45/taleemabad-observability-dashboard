"""
Student Outcomes page - Student assessment and attendance data.

Design: Minimalist, insight-first approach following Tufte principles.
"""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from data.queries import get_student_scores_by_subject, get_attendance_trend

st.set_page_config(
    page_title="Student Outcomes | Taleemabad",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === DESIGN SYSTEM CSS (consistent with app.py) ===
st.markdown("""
<style>
    /* === RESET & BASE === */
    .stApp { background: #FAFAFA; }
    #MainMenu, footer, header { visibility: hidden; }

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* === STATUS BAR === */
    .status-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0;
        border-bottom: 1px solid #E5E7EB;
        margin-bottom: 1.5rem;
    }
    .status-region { font-weight: 600; color: #1A1A1A; }
    .status-live {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.75rem;
        color: #10B981;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        background: #10B981;
        border-radius: 50%;
    }

    /* === SECTION TITLE === */
    .section-title {
        font-size: 0.75rem;
        font-weight: 600;
        color: #9CA3AF;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }

    /* === HERO METRIC === */
    .hero-metric {
        text-align: center;
        padding: 2rem 0;
    }
    .hero-value {
        font-size: 4rem;
        font-weight: 700;
        line-height: 1;
        letter-spacing: -0.02em;
    }
    .hero-label {
        font-size: 1rem;
        color: #6B7280;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }
    .hero-context {
        font-size: 0.875rem;
        color: #9CA3AF;
        margin-top: 0.25rem;
    }

    /* === METRIC CARDS === */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-card-value {
        font-size: 2rem;
        font-weight: 700;
        line-height: 1;
        color: #1A1A1A;
    }
    .metric-card-label {
        font-size: 0.75rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }

    /* === INSIGHT CARDS === */
    .insight-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .insight-highlight {
        font-size: 1.125rem;
        color: #1A1A1A;
        line-height: 1.6;
    }
    .insight-highlight strong {
        color: #EF4444;
    }

    /* === CLEAN DIVIDER === */
    .clean-divider {
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
    }

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        background: transparent;
        border-bottom: 1px solid #E5E7EB;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 0;
        padding: 0.75rem 1.25rem;
        font-size: 0.875rem;
        color: #6B7280;
        border-bottom: 2px solid transparent;
        margin-bottom: -1px;
    }
    .stTabs [aria-selected="true"] {
        color: #1A1A1A;
        font-weight: 600;
        border-bottom: 2px solid #1A1A1A;
        background: transparent;
    }

    /* Plotly backgrounds */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }

    /* Grade row */
    .grade-row {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .grade-label {
        width: 100px;
        font-weight: 600;
        color: #1A1A1A;
    }
    .grade-bar {
        flex: 1;
        height: 8px;
        background: #E5E7EB;
        border-radius: 4px;
        margin: 0 1rem;
        overflow: hidden;
    }
    .grade-fill {
        height: 100%;
        border-radius: 4px;
    }
    .grade-value {
        width: 60px;
        text-align: right;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def main():
    filters = render_sidebar()

    # === STATUS BAR ===
    st.markdown(f'''
    <div class="status-bar">
        <span class="status-region">◉ {filters["region"]} · Student Outcomes</span>
        <span class="status-live">
            <span class="status-dot"></span>
            Live
        </span>
    </div>
    ''', unsafe_allow_html=True)

    # === HERO: Reading Crisis ===
    on_track_pct = 34

    st.markdown(f'''
    <div class="hero-metric">
        <div class="hero-value" style="color: #EF4444;">{on_track_pct}%</div>
        <div class="hero-label">Students Reading at Grade Level</div>
        <div class="hero-context">National data shows 80% of Pakistani primary students cannot read appropriately</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value">16,898</div>
            <div class="metric-card-label">Total Students</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value">7,278</div>
            <div class="metric-card-label">Assessments</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #F59E0B;">67.2%</div>
            <div class="metric-card-label">Avg Score</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #10B981;">71.8%</div>
            <div class="metric-card-label">Pass Rate</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

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

    st.markdown('<div class="section-title">Performance by Subject</div>', unsafe_allow_html=True)

    scores_data = get_student_scores_by_subject(filters)

    # Horizontal bar chart
    subjects = [d['subject'] for d in scores_data]
    avg_scores = [d['avg_score'] for d in scores_data]
    pass_rates = [d['pass_rate'] for d in scores_data]

    # Color based on performance
    colors = ['#10B981' if s >= 70 else '#F59E0B' if s >= 60 else '#EF4444' for s in avg_scores]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=subjects,
        x=avg_scores,
        orientation='h',
        marker_color=colors,
        text=[f'{s:.0f}%' for s in avg_scores],
        textposition='outside',
        textfont=dict(size=12, color='#374151'),
        hovertemplate='%{y}: %{x:.1f}%<extra></extra>'
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=40, l=100, r=60),
        height=280,
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='#F3F4F6',
            zeroline=False,
            ticksuffix='%'
        ),
        yaxis=dict(showgrid=False, autorange='reversed'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Simple data table
    st.markdown('<div class="section-title" style="margin-top: 1.5rem;">Detailed Breakdown</div>', unsafe_allow_html=True)

    for d in scores_data:
        score_color = '#10B981' if d['avg_score'] >= 70 else '#F59E0B' if d['avg_score'] >= 60 else '#EF4444'
        bar_width = d['avg_score']

        st.markdown(f'''
        <div class="grade-row">
            <div class="grade-label">{d["subject"]}</div>
            <div class="grade-bar">
                <div class="grade-fill" style="width: {bar_width}%; background: {score_color};"></div>
            </div>
            <div class="grade-value" style="color: {score_color};">{d["avg_score"]:.0f}%</div>
        </div>
        ''', unsafe_allow_html=True)


def render_attendance(filters):
    """Attendance trends."""

    st.markdown('<div class="section-title">Daily Attendance Rate</div>', unsafe_allow_html=True)

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
        line=dict(color='#3B82F6', width=2),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))

    # Target line
    fig.add_hline(
        y=target,
        line_dash="dash",
        line_color="#10B981",
        annotation_text=f"Target: {target}%",
        annotation_position="right"
    )

    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=60),
        height=280,
        xaxis=dict(showgrid=False),
        yaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='#F3F4F6',
            zeroline=False,
            ticksuffix='%'
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    delta = avg_attendance - target
    delta_color = "#10B981" if delta >= 0 else "#EF4444"

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: {delta_color};">{avg_attendance:.1f}%</div>
            <div class="metric-card-label">Average</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #10B981;">{max(rates):.0f}%</div>
            <div class="metric-card-label">Best Day</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #EF4444;">{min(rates):.0f}%</div>
            <div class="metric-card-label">Lowest Day</div>
        </div>
        ''', unsafe_allow_html=True)


def render_reading_assessments(filters):
    """Rumi reading assessment data."""

    st.markdown('<div class="section-title">Rumi Reading Assessments</div>', unsafe_allow_html=True)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value">186</div>
            <div class="metric-card-label">Assessments</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value">109</div>
            <div class="metric-card-label">Students</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #F59E0B;">52</div>
            <div class="metric-card-label">Avg WCPM</div>
        </div>
        ''', unsafe_allow_html=True)

    with col4:
        st.markdown('''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #EF4444;">34%</div>
            <div class="metric-card-label">On Track</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # WCPM by Grade
    st.markdown('<div class="section-title">Words Correct Per Minute by Grade</div>', unsafe_allow_html=True)

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

    # Color based on target
    colors = ['#10B981' if w >= t * 0.8 else '#F59E0B' if w >= t * 0.6 else '#EF4444'
              for w, t in zip(wcpms, targets)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=grades,
        y=wcpms,
        marker_color=colors,
        text=[f'{w}' for w in wcpms],
        textposition='outside',
        textfont=dict(size=12, color='#374151'),
        hovertemplate='%{x}: %{y} WCPM<extra></extra>'
    ))

    # Target line (dots)
    fig.add_trace(go.Scatter(
        x=grades,
        y=targets,
        mode='markers',
        marker=dict(symbol='line-ew', size=20, color='#9CA3AF', line_width=2),
        name='Target',
        hovertemplate='Target: %{y} WCPM<extra></extra>'
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(t=20, b=40, l=40, r=20),
        height=280,
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F3F4F6',
            zeroline=False,
            title=None
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Critical alert
    st.markdown('''
    <div class="insight-card" style="border-left: 3px solid #EF4444;">
        <div style="font-size: 0.75rem; color: #EF4444; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Reading Crisis</div>
        <div class="insight-highlight">
            Only <strong>34%</strong> of assessed students read at grade level.
            All grades are below WCPM targets. Focused reading intervention is urgently needed.
        </div>
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
