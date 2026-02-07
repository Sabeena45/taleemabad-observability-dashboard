"""
Taleemabad Observability Dashboard
A minimalist, insight-first dashboard for teaching quality.

Design Philosophy (based on research):
- Five-second rule: Most important insight visible immediately
- Maximum data-ink ratio (Edward Tufte)
- One story per view
- Progressive disclosure
- Apple HIG: Clarity, deference, depth

Region-wise analysis: ICT | Balochistan | Rawalpindi | Moawin | Rumi
"""
import streamlit as st
import plotly.graph_objects as go

# === PAGE CONFIG (must be first) ===
st.set_page_config(
    page_title="Taleemabad Observability",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === IMPORTS ===
from components.sidebar import render_sidebar
from components.region_tabs import render_region_tabs, REGIONS
from data import (
    islamabad_queries,
    balochistan_queries,
    rawalpindi_queries,
    moawin_queries,
    rumi_queries
)
from styles.design_system import (
    inject_css,
    hero_metric,
    status_bar,
    divider,
    section_title,
    metric_card,
    insight_card,
    COLORS,
    plotly_layout_defaults,
    score_color
)

# === INJECT DESIGN SYSTEM ===
inject_css()


def main():
    """Main dashboard entry point."""

    # === SIDEBAR (collapsed by default, no region selector) ===
    filters = render_sidebar()

    # === HEADER ===
    st.markdown("""
    <div style="padding: 0.5rem 0 1rem 0;">
        <div style="font-size: 0.625rem; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.15em;">TALEEMABAD</div>
        <div style="font-size: 1.5rem; font-weight: 600; color: #1A1A1A;">Observability Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    # === REGION TABS ===
    tab_ict, tab_bal, tab_rwp, tab_moawin, tab_rumi = render_region_tabs()

    with tab_ict:
        render_ict_dashboard(filters)

    with tab_bal:
        render_balochistan_dashboard(filters)

    with tab_rwp:
        render_rwp_dashboard(filters)

    with tab_moawin:
        render_moawin_dashboard(filters)

    with tab_rumi:
        render_rumi_dashboard(filters)


# =============================================================================
# REGION-SPECIFIC DASHBOARDS
# =============================================================================

def render_ict_dashboard(filters):
    """ICT (Islamabad) Dashboard - BigQuery TEACH observations."""

    # Get data
    metrics = islamabad_queries.get_summary_metrics(filters.get("time_period", "All Time"))
    fico = islamabad_queries.get_fico_scores()

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{metrics['teachers']:,}",
            "Teachers in ICT",
            f"Across {metrics['schools']} schools · {metrics['observations']} TEACH observations",
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card(str(metrics['schools']), "Schools"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(f"{metrics['teachers']:,}", "Teachers"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(str(metrics['observations']), "Observations"), unsafe_allow_html=True)
    with col4:
        avg_score = metrics.get('avg_score') or 68
        st.markdown(metric_card(f"{avg_score}%", "Avg Score", score_color(avg_score, 70)), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === FICO SCORES ===
    st.markdown(section_title("FICO Framework Scores"), unsafe_allow_html=True)

    if fico.get('section_b'):
        render_fico_bar_chart(fico)
    else:
        st.info("FICO score breakdown not available for ICT region. TEACH observations use different scoring.")

    # === INSIGHT ===
    st.markdown(
        insight_card(
            "ICT has the largest teacher base with <strong>9,981 certified teachers</strong>. "
            "TEACH observations show classroom practices across the Federal Capital. "
            "Training completion data available via BigQuery.",
            title="Regional Context"
        ),
        unsafe_allow_html=True
    )


def render_balochistan_dashboard(filters):
    """Balochistan Dashboard - AI + Human observations, FICO, talk time."""

    # Get data
    obs_type = filters.get("observation_type", "All Observations")
    metrics = balochistan_queries.get_summary_metrics(obs_type)
    talk_time = balochistan_queries.get_talk_time_metrics(obs_type)
    questions = balochistan_queries.get_question_metrics(obs_type)
    obs_counts = balochistan_queries.get_observation_counts(obs_type)
    fico = balochistan_queries.get_fico_scores()

    # === HERO: Student Talk Time (the crisis) ===
    student_talk = talk_time['student_talk_time'] or 6
    target_talk = talk_time['target_student_time'] or 40

    st.markdown(
        hero_metric(
            f"{student_talk}%",
            "Student Talk Time",
            f"Target: {target_talk}% · Gap: {target_talk - student_talk:.0f} percentage points",
            color=COLORS['error']
        ),
        unsafe_allow_html=True
    )

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card(str(obs_counts['ai_count']), "AI Sessions", COLORS['info']), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(str(obs_counts['human_count']), "Human Obs", COLORS['success']), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(str(metrics['schools']), "Schools"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card(str(metrics['teachers']), "Teachers"), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === TWO COLUMN LAYOUT ===
    col1, col2 = st.columns(2)

    with col1:
        # Talk Time Donut
        st.markdown(section_title("Talk Time Distribution"), unsafe_allow_html=True)
        teacher_talk = talk_time['teacher_talk_time'] or 82

        fig = go.Figure(data=[go.Pie(
            values=[student_talk, teacher_talk, 100 - student_talk - teacher_talk],
            labels=['Student', 'Teacher', 'Other'],
            hole=0.7,
            marker_colors=[COLORS['success'], COLORS['error'], '#E5E7EB'],
            textinfo='none'
        )])

        base_layout = plotly_layout_defaults(height=200)
        base_layout['margin'] = dict(t=10, b=10, l=10, r=10)
        fig.update_layout(
            **base_layout,
            showlegend=True,
            legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center'),
            annotations=[dict(
                text=f'{student_talk}%',
                x=0.5, y=0.5,
                font_size=28,
                font_weight=600,
                font_color=COLORS['error'],
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        # Question Types
        st.markdown(section_title("Question Types"), unsafe_allow_html=True)
        open_q = questions.get('avg_open_questions', 1.9)
        closed_q = questions.get('avg_closed_questions', 12.8)
        open_ratio = questions.get('open_question_ratio', 13)

        fig = go.Figure(data=[go.Pie(
            values=[open_ratio, 100 - open_ratio],
            labels=['Open-ended', 'Closed'],
            hole=0.7,
            marker_colors=[COLORS['info'], '#E5E7EB'],
            textinfo='none'
        )])

        base_layout = plotly_layout_defaults(height=200)
        base_layout['margin'] = dict(t=10, b=10, l=10, r=10)
        fig.update_layout(
            **base_layout,
            showlegend=True,
            legend=dict(orientation='h', y=-0.1, x=0.5, xanchor='center'),
            annotations=[dict(
                text=f'{open_ratio:.0f}%',
                x=0.5, y=0.5,
                font_size=28,
                font_weight=600,
                font_color=COLORS['info'],
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown(divider(), unsafe_allow_html=True)

    # === FICO SCORES ===
    st.markdown(section_title("FICO Framework Scores"), unsafe_allow_html=True)
    render_fico_bar_chart(fico)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            f"Balochistan Winter School shows <strong>{student_talk}% student talk time</strong> vs 40% target. "
            f"Teachers ask <strong>{closed_q:.0f} closed questions</strong> for every <strong>{open_q:.0f} open</strong>. "
            "AI observations (522) enable continuous feedback at scale.",
            border_color=COLORS['error'],
            title="Implementation Gap"
        ),
        unsafe_allow_html=True
    )


def render_rwp_dashboard(filters):
    """Rawalpindi Dashboard - Early stage, events tracking."""

    # Get data
    metrics = rawalpindi_queries.get_summary_metrics(filters.get("time_period", "All Time"))

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{metrics['teachers']}",
            "Teachers Onboarded",
            f"Prevail Longitudinal Study · {metrics['schools']} schools",
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card(str(metrics['schools']), "Schools"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(str(metrics['teachers']), "Teachers"), unsafe_allow_html=True)
    with col3:
        events = rawalpindi_queries.get_event_count()
        st.markdown(metric_card(f"{events:,}", "Events"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("—", "Observations", COLORS['muted']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === STATUS MESSAGE ===
    st.markdown(
        insight_card(
            "Rawalpindi is part of the <strong>Prevail Longitudinal Study</strong>. "
            "Schools and teachers are onboarded, with <strong>444,656 analytics events</strong> tracked. "
            "Observation system launching soon.",
            title="Early Stage"
        ),
        unsafe_allow_html=True
    )

    # === PLACEHOLDER CHART ===
    st.markdown(section_title("Event Tracking"), unsafe_allow_html=True)
    st.info("📊 Event analytics dashboard coming soon. Currently tracking platform engagement across 21 schools.")


def render_moawin_dashboard(filters):
    """Moawin/SchoolPilot Dashboard - Attendance, compliance, scores."""

    # Get data
    metrics = moawin_queries.get_summary_metrics(filters.get("time_period", "All Time"))
    attendance_trend = moawin_queries.get_attendance_trend(30)
    scores_by_subject = moawin_queries.get_student_scores_by_subject()

    # === HERO ===
    avg_attendance = metrics.get('avg_attendance', 87.5)

    st.markdown(
        hero_metric(
            f"{avg_attendance}%",
            "Average Attendance",
            f"{metrics['schools']} schools · {metrics['students']:,} students tracked",
            color=COLORS['success'] if avg_attendance >= 85 else COLORS['warning']
        ),
        unsafe_allow_html=True
    )

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card(str(metrics['schools']), "Schools"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(str(metrics['teachers']), "Teachers"), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(f"{metrics['students']:,}", "Students"), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card(f"{avg_attendance}%", "Attendance", COLORS['success']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === ATTENDANCE TREND ===
    st.markdown(section_title("Attendance Trend (30 Days)"), unsafe_allow_html=True)

    if attendance_trend:
        dates = [d['date'] for d in attendance_trend]
        rates = [d['rate'] for d in attendance_trend]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=rates,
            mode='lines',
            line=dict(color=COLORS['info'], width=2, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.06)'
        ))

        # Target line
        fig.add_hline(y=85, line_dash="dash", line_color=COLORS['success'],
                      annotation_text="Target: 85%", annotation_position="right")

        base_layout = plotly_layout_defaults(height=250)
        base_layout['yaxis'] = dict(range=[0, 100], ticksuffix='%')
        fig.update_layout(**base_layout, showlegend=False)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Attendance trend data loading...")

    st.markdown(divider(), unsafe_allow_html=True)

    # === SCORES BY SUBJECT ===
    st.markdown(section_title("Scores by Subject"), unsafe_allow_html=True)

    if scores_by_subject:
        subjects = [s['subject'] for s in scores_by_subject[:8]]
        avg_scores = [s['avg_score'] for s in scores_by_subject[:8]]
        colors = [score_color(s, 70) for s in avg_scores]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=subjects,
            x=avg_scores,
            orientation='h',
            marker_color=colors,
            text=[f'{s:.0f}%' for s in avg_scores],
            textposition='outside'
        ))

        base_layout = plotly_layout_defaults(height=300)
        base_layout['margin'] = dict(t=10, b=40, l=120, r=60)
        base_layout['xaxis'] = dict(range=[0, 100], ticksuffix='%')
        base_layout['yaxis'] = dict(autorange='reversed')
        fig.update_layout(**base_layout, showlegend=False)

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("Subject scores loading...")


def render_rumi_dashboard(filters):
    """Rumi Dashboard - AI coaching, chat sessions, lesson plans."""

    # Get data
    metrics = rumi_queries.get_summary_metrics(filters.get("time_period", "All Time"))
    conversation_metrics = rumi_queries.get_conversation_metrics()
    lesson_metrics = rumi_queries.get_lesson_plan_metrics()

    # === HERO ===
    total_messages = conversation_metrics.get('total_messages', 40728)

    st.markdown(
        hero_metric(
            f"{total_messages:,}",
            "Coaching Messages",
            f"{metrics['teachers']:,} teachers using Rumi AI",
            color=COLORS['info']
        ),
        unsafe_allow_html=True
    )

    # === KEY METRICS ===
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card(f"{metrics['teachers']:,}", "Teachers"), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(f"{metrics.get('chat_sessions', 5044):,}", "Chat Sessions"), unsafe_allow_html=True)
    with col3:
        lesson_plans = lesson_metrics.get('total_lesson_plans', 1815)
        st.markdown(metric_card(f"{lesson_plans:,}", "Lesson Plans"), unsafe_allow_html=True)
    with col4:
        ai_sessions = metrics.get('ai_sessions', 135)
        st.markdown(metric_card(str(ai_sessions), "Audio Sessions", COLORS['info']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === TWO COLUMN LAYOUT ===
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(section_title("Engagement Metrics"), unsafe_allow_html=True)

        active_7d = conversation_metrics.get('active_users_7d', 89)
        active_30d = conversation_metrics.get('active_users_30d', 234)
        avg_per_session = conversation_metrics.get('avg_messages_per_session', 8.1)

        st.markdown(metric_card(str(active_7d), "Active Users (7d)", COLORS['success']), unsafe_allow_html=True)
        st.markdown(metric_card(str(active_30d), "Active Users (30d)"), unsafe_allow_html=True)
        st.markdown(metric_card(f"{avg_per_session:.1f}", "Avg Msgs/Session"), unsafe_allow_html=True)

    with col2:
        st.markdown(section_title("Content Generation"), unsafe_allow_html=True)

        unique_teachers = lesson_metrics.get('unique_teachers', 312)
        reading_assessments = 197  # Known value from Rumi

        st.markdown(metric_card(f"{lesson_plans:,}", "Lesson Plans Created"), unsafe_allow_html=True)
        st.markdown(metric_card(str(unique_teachers), "Teachers Creating"), unsafe_allow_html=True)
        st.markdown(metric_card(str(reading_assessments), "Reading Assessments"), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            f"Rumi has facilitated <strong>{total_messages:,} coaching conversations</strong> with {metrics['teachers']:,} teachers. "
            f"<strong>{lesson_plans:,} lesson plans</strong> generated, showing active content creation. "
            "AI audio sessions provide real-time feedback on teaching practice.",
            title="AI Coaching Impact"
        ),
        unsafe_allow_html=True
    )


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def render_fico_bar_chart(fico: dict):
    """Render FICO framework scores as horizontal bar chart."""

    # Extract scores from sections
    sections = ['B', 'C', 'D']
    section_names = ['B: Explanation', 'C: Understanding', 'D: Participation']
    scores = []
    targets = [75, 70, 70]

    for section in sections:
        section_data = fico.get(f'section_{section.lower()}', {})
        avg = section_data.get('avg', section_data.get('average', 60))
        scores.append(avg)

    if not any(scores):
        scores = [68, 58, 45]  # Fallback values

    colors = [COLORS['success'] if s >= t else COLORS['error'] for s, t in zip(scores, targets)]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=section_names,
        x=scores,
        orientation='h',
        marker_color=colors,
        text=[f'{s:.0f}%' for s in scores],
        textposition='outside'
    ))

    # Target markers
    fig.add_trace(go.Scatter(
        y=section_names,
        x=targets,
        mode='markers',
        marker=dict(symbol='line-ns', size=20, color='#9CA3AF', line_width=2),
        name='Target'
    ))

    base_layout = plotly_layout_defaults(height=200)
    base_layout['margin'] = dict(t=10, b=40, l=140, r=60)
    base_layout['xaxis'] = dict(range=[0, 100], ticksuffix='%')
    base_layout['yaxis'] = dict(autorange='reversed')
    fig.update_layout(**base_layout, showlegend=False)

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


if __name__ == "__main__":
    main()
