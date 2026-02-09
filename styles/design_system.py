"""
Taleemabad Observability Dashboard - Design System

A minimalist, insight-first design system based on:
- Edward Tufte's data visualization principles
- Apple Human Interface Guidelines
- Modern dashboard best practices

Usage:
    from styles.design_system import inject_css, COLORS, hero_metric, metric_card
    inject_css()
"""

# === COLOR PALETTE ===
COLORS = {
    # Base colors
    'background': '#FAFAF9',      # Warm off-white (Taleemabad brand)
    'surface': '#FFFFFF',
    'text_primary': '#1A1A1A',
    'text_secondary': '#6B7280',
    'text_muted': '#9CA3AF',

    # Semantic colors
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',
    'muted': '#6B7280',

    # Borders & dividers
    'border': '#E5E7EB',
    'divider': '#F3F4F6',
    'hover': '#F9FAFB',
}

# === FICO SECTION COLORS ===
FICO_COLORS = {
    'A': '#8B5CF6',   # Purple - Lesson Opening
    'B': '#3B82F6',   # Blue - Explanation
    'C': '#10B981',   # Green - Understanding Check
    'D': '#F59E0B',   # Amber - Student Participation
    'E': '#EF4444',   # Red - Feedback
    'F': '#6366F1',   # Indigo - Closing
}

# === TYPOGRAPHY ===
FONTS = {
    'family': "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    'mono': "'Fira Code', 'SF Mono', Consolas, monospace",
    'size_hero': '4.5rem',
    'size_heading': '1.75rem',
    'size_body': '1rem',
    'size_small': '0.875rem',
    'size_tiny': '0.75rem',
}

# === SPACING ===
SPACING = {
    'xs': '0.25rem',
    'sm': '0.5rem',
    'md': '1rem',
    'lg': '1.5rem',
    'xl': '2rem',
}

# === CSS STYLES ===
CSS = """
/* === INTER FONT === */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* === RESET & BASE === */
.stApp {
    background: #FAFAF9;
}

/* Hide Streamlit branding */
#MainMenu, footer, header {visibility: hidden;}

/* === TYPOGRAPHY === */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* === CONTAINER === */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1100px;
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
    font-size: 0.9375rem;
}
.status-live {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.6875rem;
    font-weight: 500;
    color: #10B981;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.status-dot {
    width: 6px;
    height: 6px;
    background: #10B981;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* === SECTION TITLE === */
.section-title {
    font-size: 0.6875rem;
    font-weight: 600;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 1rem;
}

/* === HERO METRIC === */
.hero-metric {
    text-align: center;
    padding: 2.5rem 0 2rem;
}
.hero-value {
    font-size: 4.5rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -0.03em;
    font-feature-settings: 'tnum' on, 'lnum' on;
}
.hero-label {
    font-size: 0.875rem;
    font-weight: 500;
    color: #6B7280;
    margin-top: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.hero-context {
    font-size: 0.8125rem;
    color: #9CA3AF;
    margin-top: 0.375rem;
}

/* === METRIC CARDS === */
.metric-card {
    background: white;
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
    text-align: center;
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.metric-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}
.metric-card-value {
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
    color: #1A1A1A;
    font-feature-settings: 'tnum' on, 'lnum' on;
}
.metric-card-label {
    font-size: 0.6875rem;
    font-weight: 500;
    color: #6B7280;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.5rem;
}
.metric-card-delta {
    font-size: 0.75rem;
    font-weight: 500;
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
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
}
.insight-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}
.insight-highlight {
    font-size: 1.0625rem;
    color: #1A1A1A;
    line-height: 1.6;
}
.insight-highlight strong {
    color: #EF4444;
    font-weight: 600;
}

/* === CLEAN DIVIDER === */
.clean-divider {
    height: 1px;
    background: #E5E7EB;
    margin: 2rem 0;
}

/* === STREAMLIT METRIC OVERRIDE === */
.stMetric {
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
}
.stMetric label {
    color: #6B7280 !important;
    font-size: 0.6875rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.stMetric [data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    font-feature-settings: 'tnum' on, 'lnum' on;
}

/* === APPLE SEGMENTED CONTROL TABS === */
.stTabs [data-baseweb="tab-list"] {
    background: #F3F4F6;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border-bottom: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-size: 0.8125rem;
    font-weight: 500;
    color: #6B7280;
    border-bottom: none;
    margin-bottom: 0;
    transition: all 0.15s ease;
    background: transparent;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #374151;
}
.stTabs [aria-selected="true"] {
    color: #1A1A1A !important;
    font-weight: 600;
    background: white !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    border-bottom: none;
}

/* === RADIO/PILLS === */
.stRadio > div {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.stRadio > div > label {
    background: #F3F4F6 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.8125rem !important;
    font-weight: 500 !important;
    color: #6B7280 !important;
    cursor: pointer;
    transition: all 0.15s ease;
}
.stRadio > div > label:hover {
    background: #E5E7EB !important;
    color: #374151 !important;
}
.stRadio > div > label[data-checked="true"] {
    background: white !important;
    color: #1A1A1A !important;
    font-weight: 600 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
}
.stRadio [data-baseweb="radio"] {
    display: none;
}

/* === PLOTLY BACKGROUNDS === */
.js-plotly-plot .plotly .main-svg {
    background: transparent !important;
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
    font-size: 0.6875rem;
    font-weight: 600;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 1px solid #E5E7EB;
}
.compare-table td {
    padding: 0.75rem;
    border-bottom: 1px solid #F3F4F6;
    font-size: 0.875rem;
    color: #374151;
}
.compare-table tr:last-child td {
    border-bottom: none;
}

/* === OBSERVATION CARD === */
.obs-card {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease, transform 0.2s ease;
    border-left: 3px solid transparent;
}
.obs-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    transform: translateY(-1px);
}
.obs-card.ai {
    border-left-color: #3B82F6;
}
.obs-card.human {
    border-left-color: #10B981;
}
.obs-score {
    font-size: 1.5rem;
    font-weight: 600;
    font-feature-settings: 'tnum' on, 'lnum' on;
}
.obs-meta {
    color: #6B7280;
    font-size: 0.8125rem;
}

/* === GRADE ROW === */
.grade-row {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    display: flex;
    align-items: center;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s ease;
}
.grade-row:hover {
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.grade-label {
    width: 100px;
    font-weight: 600;
    font-size: 0.875rem;
    color: #1A1A1A;
}
.grade-bar {
    flex: 1;
    height: 8px;
    background: #F3F4F6;
    border-radius: 4px;
    margin: 0 1rem;
    overflow: hidden;
}
.grade-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.3s ease;
}
.grade-value {
    width: 60px;
    text-align: right;
    font-weight: 600;
    font-size: 0.875rem;
    font-feature-settings: 'tnum' on, 'lnum' on;
}

/* === RECOMMENDATION CARD === */
.rec-card {
    background: #FAFAF9;
    border-radius: 10px;
    padding: 1rem 1.25rem;
    margin: 0.5rem 0;
    border-left: 3px solid #3B82F6;
    transition: background 0.2s ease;
}
.rec-card:hover {
    background: #F3F4F6;
}
.rec-card strong {
    color: #1A1A1A;
    font-weight: 600;
}

/* === SIDEBAR REFINEMENTS === */
section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}
section[data-testid="stSidebar"] .stRadio > div > label {
    font-size: 0.8125rem !important;
    padding: 0.625rem 0.875rem !important;
}
"""


def inject_css():
    """Inject the design system CSS into a Streamlit app."""
    import streamlit as st
    st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)


def get_color(name: str) -> str:
    """Get a color from the palette."""
    return COLORS.get(name, '#1A1A1A')


def score_color(value: float, target: float) -> str:
    """Return semantic color based on value vs target."""
    if value >= target:
        return COLORS['success']
    elif value >= target * 0.7:
        return COLORS['warning']
    return COLORS['error']


def plotly_layout_defaults(height: int = 280) -> dict:
    """Return standard Plotly layout defaults for consistent chart styling."""
    return {
        'margin': dict(t=20, b=40, l=40, r=20),
        'height': height,
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': dict(
            family="Inter, -apple-system, sans-serif",
            size=12,
            color='#374151'
        ),
        'xaxis': dict(
            showgrid=False,
            zeroline=False,
            tickfont=dict(size=11, color='#6B7280')
        ),
        'yaxis': dict(
            showgrid=True,
            gridcolor='#F3F4F6',
            gridwidth=0.5,
            zeroline=False,
            tickfont=dict(size=11, color='#6B7280')
        ),
        'hoverlabel': dict(
            bgcolor='white',
            font_size=12,
            font_family="Inter, sans-serif",
            bordercolor='#E5E7EB'
        ),
        'hovermode': 'x unified',
    }


def plotly_bar_defaults() -> dict:
    """Return standard Plotly bar chart defaults."""
    return {
        'marker_line_width': 0,
        'textfont': dict(
            family="Inter, -apple-system, sans-serif",
            size=11,
            color='#6B7280'
        ),
    }


def hero_metric(value: str, label: str, context: str = "", color: str = None) -> str:
    """Generate HTML for a hero metric."""
    color_style = f'style="color: {color};"' if color else ''
    return (
        f'<div class="hero-metric">'
        f'<div class="hero-value" {color_style}>{value}</div>'
        f'<div class="hero-label">{label}</div>'
        f'<div class="hero-context">{context}</div>'
        f'</div>'
    )


def metric_card(value: str, label: str, color: str = None) -> str:
    """Generate HTML for a metric card."""
    color_style = f'style="color: {color};"' if color else ''
    return (
        f'<div class="metric-card">'
        f'<div class="metric-card-value" {color_style}>{value}</div>'
        f'<div class="metric-card-label">{label}</div>'
        f'</div>'
    )


def insight_card(content: str, border_color: str = None, title: str = None) -> str:
    """Generate HTML for an insight card.

    NOTE: All HTML must be on continuous lines (no blank lines between tags).
    Streamlit's markdown parser exits HTML mode on blank lines, causing
    inner divs to render as raw text.
    """
    border_style = f'border-left: 3px solid {border_color};' if border_color else ''
    title_html = (
        f'<div style="font-size: 0.6875rem; font-weight: 600; color: {border_color}; '
        f'text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">{title}</div>'
    ) if title else ''

    return (
        f'<div style="background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; '
        f'box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06); {border_style}">'
        f'{title_html}'
        f'<div style="font-size: 1.0625rem; color: #1A1A1A; line-height: 1.6;">{content}</div>'
        f'</div>'
    )


def status_bar(region: str, page_name: str = "") -> str:
    """Generate HTML for the status bar."""
    label = f"{region} · {page_name}" if page_name else region
    return (
        f'<div class="status-bar">'
        f'<span class="status-region">◉ {label}</span>'
        f'<span class="status-live"><span class="status-dot"></span> Live</span>'
        f'</div>'
    )


def divider() -> str:
    """Generate HTML for a clean divider."""
    return '<div class="clean-divider"></div>'


def section_title(text: str) -> str:
    """Generate HTML for a section title."""
    return f'<div class="section-title">{text}</div>'


def obs_card(teacher: str, school: str, subject: str, score: int, date: str, obs_type: str = "ai") -> str:
    """Generate HTML for an observation card."""
    type_class = "ai" if obs_type.lower() == "ai" else "human"
    type_icon = "◉" if obs_type.lower() == "ai" else "○"
    type_color = COLORS['info'] if obs_type.lower() == "ai" else COLORS['success']
    score_color_val = COLORS['success'] if score >= 70 else COLORS['warning'] if score >= 60 else COLORS['error']

    return (
        f'<div class="obs-card {type_class}">'
        f'<div><span style="color: {type_color}; margin-right: 0.5rem;">{type_icon}</span>'
        f'<strong>{teacher}</strong>'
        f'<span class="obs-meta"> · {school} · {subject}</span></div>'
        f'<div style="text-align: right;">'
        f'<div class="obs-score" style="color: {score_color_val};">{score}%</div>'
        f'<div class="obs-meta">{date}</div></div>'
        f'</div>'
    )


def grade_row(label: str, value: float, color: str) -> str:
    """Generate HTML for a grade progress row."""
    return (
        f'<div class="grade-row">'
        f'<div class="grade-label">{label}</div>'
        f'<div class="grade-bar">'
        f'<div class="grade-fill" style="width: {value}%; background: {color};"></div></div>'
        f'<div class="grade-value" style="color: {color};">{value:.0f}%</div>'
        f'</div>'
    )


def rec_card(title: str, description: str) -> str:
    """Generate HTML for a recommendation card."""
    return (
        f'<div class="rec-card">'
        f'<strong>{title}</strong><br>'
        f'<span style="color: #6B7280; font-size: 0.8125rem;">{description}</span>'
        f'</div>'
    )
