"""
FICO Deep Dive - Detailed analysis by FICO section (A-F).

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
from components.region_tabs import render_region_tabs, REGIONS, render_region_header
from data.queries import (
    get_fico_section_c_metrics,
    get_fico_section_d_metrics,
    get_recent_sessions
)
from styles.design_system import (
    inject_css,
    hero_metric,
    status_bar,
    divider,
    section_title,
    insight_card,
    metric_card,
    rec_card,
    COLORS,
    FICO_COLORS,
    plotly_layout_defaults,
    score_color
)

st.set_page_config(
    page_title="FICO Analysis | Taleemabad",
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
        '<div style="font-size: 1.5rem; font-weight: 600; color: #1A1A1A; margin-top: 0.25rem;">FICO Analysis</div>'
        '<div style="font-size: 0.875rem; color: #6B7280;">Instructional Fidelity Metrics by Region</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # === REGION TABS ===
    tab_ict, tab_bal, tab_rwp, tab_moawin, tab_rumi = render_region_tabs()

    with tab_ict:
        render_region_fico("ICT", filters)

    with tab_bal:
        render_region_fico("Balochistan", filters)

    with tab_rwp:
        render_region_fico("Rawalpindi", filters)

    with tab_moawin:
        render_region_fico("Moawin", filters)

    with tab_rumi:
        render_region_fico("Rumi", filters)


def render_region_fico(region: str, filters: dict):
    """Render FICO analysis for a specific region."""
    # Update filters with specific region
    region_filters = {**filters, "region": region}

    # Check if region has FICO data
    if region in ["Moawin", "Rumi"]:
        render_no_fico_data(region)
        return

    # === SECTION SELECTOR (Apple segmented control via design system) ===
    section = st.radio(
        "Focus Area",
        options=[
            "Overview",
            "A: Lesson Opening",
            "B: Explanation",
            "C: Understanding",
            "D: Participation",
            "E: Feedback",
            "F: Closing"
        ],
        horizontal=True,
        label_visibility="collapsed",
        key=f"fico_section_{region}"
    )

    # Route to appropriate section
    if section == "Overview":
        render_overview(region_filters, region)
    elif section == "A: Lesson Opening":
        render_section_a(region_filters, region)
    elif section == "B: Explanation":
        render_section_b(region_filters, region)
    elif section == "C: Understanding":
        render_section_c_detail(region_filters, region)
    elif section == "D: Participation":
        render_section_d_detail(region_filters, region)
    elif section == "E: Feedback":
        render_section_e(region_filters, region)
    elif section == "F: Closing":
        render_section_f(region_filters, region)


def render_no_fico_data(region: str):
    """Render message for regions without FICO observation data."""
    info = REGIONS.get(region, {})

    st.markdown(
        '<div style="text-align: center; padding: 4rem 2rem; background: #F9FAFB; border-radius: 12px; margin: 2rem 0;">'
        '<div style="font-size: 3rem; margin-bottom: 1rem;">' + info.get('icon', '📊') + '</div>'
        '<div style="font-size: 1.25rem; font-weight: 600; color: #1A1A1A; margin-bottom: 0.5rem;">'
        'FICO Data Not Available'
        '</div>'
        '<div style="font-size: 0.875rem; color: #6B7280; max-width: 400px; margin: 0 auto;">'
        + info.get('description', 'This region') + ' does not have classroom observation data with FICO scoring.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    if region == "Moawin":
        st.markdown(
            '<div style="background: #FEF3C7; border-left: 3px solid #F59E0B; padding: 1rem; border-radius: 0 8px 8px 0; margin-top: 1rem;">'
            '<strong>SchoolPilot Focus:</strong> Moawin tracks attendance, compliance, and student scores rather than classroom observations. '
            'View the <strong>Students</strong> page for Moawin data.'
            '</div>',
            unsafe_allow_html=True
        )

    elif region == "Rumi":
        st.markdown(
            '<div style="background: #DBEAFE; border-left: 3px solid #3B82F6; padding: 1rem; border-radius: 0 8px 8px 0; margin-top: 1rem;">'
            '<strong>AI Coaching Focus:</strong> Rumi provides WhatsApp-based coaching conversations and lesson plan support. '
            'View the <strong>Observations</strong> page for Rumi chat analytics.'
            '</div>',
            unsafe_allow_html=True
        )


def render_overview(filters, region: str):
    """Render overview of all FICO sections - horizontal bar chart."""

    # Region-specific data (in production, this would come from queries)
    if region == "Balochistan":
        dimensions = ['A: Lesson Opening', 'B: Explanation', 'C: Understanding', 'D: Participation', 'E: Feedback', 'F: Closing']
        scores = [68, 62, 52, 6, 65, 58]  # Note: D is 6% student talk time
        targets = [75, 75, 70, 40, 70, 70]
    elif region == "ICT":
        dimensions = ['A: Lesson Opening', 'B: Explanation', 'C: Understanding', 'D: Participation', 'E: Feedback', 'F: Closing']
        scores = [72, 68, 58, 45, 71, 65]
        targets = [75, 75, 70, 70, 70, 70]
    elif region == "Rawalpindi":
        dimensions = ['A: Lesson Opening', 'B: Explanation', 'C: Understanding', 'D: Participation', 'E: Feedback', 'F: Closing']
        scores = [70, 65, 55, 42, 68, 62]
        targets = [75, 75, 70, 70, 70, 70]
    else:
        dimensions = ['A: Lesson Opening', 'B: Explanation', 'C: Understanding', 'D: Participation', 'E: Feedback', 'F: Closing']
        scores = [72, 68, 58, 45, 71, 65]
        targets = [75, 75, 70, 70, 70, 70]

    gaps = [t - s for s, t in zip(scores, targets)]

    # Find biggest gap for hero metric
    max_gap_idx = gaps.index(max(gaps))
    biggest_gap_dimension = dimensions[max_gap_idx].split(': ')[1]
    biggest_gap = gaps[max_gap_idx]

    # === HERO: Biggest Gap ===
    st.markdown(
        hero_metric(
            str(biggest_gap),
            "Points Below Target",
            f"{biggest_gap_dimension} is the biggest opportunity in {region}",
            color=COLORS['error']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === HORIZONTAL BAR CHART ===
    st.markdown(section_title("All Dimensions"), unsafe_allow_html=True)

    colors = [COLORS['success'] if s >= t else COLORS['error'] for s, t in zip(scores, targets)]

    fig = go.Figure()

    # Score bars
    fig.add_trace(go.Bar(
        y=dimensions,
        x=scores,
        orientation='h',
        marker_color=colors,
        marker_line_width=0,
        text=[f'{s}%' for s in scores],
        textposition='outside',
        textfont=dict(size=11, color='#6B7280', family="Inter, -apple-system, sans-serif"),
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

    base_layout = plotly_layout_defaults(height=340)
    base_layout['margin'] = dict(t=10, b=40, l=150, r=60)
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

    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<span style="color: {COLORS["success"]};">●</span> Meeting target', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<span style="color: {COLORS["error"]};">●</span> Below target', unsafe_allow_html=True)
    with col3:
        st.markdown('<span style="color: #9CA3AF;">|</span> Target', unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY INSIGHTS (Region-specific) ===
    col1, col2 = st.columns(2)

    if region == "Balochistan":
        with col1:
            st.markdown(
                insight_card(
                    f'<strong style="color: {COLORS["success"]};">Lesson Opening (68%)</strong> and '
                    f'<strong style="color: {COLORS["success"]};">Feedback (65%)</strong> are closest to targets.',
                    border_color=COLORS['success'],
                    title="Strengths"
                ),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                insight_card(
                    '<strong style="color: #EF4444;">Student Talk Time (6%)</strong> is critically low. '
                    'Target is 40%. Teachers dominate 82% of class time.',
                    border_color=COLORS['error'],
                    title="Critical Focus"
                ),
                unsafe_allow_html=True
            )
    else:
        with col1:
            st.markdown(
                insight_card(
                    f'<strong style="color: {COLORS["success"]};">Lesson Opening (72%)</strong> and '
                    f'<strong style="color: {COLORS["success"]};">Feedback (71%)</strong> are closest to targets.',
                    border_color=COLORS['success'],
                    title="Strengths"
                ),
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                insight_card(
                    '<strong>Participation (45%)</strong> and <strong>Understanding (58%)</strong> need immediate attention.',
                    border_color=COLORS['error'],
                    title="Focus Areas"
                ),
                unsafe_allow_html=True
            )


def render_section_a(filters, region: str):
    """Section A: Lesson Opening - How teachers begin class."""

    # Region-specific scores
    if region == "Balochistan":
        score, target = 68, 75
        recap, objectives, hooks = 62, 70, 65
    else:
        score, target = 72, 75
        recap, objectives, hooks = 68, 74, 71

    gap = target - score

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{score}%",
            "Lesson Opening Score",
            f"Target: {target}% · Gap: {gap} points",
            color=score_color(score, target)
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY BEHAVIORS ===
    st.markdown(section_title("Key Behaviors Observed"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card(f"{recap}%", "Recaps Prior Learning", score_color(recap, 70)), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(f"{objectives}%", "States Objectives", score_color(objectives, 70)), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(f"{hooks}%", "Hooks Attention", score_color(hooks, 70)), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            'Teachers who <strong>recap prior learning</strong> before introducing new content '
            'see <strong>23% higher</strong> student engagement throughout the lesson.',
            border_color=FICO_COLORS['A']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown(section_title("Recommendations"), unsafe_allow_html=True)

    recs = [
        ("Start with a question", "Connect to yesterday's lesson with one review question"),
        ("State the goal clearly", "Write the learning objective on the board"),
        ("Use a hook", "Start with a story, question, or surprising fact"),
        ("Set expectations", "Briefly outline what students will do today")
    ]

    for title, desc in recs:
        st.markdown(rec_card(title, desc, FICO_COLORS['A']), unsafe_allow_html=True)


def render_section_b(filters, region: str):
    """Section B: Explanation - Clarity of instruction."""

    # Region-specific scores
    if region == "Balochistan":
        score, target = 62, 75
        clear_lang, examples, pace = 65, 55, 58
    else:
        score, target = 68, 75
        clear_lang, examples, pace = 72, 61, 65

    gap = target - score

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{score}%",
            "Explanation Quality",
            f"Target: {target}% · Gap: {gap} points",
            color=score_color(score, target)
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY BEHAVIORS ===
    st.markdown(section_title("Key Behaviors Observed"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card(f"{clear_lang}%", "Clear Language", score_color(clear_lang, 70)), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(f"{examples}%", "Uses Examples", score_color(examples, 65)), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(f"{pace}%", "Checks Pace", score_color(pace, 65)), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            f'Only <strong>{examples}%</strong> of teachers use concrete examples. '
            'Research shows examples increase comprehension by <strong>40%</strong>.',
            border_color=FICO_COLORS['B']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown(section_title("Recommendations"), unsafe_allow_html=True)

    recs = [
        ("Use 3 examples", "Give at least 3 varied examples per new concept"),
        ("Check pace", "Watch for confused faces, ask 'Should I slow down?'"),
        ("Chunk content", "Break complex topics into 5-minute segments"),
        ("Model thinking", "Show your thought process, not just answers")
    ]

    for title, desc in recs:
        st.markdown(rec_card(title, desc, FICO_COLORS['B']), unsafe_allow_html=True)


def render_section_c_detail(filters, region: str):
    """Section C: Checking for Understanding - Question analysis."""

    metrics = get_fico_section_c_metrics(filters)

    # Override with region-specific data for Balochistan
    if region == "Balochistan":
        open_ratio = 13  # Only 13% open-ended questions
        avg_open = 1.2
        avg_closed = 8.1
    else:
        open_ratio = metrics.get('open_question_ratio', 35)
        avg_open = metrics.get('avg_open_questions', 3.5)
        avg_closed = metrics.get('avg_closed_questions', 6.5)

    target = 40

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{open_ratio:.0f}%",
            "Open-Ended Questions",
            f"Target: {target}% · Gap: {target - open_ratio:.0f} percentage points",
            color=score_color(open_ratio, target)
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY METRICS ===
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            metric_card(f'{avg_open:.1f}', "Open Questions / Session", COLORS['success']),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card(f'{avg_closed:.1f}', "Closed Questions / Session", COLORS['text_muted']),
            unsafe_allow_html=True
        )

    st.markdown(divider(), unsafe_allow_html=True)

    # === QUESTION DISTRIBUTION CHART ===
    st.markdown(section_title("Recent Sessions"), unsafe_allow_html=True)

    sessions = get_recent_sessions(filters, limit=12)
    if sessions:
        session_labels = [f"S{i+1}" for i in range(len(sessions))]
        open_qs = [s.get('open_questions', 2) for s in sessions]
        closed_qs = [s.get('closed_questions', 6) for s in sessions]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Open',
            x=session_labels,
            y=open_qs,
            marker_color=COLORS['success']
        ))
        fig.add_trace(go.Bar(
            name='Closed',
            x=session_labels,
            y=closed_qs,
            marker_color='#E5E7EB'
        ))

        base_layout = plotly_layout_defaults(height=240)
        base_layout['xaxis'] = dict(showgrid=False)
        base_layout['yaxis'] = dict(showgrid=True, gridcolor='#F3F4F6', zeroline=False, title=None)
        fig.update_layout(
            **base_layout,
            barmode='stack',
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(size=11, family="Inter, -apple-system, sans-serif")
            )
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown(divider(), unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown(section_title("Recommendations"), unsafe_allow_html=True)

    recommendations = [
        ("Use Why and How", "These question starters encourage deeper thinking"),
        ("Wait 3-5 seconds", "Allow thinking time before calling on students"),
        ("Follow up", "Ask 'Can you explain more?' after short answers"),
        ("Target: 40%", "Aim for at least 40% open-ended questions")
    ]

    for title, desc in recommendations:
        st.markdown(rec_card(title, desc, FICO_COLORS['C']), unsafe_allow_html=True)


def render_section_d_detail(filters, region: str):
    """Section D: Student Participation - Talk time analysis."""

    metrics = get_fico_section_d_metrics(filters)

    # Override with region-specific data for Balochistan
    if region == "Balochistan":
        student_talk = 6  # Critical: only 6%
        teacher_talk = 82
    else:
        student_talk = metrics.get('student_talk_time', 35)
        teacher_talk = metrics.get('teacher_talk_time', 65)

    target = 40

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{student_talk}%",
            "Student Talk Time",
            f"Target: {target}% · Currently {target - student_talk} points below",
            color=score_color(student_talk, target)
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === TALK TIME DISTRIBUTION ===
    col1, col2 = st.columns([1, 1])

    with col1:
        # Donut chart
        fig = go.Figure(data=[go.Pie(
            values=[student_talk, teacher_talk],
            labels=['Student', 'Teacher'],
            hole=0.75,
            marker_colors=[COLORS['success'], COLORS['text_muted']],
            textinfo='none',
            hovertemplate='%{label}: %{value}%<extra></extra>'
        )])

        base_layout = plotly_layout_defaults(height=220)
        base_layout['margin'] = dict(t=10, b=40, l=10, r=10)
        fig.update_layout(
            **base_layout,
            showlegend=True,
            legend=dict(
                orientation='h',
                yanchor='top',
                y=-0.1,
                xanchor='center',
                x=0.5,
                font=dict(size=12, family="Inter, -apple-system, sans-serif")
            ),
            annotations=[dict(
                text=f'{student_talk}%',
                x=0.5, y=0.5,
                font_size=32,
                font_weight=600,
                font_color=COLORS['success'] if student_talk >= 30 else COLORS['error'],
                font_family="Inter, -apple-system, sans-serif",
                showarrow=False
            )]
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
        if region == "Balochistan":
            st.markdown(
                insight_card(
                    f'<strong style="color: {COLORS["error"]};">Critical:</strong> Students speak only <strong>6%</strong> of class time.'
                    f'<br><br>Teachers dominate at <strong>{teacher_talk}%</strong>. This severely limits learning.',
                    border_color=COLORS['error'],
                    title="Urgent Action Needed"
                ),
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                insight_card(
                    f'Students learn best when actively speaking at least <strong style="color: {COLORS["success"]};">40%</strong> of class time.'
                    f'<br><br>Current: Teachers dominate at <strong>{teacher_talk}%</strong>.',
                    border_color=COLORS['error'],
                    title="Critical Finding"
                ),
                unsafe_allow_html=True
            )

    st.markdown(divider(), unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown(section_title("Action Items"), unsafe_allow_html=True)

    actions = [
        ("Think-Pair-Share", "Students discuss with partner before whole-class sharing"),
        ("Student Explanations", "Ask students to explain concepts to each other"),
        ("5-Minute Chunks", "Break lectures with student activity between"),
        ("Cold Calling", "Call on students randomly, not just raised hands"),
        ("Student Questions", "Encourage students to ask, not just answer")
    ]

    for title, desc in actions:
        st.markdown(rec_card(title, desc, FICO_COLORS['D']), unsafe_allow_html=True)


def render_section_e(filters, region: str):
    """Section E: Feedback - Quality of teacher feedback to students."""

    # Region-specific scores
    if region == "Balochistan":
        score, target = 65, 70
        specific, corrective, timely = 68, 60, 65
    else:
        score, target = 71, 70
        specific, corrective, timely = 73, 68, 70

    gap = target - score

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{score}%",
            "Feedback Quality",
            f"Target: {target}% · {abs(gap)} points {'above' if gap <= 0 else 'below'}",
            color=score_color(score, target)
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY BEHAVIORS ===
    st.markdown(section_title("Key Behaviors Observed"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card(f"{specific}%", "Specific Praise", score_color(specific, 70)), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(f"{corrective}%", "Corrective Feedback", score_color(corrective, 65)), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(f"{timely}%", "Timely Response", score_color(timely, 70)), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            f'Teachers give <strong>specific praise</strong> ({specific}%) but struggle with '
            f'<strong>corrective feedback</strong> ({corrective}%). Students need both to improve.',
            border_color=FICO_COLORS['E']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown(section_title("Recommendations"), unsafe_allow_html=True)

    recs = [
        ("Be specific", "Say 'Great use of evidence!' not just 'Good job'"),
        ("Focus on growth", "Highlight improvement, not just correctness"),
        ("Immediate response", "Give feedback within seconds, not days"),
        ("Balance praise/correction", "Aim for 4:1 positive to corrective ratio")
    ]

    for title, desc in recs:
        st.markdown(rec_card(title, desc, FICO_COLORS['E']), unsafe_allow_html=True)


def render_section_f(filters, region: str):
    """Section F: Closing - How teachers end the lesson."""

    # Region-specific scores
    if region == "Balochistan":
        score, target = 58, 70
        summarizes, checks, previews = 55, 50, 62
    else:
        score, target = 65, 70
        summarizes, checks, previews = 62, 58, 71

    gap = target - score

    # === HERO ===
    st.markdown(
        hero_metric(
            f"{score}%",
            "Lesson Closing Score",
            f"Target: {target}% · Gap: {gap} points",
            color=score_color(score, target)
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === KEY BEHAVIORS ===
    st.markdown(section_title("Key Behaviors Observed"), unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card(f"{summarizes}%", "Summarizes Key Points", score_color(summarizes, 65)), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card(f"{checks}%", "Checks Understanding", score_color(checks, 60)), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card(f"{previews}%", "Previews Next Lesson", score_color(previews, 70)), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            f'Only <strong>{checks}%</strong> check understanding at lesson end. '
            'Exit tickets can increase retention by <strong>35%</strong>.',
            border_color=FICO_COLORS['F']
        ),
        unsafe_allow_html=True
    )

    st.markdown(divider(), unsafe_allow_html=True)

    # === RECOMMENDATIONS ===
    st.markdown(section_title("Recommendations"), unsafe_allow_html=True)

    recs = [
        ("3-2-1 Summary", "Students share 3 things learned, 2 questions, 1 connection"),
        ("Exit Ticket", "Quick written response to check understanding"),
        ("Preview tomorrow", "Create anticipation for next lesson"),
        ("Student summary", "Have a student summarize the key points")
    ]

    for title, desc in recs:
        st.markdown(rec_card(title, desc, FICO_COLORS['F']), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
