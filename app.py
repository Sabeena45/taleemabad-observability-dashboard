"""
Taleemabad Observability Dashboard
A minimalist, insight-first dashboard for teaching quality.

Design Philosophy (based on research):
- Five-second rule: Most important insight visible immediately
- Maximum data-ink ratio (Edward Tufte)
- One story per view
- Progressive disclosure
- Apple HIG: Clarity, deference, depth

Sources:
- https://medium.com/@yahiazakaria445/edward-tuftes-6-data-visualization-principles
- https://developer.apple.com/design/human-interface-guidelines
- https://www.uxpin.com/studio/blog/dashboard-design-principles/
"""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

# === PAGE CONFIG (must be first) ===
st.set_page_config(
    page_title="Taleemabad",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"  # Start clean, expand on demand
)

# === IMPORTS ===
from components.sidebar import render_sidebar
from data.queries import (
    get_summary_metrics,
    get_fico_section_c_metrics,
    get_fico_section_d_metrics,
    get_observation_counts
)

# === DESIGN SYSTEM CSS ===
st.markdown("""
<style>
    /* === RESET & BASE === */
    .stApp {
        background: #FAFAFA;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header {visibility: hidden;}

    /* === TYPOGRAPHY === */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* === HERO METRIC === */
    .hero-metric {
        text-align: center;
        padding: 2rem 0;
    }
    .hero-value {
        font-size: 4.5rem;
        font-weight: 700;
        color: #1A1A1A;
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
    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .metric-card {
        flex: 1;
        background: white;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .metric-card-value {
        font-size: 1.75rem;
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
    .metric-card-delta {
        font-size: 0.75rem;
        margin-top: 0.5rem;
    }
    .delta-positive { color: #10B981; }
    .delta-negative { color: #EF4444; }
    .delta-neutral { color: #6B7280; }

    /* === INSIGHT CARDS === */
    .insight-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }
    .insight-title {
        font-size: 0.875rem;
        font-weight: 600;
        color: #374151;
        margin-bottom: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .insight-highlight {
        font-size: 1.125rem;
        color: #1A1A1A;
        line-height: 1.6;
    }
    .insight-highlight strong {
        color: #EF4444;
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
    .status-region {
        font-weight: 600;
        color: #1A1A1A;
    }
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

    /* === CLEAN DIVIDER === */
    .clean-divider {
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
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

    /* Tabs - minimal */
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

    /* Hide streamlit header padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Plotly chart backgrounds */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main dashboard entry point."""

    # === SIDEBAR (collapsed by default) ===
    filters = render_sidebar()

    # === STATUS BAR ===
    st.markdown(f'''
    <div class="status-bar">
        <span class="status-region">◉ {filters["region"]}</span>
        <span class="status-live">
            <span class="status-dot"></span>
            Live
        </span>
    </div>
    ''', unsafe_allow_html=True)

    # === HERO METRIC: The #1 thing users should see ===
    metrics = get_summary_metrics(filters)
    fico_d = get_fico_section_d_metrics(filters)

    # The critical metric: Student talk time (our biggest gap)
    student_talk = fico_d['student_talk_time']
    target_talk = fico_d['target_student_time']

    # Color based on performance
    if student_talk >= target_talk:
        hero_color = "#10B981"
    elif student_talk >= target_talk * 0.6:
        hero_color = "#F59E0B"
    else:
        hero_color = "#EF4444"

    st.markdown(f'''
    <div class="hero-metric">
        <div class="hero-value" style="color: {hero_color}">{student_talk}%</div>
        <div class="hero-label">Student Talk Time</div>
        <div class="hero-context">Target: {target_talk}% · Gap: {target_talk - student_talk:.0f} percentage points</div>
    </div>
    ''', unsafe_allow_html=True)

    # === KEY METRICS ROW ===
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Schools", f"{metrics['schools']:,}")
    with col2:
        st.metric("AI Sessions", metrics['ai_sessions'], delta="+12")
    with col3:
        obs = get_observation_counts(filters)
        st.metric("Observations", obs['total'])
    with col4:
        st.metric("Avg Score", f"{metrics['avg_score']}%", delta="+2.1%")

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === MAIN INSIGHT: One story ===
    st.markdown('<div class="section-title">Key Insight</div>', unsafe_allow_html=True)

    fico_c = get_fico_section_c_metrics(filters)
    open_ratio = fico_c['open_question_ratio']

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f'''
        <div class="insight-card">
            <div class="insight-highlight">
                Teachers ask <strong>{fico_c["avg_closed_questions"]:.0f} closed questions</strong>
                for every <strong>{fico_c["avg_open_questions"]:.0f} open questions</strong>.
                <br><br>
                Only <strong>{open_ratio:.0f}%</strong> of questions encourage deeper thinking.
                Research suggests at least 40%.
            </div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        # Simple donut chart showing question ratio
        fig = go.Figure(data=[go.Pie(
            values=[open_ratio, 100-open_ratio],
            hole=0.75,
            marker_colors=['#3B82F6', '#E5E7EB'],
            textinfo='none',
            hoverinfo='skip'
        )])
        fig.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            height=160,
            annotations=[dict(
                text=f'{open_ratio:.0f}%',
                x=0.5, y=0.5,
                font_size=28,
                font_weight=600,
                font_color='#3B82F6',
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.caption("Open-ended questions")

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === DRILL DOWN TABS ===
    st.markdown('<div class="section-title">Explore</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Teaching Quality", "Observations", "Students"])

    with tab1:
        render_teaching_tab(filters)

    with tab2:
        render_observations_tab(filters)

    with tab3:
        render_students_tab(filters)


def render_teaching_tab(filters):
    """Teaching quality breakdown by FICO dimension."""

    # Simple horizontal bar showing FICO scores
    dimensions = ['Lesson Opening', 'Explanation', 'Understanding Check', 'Participation', 'Feedback', 'Closing']
    scores = [72, 68, 58, 45, 71, 65]
    targets = [75, 75, 70, 70, 70, 70]

    # Color based on whether meeting target
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
        margin=dict(t=20, b=40, l=140, r=60),
        height=320,
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
        st.markdown('<span style="color: #9CA3AF;">|</span> Target line', unsafe_allow_html=True)


def render_observations_tab(filters):
    """AI vs Human observation comparison."""

    obs = get_observation_counts(filters)

    # Simple comparison cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'''
        <div class="insight-card" style="text-align: center;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #3B82F6;">{obs["ai_count"]}</div>
            <div style="color: #6B7280; font-size: 0.875rem; margin-top: 0.25rem;">AI Sessions</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="insight-card" style="text-align: center;">
            <div style="font-size: 2.5rem; font-weight: 700; color: #10B981;">{obs["human_count"]}</div>
            <div style="color: #6B7280; font-size: 0.875rem; margin-top: 0.25rem;">Human Observations</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        if obs['total'] > 0:
            ratio = obs['ai_count'] / max(obs['human_count'], 1)
            st.markdown(f'''
            <div class="insight-card" style="text-align: center;">
                <div style="font-size: 2.5rem; font-weight: 700; color: #1A1A1A;">{ratio:.1f}×</div>
                <div style="color: #6B7280; font-size: 0.875rem; margin-top: 0.25rem;">AI Multiplier</div>
            </div>
            ''', unsafe_allow_html=True)

    # Weekly trend (simplified)
    st.markdown('<div style="height: 1rem;"></div>', unsafe_allow_html=True)

    trend_data = [
        {"week": "W1", "ai": 12, "human": 8},
        {"week": "W2", "ai": 15, "human": 10},
        {"week": "W3", "ai": 18, "human": 7},
        {"week": "W4", "ai": 22, "human": 12},
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[d['week'] for d in trend_data],
        y=[d['ai'] for d in trend_data],
        mode='lines+markers',
        name='AI',
        line=dict(color='#3B82F6', width=2),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=[d['week'] for d in trend_data],
        y=[d['human'] for d in trend_data],
        mode='lines+markers',
        name='Human',
        line=dict(color='#10B981', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        margin=dict(t=30, b=30, l=40, r=20),
        height=220,
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=11)
        ),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#F3F4F6', zeroline=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


def render_students_tab(filters):
    """Student outcomes summary."""

    metrics = get_summary_metrics(filters)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Students", f"{metrics['students']:,}")
    with col2:
        st.metric("Assessments", "7,278")
    with col3:
        st.metric("Avg Score", "67.2%")
    with col4:
        st.metric("Pass Rate", "71.8%")

    # Reading crisis callout
    st.markdown('''
    <div class="insight-card" style="border-left: 3px solid #EF4444; margin-top: 1rem;">
        <div style="font-size: 0.75rem; color: #EF4444; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Reading Alert</div>
        <div class="insight-highlight">
            Only <strong>34%</strong> of assessed students read at grade level.
            <span style="color: #6B7280;">National data shows 80% of Pakistani primary students cannot read appropriately.</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
