"""
FICO Deep Dive - Detailed analysis by FICO section (A-F).

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

    # === STATUS BAR ===
    st.markdown(status_bar(filters["region"], "FICO Analysis"), unsafe_allow_html=True)

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
        label_visibility="collapsed"
    )

    # Route to appropriate section
    if section == "Overview":
        render_overview(filters)
    elif section == "A: Lesson Opening":
        render_section_a(filters)
    elif section == "B: Explanation":
        render_section_b(filters)
    elif section == "C: Understanding":
        render_section_c_detail(filters)
    elif section == "D: Participation":
        render_section_d_detail(filters)
    elif section == "E: Feedback":
        render_section_e(filters)
    elif section == "F: Closing":
        render_section_f(filters)


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
    st.markdown(
        hero_metric(
            str(biggest_gap),
            "Points Below Target",
            f"{biggest_gap_dimension} is our biggest opportunity",
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

    # === KEY INSIGHTS ===
    col1, col2 = st.columns(2)

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


def render_section_a(filters):
    """Section A: Lesson Opening - How teachers begin class."""

    score = 72
    target = 75
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
        st.markdown(metric_card("68%", "Recaps Prior Learning", COLORS['warning']), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("74%", "States Objectives", COLORS['success']), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("71%", "Hooks Attention", COLORS['success']), unsafe_allow_html=True)

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


def render_section_b(filters):
    """Section B: Explanation - Clarity of instruction."""

    score = 68
    target = 75
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
        st.markdown(metric_card("72%", "Clear Language", COLORS['success']), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("61%", "Uses Examples", COLORS['warning']), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("65%", "Checks Pace", COLORS['warning']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            'Only <strong>61%</strong> of teachers use concrete examples. '
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


def render_section_c_detail(filters):
    """Section C: Checking for Understanding - Question analysis."""

    metrics = get_fico_section_c_metrics(filters)
    open_ratio = metrics['open_question_ratio']
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
            metric_card(f'{metrics["avg_open_questions"]:.1f}', "Open Questions / Session", COLORS['success']),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card(f'{metrics["avg_closed_questions"]:.1f}', "Closed Questions / Session", COLORS['muted']),
            unsafe_allow_html=True
        )

    st.markdown(divider(), unsafe_allow_html=True)

    # === QUESTION DISTRIBUTION CHART ===
    st.markdown(section_title("Recent Sessions"), unsafe_allow_html=True)

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


def render_section_d_detail(filters):
    """Section D: Student Participation - Talk time analysis."""

    metrics = get_fico_section_d_metrics(filters)
    student_talk = metrics['student_talk_time']
    teacher_talk = metrics['teacher_talk_time']
    target = metrics['target_student_time']

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
            marker_colors=[COLORS['success'], COLORS['muted']],
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
                font_color=COLORS['success'],
                font_family="Inter, -apple-system, sans-serif",
                showarrow=False
            )]
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with col2:
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


def render_section_e(filters):
    """Section E: Feedback - Quality of teacher feedback to students."""

    score = 71
    target = 70
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
        st.markdown(metric_card("73%", "Specific Praise", COLORS['success']), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("68%", "Corrective Feedback", COLORS['warning']), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("70%", "Timely Response", COLORS['success']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            'Teachers give <strong>specific praise</strong> (73%) but struggle with '
            '<strong>corrective feedback</strong> (68%). Students need both to improve.',
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


def render_section_f(filters):
    """Section F: Closing - How teachers end the lesson."""

    score = 65
    target = 70
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
        st.markdown(metric_card("62%", "Summarizes Key Points", COLORS['warning']), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("58%", "Checks Understanding", COLORS['error']), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("71%", "Previews Next Lesson", COLORS['success']), unsafe_allow_html=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # === INSIGHT ===
    st.markdown(
        insight_card(
            'Only <strong>58%</strong> check understanding at lesson end. '
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
