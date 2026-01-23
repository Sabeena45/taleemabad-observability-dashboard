"""
Taleemabad Observability Dashboard - Design System

A minimalist, insight-first design system based on:
- Edward Tufte's data visualization principles
- Apple Human Interface Guidelines
- Modern dashboard best practices

Usage:
    from styles.design_system import inject_css, COLORS
    inject_css()
"""

# === COLOR PALETTE ===
COLORS = {
    # Base colors
    'background': '#FAFAFA',
    'surface': '#FFFFFF',
    'text_primary': '#1A1A1A',
    'text_secondary': '#6B7280',
    'text_muted': '#9CA3AF',

    # Semantic colors
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'info': '#3B82F6',

    # Borders & dividers
    'border': '#E5E7EB',
    'divider': '#F3F4F6',
}

# === TYPOGRAPHY ===
FONTS = {
    'family': '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    'size_hero': '4rem',
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

/* === CONTAINER === */
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
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
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

/* === STREAMLIT METRIC OVERRIDE === */
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

/* === RADIO/PILLS === */
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

/* === OBSERVATION CARD === */
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

/* === GRADE ROW === */
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

/* === RECOMMENDATION CARD === */
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
"""


def inject_css():
    """Inject the design system CSS into a Streamlit app."""
    import streamlit as st
    st.markdown(f'<style>{CSS}</style>', unsafe_allow_html=True)


def get_color(name: str) -> str:
    """Get a color from the palette."""
    return COLORS.get(name, '#1A1A1A')


def hero_metric(value: str, label: str, context: str = "", color: str = None):
    """Generate HTML for a hero metric."""
    color_style = f'style="color: {color};"' if color else ''
    return f'''
    <div class="hero-metric">
        <div class="hero-value" {color_style}>{value}</div>
        <div class="hero-label">{label}</div>
        <div class="hero-context">{context}</div>
    </div>
    '''


def metric_card(value: str, label: str, color: str = None):
    """Generate HTML for a metric card."""
    color_style = f'style="color: {color};"' if color else ''
    return f'''
    <div class="metric-card">
        <div class="metric-card-value" {color_style}>{value}</div>
        <div class="metric-card-label">{label}</div>
    </div>
    '''


def insight_card(content: str, border_color: str = None, title: str = None):
    """Generate HTML for an insight card."""
    border_style = f'border-left: 3px solid {border_color};' if border_color else ''
    title_html = f'''
        <div style="font-size: 0.75rem; color: {border_color}; text-transform: uppercase;
                    letter-spacing: 0.05em; margin-bottom: 0.5rem;">{title}</div>
    ''' if title else ''

    return f'''
    <div class="insight-card" style="{border_style}">
        {title_html}
        <div class="insight-highlight">{content}</div>
    </div>
    '''


def status_bar(region: str, page_name: str = ""):
    """Generate HTML for the status bar."""
    label = f"{region} · {page_name}" if page_name else region
    return f'''
    <div class="status-bar">
        <span class="status-region">◉ {label}</span>
        <span class="status-live">
            <span class="status-dot"></span>
            Live
        </span>
    </div>
    '''


def divider():
    """Generate HTML for a clean divider."""
    return '<div class="clean-divider"></div>'


def section_title(text: str):
    """Generate HTML for a section title."""
    return f'<div class="section-title">{text}</div>'
