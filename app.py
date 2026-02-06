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

# === PAGE CONFIG (must be first) ===
st.set_page_config(
    page_title="Taleemabad",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === IMPORTS ===
from components.sidebar import render_sidebar
from data.queries import (
    get_summary_metrics,
    get_fico_section_c_metrics,
    get_fico_section_d_metrics,
    get_observation_counts
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

    # === SIDEBAR (collapsed by default) ===
    filters = render_sidebar()

    # === STATUS BAR ===
    st.markdown(status_bar(filters["region"]), unsafe_allow_html=True)

    # === HERO METRIC: The #1 thing users should see ===
    metrics = get_summary_metrics(filters)
    fico_d = get_fico_section_d_metrics(filters)

    # The critical metric: Student talk time (our biggest gap)
    student_talk = fico_d['student_talk_time']
    target_talk = fico_d['target_student_time']

    # Color based on performance
    hero_color = score_color(student_talk, target_talk)

    st.markdown(
        hero_metric(
            f"{student_talk}%",
            "Student Talk Time",
            f"Target: {target_talk}% · Gap: {target_talk - student_talk:.0f} percentage points",
            color=hero_color
        ),
        unsafe_allow_html=True
    )

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

    st.markdown(divider(), unsafe_allow_html=True)

    # === MAIN INSIGHT: One story ===
    st.markdown(section_title("Key Insight"), unsafe_allow_html=True)

    fico_c = get_fico_section_c_metrics(filters)
    open_ratio = fico_c['open_question_ratio']

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(
            insight_card(
                f"""Teachers ask <strong>{fico_c["avg_closed_questions"]:.0f} closed questions</strong>
                for every <strong>{fico_c["avg_open_questions"]:.0f} open questions</strong>.
                <br><br>
                Only <strong>{open_ratio:.0f}%</strong> of questions encourage deeper thinking.
                Research suggests at least 40%."""
            ),
            unsafe_allow_html=True
        )

    with col2:
        # Simple donut chart showing question ratio
        fig = go.Figure(data=[go.Pie(
            values=[open_ratio, 100-open_ratio],
            hole=0.75,
            marker_colors=[COLORS['info'], '#E5E7EB'],
            textinfo='none',
            hoverinfo='skip'
        )])

        base_layout = plotly_layout_defaults(height=160)
        # Override margin for this compact chart
        base_layout['margin'] = dict(t=10, b=10, l=10, r=10)
        fig.update_layout(
            **base_layout,
            showlegend=False,
            annotations=[dict(
                text=f'{open_ratio:.0f}%',
                x=0.5, y=0.5,
                font_size=28,
                font_weight=600,
                font_color=COLORS['info'],
                font_family="Inter, -apple-system, sans-serif",
                showarrow=False
            )]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.caption("Open-ended questions")

    st.markdown(divider(), unsafe_allow_html=True)

    # === DRILL DOWN TABS ===
    st.markdown(section_title("Explore"), unsafe_allow_html=True)

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
    dimensions = ['A: Lesson Opening', 'B: Explanation', 'C: Understanding', 'D: Participation', 'E: Feedback', 'F: Closing']
    scores = [72, 68, 58, 45, 71, 65]
    targets = [75, 75, 70, 70, 70, 70]

    # Color based on whether meeting target
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

    base_layout = plotly_layout_defaults(height=320)
    # Override margin for this chart with labels on left
    base_layout['margin'] = dict(t=20, b=40, l=140, r=60)
    fig.update_layout(
        **base_layout,
        showlegend=False,
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor='#F3F4F6',
            zeroline=False,
            ticksuffix='%',
            tickfont=dict(size=11, color='#6B7280')
        ),
        yaxis=dict(showgrid=False, autorange='reversed', tickfont=dict(size=12, color='#374151'))
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
        st.markdown(
            metric_card(str(obs["ai_count"]), "AI Sessions", COLORS['info']),
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            metric_card(str(obs["human_count"]), "Human Observations", COLORS['success']),
            unsafe_allow_html=True
        )

    with col3:
        if obs['total'] > 0:
            ratio = obs['ai_count'] / max(obs['human_count'], 1)
            st.markdown(
                metric_card(f"{ratio:.1f}×", "AI Multiplier"),
                unsafe_allow_html=True
            )

    # Weekly trend (simplified)
    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)

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
        line=dict(color=COLORS['info'], width=2, shape='spline'),
        marker=dict(size=6, color=COLORS['info'], line=dict(color='white', width=1.5)),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.06)'
    ))
    fig.add_trace(go.Scatter(
        x=[d['week'] for d in trend_data],
        y=[d['human'] for d in trend_data],
        mode='lines+markers',
        name='Human',
        line=dict(color=COLORS['success'], width=2, shape='spline'),
        marker=dict(size=6, color=COLORS['success'], line=dict(color='white', width=1.5))
    ))

    base_layout = plotly_layout_defaults(height=220)
    fig.update_layout(
        **base_layout,
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
    st.markdown(
        insight_card(
            'Only <strong>34%</strong> of assessed students read at grade level. '
            '<span style="color: #6B7280;">National data shows 80% of Pakistani primary students cannot read appropriately.</span>',
            border_color=COLORS['error'],
            title="Reading Alert"
        ),
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
