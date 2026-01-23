"""
FICO Deep Dive - Detailed analysis by FICO section.

Design: Minimalist, insight-first approach following Tufte principles.
"""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from data.queries import (
    get_fico_section_c_metrics,
    get_fico_section_d_metrics,
    get_recent_sessions
)

st.set_page_config(
    page_title="FICO Analysis | Taleemabad",
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

    /* === METRIC CARDS === */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-card-value {
        font-size: 2rem;
        font-weight: 600;
        color: #1A1A1A;
    }
    .metric-card-label {
        font-size: 0.75rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }

    /* === CLEAN DIVIDER === */
    .clean-divider {
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
    }

    /* === STREAMLIT OVERRIDES === */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .stMetric label {
        color: #6B7280 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 600 !important;
    }

    /* Pills/Radio styling */
    .stRadio > div {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
    }
    .stRadio label {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 0.875rem;
        cursor: pointer;
        transition: all 0.15s;
    }
    .stRadio label:hover {
        border-color: #3B82F6;
    }
    .stRadio [data-baseweb="radio"] {
        display: none;
    }

    /* Plotly backgrounds */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }

    /* Recommendation card */
    .rec-card {
        background: #F9FAFB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3B82F6;
    }
    .rec-card strong {
        color: #1A1A1A;
    }
</style>
""", unsafe_allow_html=True)


def main():
    filters = render_sidebar()

    # === STATUS BAR ===
    st.markdown(f'''
    <div class="status-bar">
        <span class="status-region">◉ {filters["region"]} · FICO Analysis</span>
        <span class="status-live">
            <span class="status-dot"></span>
            Live
        </span>
    </div>
    ''', unsafe_allow_html=True)

    # === SECTION SELECTOR (as pills) ===
    section = st.radio(
        "Focus Area",
        options=[
            "Overview",
            "C: Understanding Check",
            "D: Student Participation"
        ],
        horizontal=True,
        label_visibility="collapsed"
    )

    if section == "Overview":
        render_overview(filters)
    elif section == "C: Understanding Check":
        render_section_c_detail(filters)
    elif section == "D: Student Participation":
        render_section_d_detail(filters)


def render_overview(filters):
    """Render overview of all FICO sections - horizontal bar chart."""

    # Data
    dimensions = ['A: Lesson Opening', 'B: Explanation', 'C: Understanding', 'D: Participation', 'E: Feedback', 'F: Closing']
    scores = [72, 68, 58, 45, 71, 65]
    targets = [75, 75, 70, 70, 70, 70]
    gaps = [t - s for s, t in zip(scores, targets)]

    # Find biggest gap for hero metric
    max_gap_idx = gaps.index(max(gaps))
    biggest_gap_dimension = dimensions[max_gap_idx].split(': ')[1]
    biggest_gap = gaps[max_gap_idx]

    # === HERO: Biggest Gap ===
    st.markdown(f'''
    <div class="hero-metric">
        <div class="hero-value" style="color: #EF4444;">{biggest_gap}</div>
        <div class="hero-label">Points Below Target</div>
        <div class="hero-context">{biggest_gap_dimension} is our biggest opportunity</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === HORIZONTAL BAR CHART ===
    st.markdown('<div class="section-title">All Dimensions</div>', unsafe_allow_html=True)

    colors = ['#10B981' if s >= t else '#EF4444' for s, t in zip(scores, targets)]

    fig = go.Figure()

    # Score bars
    fig.add_trace(go.Bar(
        y=dimensions,
        x=scores,
        orientation='h',
        marker_color=colors,
        text=[f'{s}%' for s in scores],
        textposition='outside',
        textfont=dict(size=12, color='#374151'),
        hovertemplate='%{y}: %{x}%<extra></extra>'
    ))

    # Target markers
    fig.add_trace(go.Scatter(
        y=dimensions,
        x=targets,
        mode='markers',
        marker=dict(symbol='line-ns', size=20, color='#9CA3AF', line_width=2),
        name='Target',
        hovertemplate='Target: %{x}%<extra></extra>'
    ))

    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=40, l=150, r=60),
        height=340,
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

    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<span style="color: #10B981;">●</span> Meeting target', unsafe_allow_html=True)
    with col2:
        st.markdown('<span style="color: #EF4444;">●</span> Below target', unsafe_allow_html=True)
    with col3:
        st.markdown('<span style="color: #9CA3AF;">|</span> Target', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === KEY INSIGHTS ===
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div class="insight-card" style="border-left: 3px solid #10B981;">
            <div style="font-size: 0.75rem; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Strengths</div>
            <div class="insight-highlight">
                <strong style="color: #10B981;">Lesson Opening (72%)</strong> and <strong style="color: #10B981;">Feedback (71%)</strong> are closest to targets.
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="insight-card" style="border-left: 3px solid #EF4444;">
            <div style="font-size: 0.75rem; color: #EF4444; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Focus Areas</div>
            <div class="insight-highlight">
                <strong>Participation (45%)</strong> and <strong>Understanding (58%)</strong> need immediate attention.
            </div>
        </div>
        ''', unsafe_allow_html=True)


def render_section_c_detail(filters):
    """Section C: Checking for Understanding - Question analysis."""

    metrics = get_fico_section_c_metrics(filters)
    open_ratio = metrics['open_question_ratio']

    # === HERO: Open Question Ratio ===
    hero_color = "#10B981" if open_ratio >= 40 else "#EF4444" if open_ratio < 25 else "#F59E0B"

    st.markdown(f'''
    <div class="hero-metric">
        <div class="hero-value" style="color: {hero_color};">{open_ratio:.0f}%</div>
        <div class="hero-label">Open-Ended Questions</div>
        <div class="hero-context">Target: 40% · Gap: {40 - open_ratio:.0f} percentage points</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #10B981;">{metrics["avg_open_questions"]:.1f}</div>
            <div class="metric-card-label">Open Questions / Session</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #6B7280;">{metrics["avg_closed_questions"]:.1f}</div>
            <div class="metric-card-label">Closed Questions / Session</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === QUESTION DISTRIBUTION CHART ===
    st.markdown('<div class="section-title">Recent Sessions</div>', unsafe_allow_html=True)

    sessions = get_recent_sessions(filters, limit=12)
    if sessions:
        session_labels = [f"S{i+1}" for i in range(len(sessions))]
        open_qs = [s['open_questions'] for s in sessions]
        closed_qs = [s['closed_questions'] for s in sessions]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Open',
            x=session_labels,
            y=open_qs,
            marker_color='#10B981'
        ))
        fig.add_trace(go.Bar(
            name='Closed',
            x=session_labels,
            y=closed_qs,
            marker_color='#E5E7EB'
        ))

        fig.update_layout(
            barmode='stack',
            margin=dict(t=20, b=40, l=40, r=20),
            height=240,
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(size=11)
            ),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor='#F3F4F6', zeroline=False, title=None),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown('<div class="section-title">Recommendations</div>', unsafe_allow_html=True)

    recommendations = [
        ("Use Why and How", "These question starters encourage deeper thinking"),
        ("Wait 3-5 seconds", "Allow thinking time before calling on students"),
        ("Follow up", "Ask 'Can you explain more?' after short answers"),
        ("Target: 40%", "Aim for at least 40% open-ended questions")
    ]

    for title, desc in recommendations:
        st.markdown(f'''
        <div class="rec-card">
            <strong>{title}</strong><br>
            <span style="color: #6B7280; font-size: 0.875rem;">{desc}</span>
        </div>
        ''', unsafe_allow_html=True)


def render_section_d_detail(filters):
    """Section D: Student Participation - Talk time analysis."""

    metrics = get_fico_section_d_metrics(filters)
    student_talk = metrics['student_talk_time']
    teacher_talk = metrics['teacher_talk_time']
    target = metrics['target_student_time']

    # === HERO: Student Talk Time ===
    hero_color = "#10B981" if student_talk >= target else "#EF4444" if student_talk < 20 else "#F59E0B"

    st.markdown(f'''
    <div class="hero-metric">
        <div class="hero-value" style="color: {hero_color};">{student_talk}%</div>
        <div class="hero-label">Student Talk Time</div>
        <div class="hero-context">Target: {target}% · Currently {target - student_talk} points below</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === TALK TIME DISTRIBUTION ===
    col1, col2 = st.columns([1, 1])

    with col1:
        # Donut chart
        fig = go.Figure(data=[go.Pie(
            values=[student_talk, teacher_talk],
            labels=['Student', 'Teacher'],
            hole=0.7,
            marker_colors=['#10B981', '#6B7280'],
            textinfo='none',
            hovertemplate='%{label}: %{value}%<extra></extra>'
        )])

        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='top',
                y=-0.1,
                xanchor='center',
                x=0.5,
                font=dict(size=12)
            ),
            margin=dict(t=10, b=40, l=10, r=10),
            height=220,
            annotations=[dict(
                text=f'{student_talk}%',
                x=0.5, y=0.5,
                font_size=32,
                font_weight=600,
                font_color='#10B981',
                showarrow=False
            )]
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        st.markdown(f'''
        <div class="insight-card" style="border-left: 3px solid #EF4444; height: 180px;">
            <div style="font-size: 0.75rem; color: #EF4444; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Critical Finding</div>
            <div class="insight-highlight">
                Students learn best when actively speaking at least <strong style="color: #10B981;">40%</strong> of class time.
                <br><br>
                Current: Teachers dominate at <strong>{teacher_talk}%</strong>.
            </div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown('<div class="section-title">Action Items</div>', unsafe_allow_html=True)

    actions = [
        ("Think-Pair-Share", "Students discuss with partner before whole-class sharing"),
        ("Student Explanations", "Ask students to explain concepts to each other"),
        ("5-Minute Chunks", "Break lectures with student activity between"),
        ("Cold Calling", "Call on students randomly, not just raised hands"),
        ("Student Questions", "Encourage students to ask, not just answer")
    ]

    for title, desc in actions:
        st.markdown(f'''
        <div class="rec-card">
            <strong>{title}</strong><br>
            <span style="color: #6B7280; font-size: 0.875rem;">{desc}</span>
        </div>
        ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
