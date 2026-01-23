"""
Observations page - AI vs Human observation comparison.

Design: Minimalist, insight-first approach following Tufte principles.
"""
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from components.sidebar import render_sidebar
from data.queries import get_observation_counts, get_observation_trend

st.set_page_config(
    page_title="Observations | Taleemabad",
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
        font-size: 2.5rem;
        font-weight: 700;
        line-height: 1;
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

    /* === COMPARISON TABLE === */
    .compare-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .compare-table th {
        text-align: left;
        padding: 0.75rem;
        font-size: 0.75rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-bottom: 1px solid #E5E7EB;
    }
    .compare-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #F3F4F6;
        font-size: 0.875rem;
    }
    .compare-table tr:last-child td {
        border-bottom: none;
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

    /* Observation card */
    .obs-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .obs-score {
        font-size: 1.5rem;
        font-weight: 600;
    }
    .obs-meta {
        color: #6B7280;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)


def main():
    filters = render_sidebar()

    # === STATUS BAR ===
    st.markdown(f'''
    <div class="status-bar">
        <span class="status-region">◉ {filters["region"]} · Observations</span>
        <span class="status-live">
            <span class="status-dot"></span>
            Live
        </span>
    </div>
    ''', unsafe_allow_html=True)

    # Get data
    obs_counts = get_observation_counts(filters)

    # === HERO: AI Multiplier ===
    if obs_counts['human_count'] > 0:
        multiplier = obs_counts['ai_count'] / obs_counts['human_count']
    else:
        multiplier = obs_counts['ai_count']

    st.markdown(f'''
    <div class="hero-metric">
        <div class="hero-value" style="color: #3B82F6;">{multiplier:.1f}×</div>
        <div class="hero-label">AI Observation Multiplier</div>
        <div class="hero-context">{obs_counts["ai_count"]} AI sessions vs {obs_counts["human_count"]} human observations</div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #3B82F6;">{obs_counts["ai_count"]}</div>
            <div class="metric-card-label">AI Sessions</div>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #10B981;">{obs_counts["human_count"]}</div>
            <div class="metric-card-label">Human Observations</div>
        </div>
        ''', unsafe_allow_html=True)

    with col3:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-card-value" style="color: #1A1A1A;">{obs_counts["total"]}</div>
            <div class="metric-card-label">Total</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

    # === TABS ===
    tab1, tab2, tab3 = st.tabs(["Trends", "Comparison", "Recent"])

    with tab1:
        render_trend_view(filters)

    with tab2:
        render_comparison_view(filters)

    with tab3:
        render_recent_observations(filters)


def render_trend_view(filters):
    """Weekly observation trend."""

    st.markdown('<div class="section-title">Weekly Volume</div>', unsafe_allow_html=True)

    trend_data = get_observation_trend(filters)

    weeks = [d['week'] for d in trend_data]
    ai_counts = [d['ai'] for d in trend_data]
    human_counts = [d['human'] for d in trend_data]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=weeks,
        y=ai_counts,
        mode='lines+markers',
        name='AI',
        line=dict(color='#3B82F6', width=2),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)'
    ))

    fig.add_trace(go.Scatter(
        x=weeks,
        y=human_counts,
        mode='lines+markers',
        name='Human',
        line=dict(color='#10B981', width=2),
        marker=dict(size=6)
    ))

    fig.update_layout(
        margin=dict(t=20, b=40, l=40, r=20),
        height=280,
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
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Insight
    total_ai = sum(ai_counts)
    total_human = sum(human_counts)

    st.markdown(f'''
    <div class="insight-card">
        <div class="insight-highlight">
            Over this period: <strong style="color: #3B82F6;">{total_ai}</strong> AI sessions
            delivered <strong>{total_ai / max(total_human, 1):.1f}×</strong> the coverage of
            <strong style="color: #10B981;">{total_human}</strong> human observations.
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_comparison_view(filters):
    """AI vs Human comparison - strengths and limitations."""

    st.markdown('<div class="section-title">Strengths & Limitations</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
        <div class="insight-card" style="border-left: 3px solid #3B82F6;">
            <div style="font-size: 0.875rem; font-weight: 600; color: #3B82F6; margin-bottom: 1rem;">AI Observations (Rumi)</div>
            <table class="compare-table">
                <tr><td style="color: #10B981;">✓</td><td>24-48 hour feedback turnaround</td></tr>
                <tr><td style="color: #10B981;">✓</td><td>Consistent scoring criteria</td></tr>
                <tr><td style="color: #10B981;">✓</td><td>Unlimited scalability</td></tr>
                <tr><td style="color: #10B981;">✓</td><td>Non-intrusive (natural teaching)</td></tr>
                <tr><td style="color: #F59E0B;">⚠</td><td>Audio-only analysis</td></tr>
                <tr><td style="color: #F59E0B;">⚠</td><td>Cannot see visual aids</td></tr>
            </table>
        </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
        <div class="insight-card" style="border-left: 3px solid #10B981;">
            <div style="font-size: 0.875rem; font-weight: 600; color: #10B981; margin-bottom: 1rem;">Human Observations</div>
            <table class="compare-table">
                <tr><td style="color: #10B981;">✓</td><td>Full classroom context</td></tr>
                <tr><td style="color: #10B981;">✓</td><td>Visual + non-verbal cues</td></tr>
                <tr><td style="color: #10B981;">✓</td><td>Relationship building</td></tr>
                <tr><td style="color: #10B981;">✓</td><td>Real-time intervention</td></tr>
                <tr><td style="color: #F59E0B;">⚠</td><td>Expensive (travel, time)</td></tr>
                <tr><td style="color: #F59E0B;">⚠</td><td>Infrequent (quarterly)</td></tr>
            </table>
        </div>
        ''', unsafe_allow_html=True)

    # Agreement analysis for Balochistan
    if filters['region'] == 'Balochistan' or filters['region'] == 'Combined':
        st.markdown('<div class="clean-divider"></div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">AI-Human Agreement (Balochistan Winter School)</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-card-value" style="color: #F59E0B;">46%</div>
                <div class="metric-card-label">Agreement Rate</div>
            </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-card-value" style="color: #6B7280;">12%</div>
                <div class="metric-card-label">AI Rated Higher</div>
            </div>
            ''', unsafe_allow_html=True)

        with col3:
            st.markdown('''
            <div class="metric-card">
                <div class="metric-card-value" style="color: #EF4444;">42%</div>
                <div class="metric-card-label">Human Rated Higher</div>
            </div>
            ''', unsafe_allow_html=True)

        st.markdown('''
        <div class="insight-card" style="border-left: 3px solid #F59E0B; margin-top: 1rem;">
            <div style="font-size: 0.75rem; color: #F59E0B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Key Finding</div>
            <div class="insight-highlight">
                <strong style="color: #F59E0B;">54 percentage point gap</strong> between AI and human ratings.
                AI may be more critical OR human coaches may be more lenient. Further validation needed.
            </div>
        </div>
        ''', unsafe_allow_html=True)


def render_recent_observations(filters):
    """Recent observations list."""

    st.markdown('<div class="section-title">Recent Activity</div>', unsafe_allow_html=True)

    # Sample data
    observations = [
        {"date": "2026-01-21", "type": "AI", "school": "GMS Rawalpindi #12", "teacher": "Mahjabeen", "subject": "Mathematics", "score": 72},
        {"date": "2026-01-20", "type": "AI", "school": "GMS Islamabad #5", "teacher": "Fatima", "subject": "English", "score": 68},
        {"date": "2026-01-19", "type": "Human", "school": "GPS Balochistan #8", "teacher": "Ahmed", "subject": "Science", "score": 75},
        {"date": "2026-01-18", "type": "AI", "school": "GMS Rawalpindi #3", "teacher": "Ayesha", "subject": "Urdu", "score": 71},
        {"date": "2026-01-17", "type": "Human", "school": "GPS Balochistan #2", "teacher": "Zara", "subject": "Mathematics", "score": 65},
    ]

    for obs in observations:
        type_color = "#3B82F6" if obs['type'] == 'AI' else "#10B981"
        type_icon = "◉" if obs['type'] == 'AI' else "○"
        score_color = "#10B981" if obs['score'] >= 70 else "#F59E0B" if obs['score'] >= 60 else "#EF4444"

        st.markdown(f'''
        <div class="obs-card">
            <div>
                <span style="color: {type_color}; margin-right: 0.5rem;">{type_icon}</span>
                <strong>{obs["teacher"]}</strong>
                <span class="obs-meta"> · {obs["school"]} · {obs["subject"]}</span>
            </div>
            <div style="text-align: right;">
                <div class="obs-score" style="color: {score_color};">{obs["score"]}%</div>
                <div class="obs-meta">{obs["date"]}</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
