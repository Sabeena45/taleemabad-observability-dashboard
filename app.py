"""
Taleemabad Observability Dashboard
Cross-Region Comparison Dashboard with 6 common metrics.

Design Philosophy:
- Five-second rule: Most important insight visible immediately
- Cross-region comparison: Same 6 metrics across all 5 regions
- Definitions included: User knows how each metric is calculated
- "No data available" shown clearly when data doesn't exist
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# === PAGE CONFIG (must be first) ===
st.set_page_config(
    page_title="Taleemabad Observability",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === IMPORTS ===
from components.sidebar import render_sidebar
from data.common_metrics import (
    get_observation_metrics,
    get_lp_engagement_metrics,
    get_training_metrics,
    get_retention_metrics,
    get_fico_metrics,
    get_student_learning_metrics,
    METRIC_DEFINITIONS,
    REGION_PARAMETERS,
    REGIONS,
    REGION_COLORS,
)
from data.cache_layer import data_freshness_banner, clear_all_caches
from styles.design_system import (
    inject_css,
    section_title,
    insight_card,
    divider,
    COLORS,
    plotly_layout_defaults,
)

# === INJECT DESIGN SYSTEM ===
inject_css()

# Consistent region order
REGION_ORDER = ["ICT", "Balochistan", "RWP", "Moawin", "Rumi"]
REGION_LABELS = {
    "ICT": "ICT",
    "Balochistan": "Balochistan",
    "RWP": "Rawalpindi",
    "Moawin": "Moawin",
    "Rumi": "Rumi",
}


def _no_data_text(status: str) -> str:
    """Return display text for non-active statuses."""
    if status == "not_applicable":
        return "N/A"
    if status == "launching_q2_2026":
        return "Launching Q2 2026"
    return "No data"


def _metric_definition_expander(key: str):
    """Render a metric definition in a small expander."""
    defn = METRIC_DEFINITIONS.get(key, {})
    with st.expander(f"How is this calculated?", expanded=False):
        st.caption(defn.get("definition", ""))


def main():
    """Main dashboard entry point."""
    filters = render_sidebar()

    # === HEADER ===
    st.markdown(
        '<div style="padding: 0.5rem 0 0.25rem 0;">'
        '<div style="font-size: 0.625rem; font-weight: 600; color: #9CA3AF; '
        'text-transform: uppercase; letter-spacing: 0.15em;">TALEEMABAD</div>'
        '<div style="font-size: 1.5rem; font-weight: 600; color: #1A1A1A;">'
        'Observability Dashboard</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # === DATA FRESHNESS BANNER ===
    st.markdown(data_freshness_banner(), unsafe_allow_html=True)

    # === REFRESH BUTTON (sidebar) ===
    with st.sidebar:
        if st.button("Refresh Data"):
            clear_all_caches()
            st.rerun()

    # === REGION PARAMETERS SUMMARY ===
    _render_region_summary()

    st.markdown(divider(), unsafe_allow_html=True)

    # === 6 METRIC SECTIONS ===
    _render_observations_section()
    st.markdown(divider(), unsafe_allow_html=True)

    _render_lp_engagement_section()
    st.markdown(divider(), unsafe_allow_html=True)

    _render_training_section()
    st.markdown(divider(), unsafe_allow_html=True)

    _render_retention_section()
    st.markdown(divider(), unsafe_allow_html=True)

    _render_fico_section()
    st.markdown(divider(), unsafe_allow_html=True)

    _render_student_learning_section()
    st.markdown(divider(), unsafe_allow_html=True)

    # === SUMMARY TABLE ===
    _render_summary_table()


# =============================================================================
# REGION SUMMARY
# =============================================================================

def _render_region_summary():
    """Show region parameters at a glance."""
    cols = st.columns(5)
    for i, region in enumerate(REGION_ORDER):
        params = REGION_PARAMETERS.get(region, {})
        with cols[i]:
            color = REGION_COLORS[region]
            schools = params.get("schools", "—")
            teachers = params.get("teachers", "—")
            students = params.get("students", "—")
            schools_str = f"{schools:,}" if isinstance(schools, int) else str(schools)
            teachers_str = f"{teachers:,}" if isinstance(teachers, int) else str(teachers)
            students_str = f"{students:,}" if isinstance(students, int) else str(students)

            st.markdown(
                f'<div style="border-left: 3px solid {color}; padding: 0.5rem 0.75rem; '
                f'background: #FAFAFA; border-radius: 4px;">'
                f'<div style="font-size: 0.8125rem; font-weight: 600; color: {color};">'
                f'{REGION_LABELS[region]}</div>'
                f'<div style="font-size: 0.6875rem; color: #6B7280; margin-top: 0.25rem;">'
                f'{schools_str} schools · {teachers_str} teachers</div>'
                f'<div style="font-size: 0.6875rem; color: #9CA3AF;">'
                f'{students_str} students</div>'
                f'</div>',
                unsafe_allow_html=True
            )


# =============================================================================
# SECTION 1: OBSERVATIONS
# =============================================================================

def _render_observations_section():
    st.markdown(section_title("1. Observations (vs Benchmark)"), unsafe_allow_html=True)
    _metric_definition_expander("observations")

    data = get_observation_metrics()

    # Build chart data
    regions_active = []
    actuals = []
    benchmarks = []
    bar_colors = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")

        if status == "active" and d.get("actual") is not None:
            regions_active.append(REGION_LABELS[region])
            actuals.append(d["actual"])
            benchmarks.append(d.get("benchmark_monthly"))
            bar_colors.append(REGION_COLORS[region])
        else:
            annotations.append(f"**{REGION_LABELS[region]}**: {_no_data_text(status)}")

    if actuals:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=regions_active,
            y=actuals,
            name="Actual",
            marker_color=bar_colors,
            text=[f"{v:,}" for v in actuals],
            textposition="outside",
        ))

        # Add benchmark markers where available
        bm_x = [r for r, b in zip(regions_active, benchmarks) if b is not None]
        bm_y = [b for b in benchmarks if b is not None]
        if bm_x:
            fig.add_trace(go.Scatter(
                x=bm_x,
                y=bm_y,
                mode="markers",
                marker=dict(symbol="line-ew-open", size=16, color="#9CA3AF", line_width=3),
                name="Monthly Benchmark",
            ))

        base_layout = plotly_layout_defaults(height=300)
        base_layout["showlegend"] = bool(bm_x)
        base_layout["legend"] = dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11)
        )
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if annotations:
        st.caption(" · ".join(annotations))


# =============================================================================
# SECTION 2: LESSON PLAN ENGAGEMENT
# =============================================================================

def _render_lp_engagement_section():
    st.markdown(section_title("2. Lesson Plan Engagement"), unsafe_allow_html=True)
    _metric_definition_expander("lp_engagement")

    data = get_lp_engagement_metrics()

    regions_show = []
    values = []
    bar_colors = []
    hover_texts = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")

        if status == "active" and d.get("total_events", 0) > 0:
            regions_show.append(REGION_LABELS[region])
            total = d["total_events"]
            values.append(total)
            bar_colors.append(REGION_COLORS[region])
            teachers = d.get("unique_teachers", 0)
            per_t = d.get("per_teacher", 0)
            extra = d.get("type", "")
            hover = f"Total: {total:,}<br>Teachers: {teachers:,}<br>Per teacher: {per_t}"
            if extra:
                hover += f"<br>Type: {extra}"
            hover_texts.append(hover)
        else:
            annotations.append(f"**{REGION_LABELS[region]}**: {_no_data_text(status)}")

    if values:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=regions_show,
            x=values,
            orientation="h",
            marker_color=bar_colors,
            text=[f"{v:,}" for v in values],
            textposition="outside",
            hovertext=hover_texts,
            hoverinfo="text",
        ))

        base_layout = plotly_layout_defaults(height=250)
        base_layout["margin"] = dict(t=10, b=40, l=100, r=80)
        base_layout["yaxis"] = dict(autorange="reversed")
        base_layout["showlegend"] = False
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if annotations:
        st.caption(" · ".join(annotations))


# =============================================================================
# SECTION 3: TEACHER TRAINING ENGAGEMENT
# =============================================================================

def _render_training_section():
    st.markdown(section_title("3. Teacher Training Engagement"), unsafe_allow_html=True)
    _metric_definition_expander("training")

    data = get_training_metrics()

    regions_show = []
    values = []
    bar_colors = []
    hover_texts = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")

        if status == "not_applicable":
            annotations.append(f"**{REGION_LABELS[region]}**: N/A (coaching only)")
            continue

        total = d.get("total_submissions", 0) or 0
        if status == "active" and total > 0:
            regions_show.append(REGION_LABELS[region])
            values.append(total)
            bar_colors.append(REGION_COLORS[region])
            teachers = d.get("unique_teachers", 0)
            per_t = d.get("per_teacher", 0)
            hover_texts.append(
                f"Submissions: {total:,}<br>Teachers: {teachers:,}<br>Per teacher: {per_t}"
            )
        else:
            annotations.append(f"**{REGION_LABELS[region]}**: {_no_data_text(status)}")

    if values:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=regions_show,
            x=values,
            orientation="h",
            marker_color=bar_colors,
            text=[f"{v:,}" for v in values],
            textposition="outside",
            hovertext=hover_texts,
            hoverinfo="text",
        ))

        base_layout = plotly_layout_defaults(height=250)
        base_layout["margin"] = dict(t=10, b=40, l=100, r=80)
        base_layout["yaxis"] = dict(autorange="reversed")
        base_layout["showlegend"] = False
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if annotations:
        st.caption(" · ".join(annotations))


# =============================================================================
# SECTION 4: RETENTION
# =============================================================================

def _render_retention_section():
    st.markdown(section_title("4. Retention (7-day & 30-day)"), unsafe_allow_html=True)
    _metric_definition_expander("retention")

    data = get_retention_metrics()

    regions_show = []
    ret_7d = []
    ret_30d = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")
        r7 = d.get("retention_7d", 0)
        r30 = d.get("retention_30d", 0)

        if status == "active" and (r7 > 0 or r30 > 0):
            regions_show.append(REGION_LABELS[region])
            ret_7d.append(r7)
            ret_30d.append(r30)
        else:
            annotations.append(
                f"**{REGION_LABELS[region]}**: {_no_data_text(status)}"
                + (f" ({d.get('total_users', 0):,} users)" if d.get("total_users") else "")
            )

    if regions_show:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=regions_show, y=ret_7d,
            name="7-day",
            marker_color="#3B82F6",
            text=[f"{v:.1f}%" for v in ret_7d],
            textposition="outside",
        ))
        fig.add_trace(go.Bar(
            x=regions_show, y=ret_30d,
            name="30-day",
            marker_color="#93C5FD",
            text=[f"{v:.1f}%" for v in ret_30d],
            textposition="outside",
        ))

        base_layout = plotly_layout_defaults(height=300)
        base_layout["barmode"] = "group"
        base_layout["yaxis"] = dict(ticksuffix="%", range=[0, max(max(ret_30d, default=0), max(ret_7d, default=0)) * 1.3])
        base_layout["legend"] = dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11)
        )
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No retention data available yet. Data will appear when users have activity in the last 30 days.")

    if annotations:
        st.caption(" · ".join(annotations))


# =============================================================================
# SECTION 5: FICO SCORES
# =============================================================================

def _render_fico_section():
    st.markdown(section_title("5. FICO / Observation Scores by Section"), unsafe_allow_html=True)
    _metric_definition_expander("fico")

    data = get_fico_metrics()

    # Only ICT and Balochistan have FICO data
    regions_with_data = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")
        if status == "active":
            regions_with_data.append(region)
        elif status == "not_applicable":
            annotations.append(f"**{REGION_LABELS[region]}**: N/A")
        else:
            annotations.append(f"**{REGION_LABELS[region]}**: No data")

    if regions_with_data:
        sections = ["Section B", "Section C", "Section D"]

        fig = go.Figure()
        for region in regions_with_data:
            d = data[region]
            fig.add_trace(go.Bar(
                x=sections,
                y=[d.get("b_avg", 0), d.get("c_avg", 0), d.get("d_avg", 0)],
                name=f"{REGION_LABELS[region]} ({d.get('type', '')})",
                marker_color=REGION_COLORS[region],
                text=[f"{d.get('b_avg', 0):.0f}%", f"{d.get('c_avg', 0):.0f}%", f"{d.get('d_avg', 0):.0f}%"],
                textposition="outside",
            ))

        base_layout = plotly_layout_defaults(height=300)
        base_layout["barmode"] = "group"
        base_layout["yaxis"] = dict(range=[0, 100], ticksuffix="%")
        base_layout["legend"] = dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11)
        )
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # Insight
        if "ICT" in regions_with_data and "Balochistan" in regions_with_data:
            ict_d = data["ICT"]
            bal_d = data["Balochistan"]
            st.markdown(
                insight_card(
                    f"ICT uses <strong>TEACH Tool (human observers)</strong> while Balochistan uses "
                    f"<strong>AI + Human</strong> scoring. "
                    f"Section D (Participation) is weakest across both regions: "
                    f"ICT {ict_d.get('d_avg', 0):.0f}%, Balochistan {bal_d.get('d_avg', 0):.0f}%.",
                    title="Cross-Region FICO Comparison"
                ),
                unsafe_allow_html=True
            )
    else:
        st.info("FICO score data is only available for regions with classroom observations (ICT and Balochistan).")

    if annotations:
        st.caption(" · ".join(annotations))


# =============================================================================
# SECTION 6: STUDENT LEARNING
# =============================================================================

def _render_student_learning_section():
    st.markdown(section_title("6. Student Learning"), unsafe_allow_html=True)
    _metric_definition_expander("student_learning")

    data = get_student_learning_metrics()

    col1, col2, col3 = st.columns(3)
    annotations = []

    # ICT: Effect size
    ict = data.get("ICT", {})
    with col1:
        if ict.get("status") == "active":
            es = ict.get("effect_size", 0.46)
            st.markdown(
                f'<div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 1rem; text-align: center;">'
                f'<div style="font-size: 2rem; font-weight: 700; color: {REGION_COLORS["ICT"]};">{es}</div>'
                f'<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">Effect Size (Cohen\'s d)</div>'
                f'<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">ICT · RCT-validated</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            annotations.append("**ICT**: No data")

    # Moawin: Assessment scores
    moawin = data.get("Moawin", {})
    with col2:
        if moawin.get("status") == "active":
            avg = moawin.get("avg_score", 0)
            pr = moawin.get("avg_pass_rate", 0)
            total = moawin.get("total_assessments", 0)
            st.markdown(
                f'<div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 1rem; text-align: center;">'
                f'<div style="font-size: 2rem; font-weight: 700; color: {REGION_COLORS["Moawin"]};">{avg:.0f}%</div>'
                f'<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">Avg Assessment Score</div>'
                f'<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
                f'Moawin · {pr:.0f}% pass rate · {total:,} assessments</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            annotations.append("**Moawin**: No data")

    # Rumi: Reading assessments
    rumi = data.get("Rumi", {})
    with col3:
        if rumi.get("status") == "active":
            total = rumi.get("total_assessments", 197)
            st.markdown(
                f'<div style="border: 1px solid #E5E7EB; border-radius: 8px; padding: 1rem; text-align: center;">'
                f'<div style="font-size: 2rem; font-weight: 700; color: {REGION_COLORS["Rumi"]};">{total}</div>'
                f'<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">WCPM Assessments</div>'
                f'<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">Rumi · Reading assessments</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            annotations.append("**Rumi**: No data")

    # Others with no data
    for region in ["Balochistan", "RWP"]:
        d = data.get(region, {})
        if d.get("status") != "active":
            annotations.append(f"**{REGION_LABELS[region]}**: {_no_data_text(d.get('status', 'no_data'))}")

    if annotations:
        st.caption(" · ".join(annotations))


# =============================================================================
# SUMMARY TABLE
# =============================================================================

def _render_summary_table():
    st.markdown(section_title("Summary: All Metrics x All Regions"), unsafe_allow_html=True)

    obs = get_observation_metrics()
    lp = get_lp_engagement_metrics()
    training = get_training_metrics()
    retention = get_retention_metrics()
    fico = get_fico_metrics()
    learning = get_student_learning_metrics()

    rows = []

    # Row 1: Observations
    row = {"Metric": "Observations"}
    for region in REGION_ORDER:
        d = obs.get(region, {})
        if d.get("status") == "active" and d.get("actual") is not None:
            val = d["actual"]
            row[REGION_LABELS[region]] = f"{val:,}"
        else:
            row[REGION_LABELS[region]] = _no_data_text(d.get("status", "no_data"))
    rows.append(row)

    # Row 2: LP Engagement
    row = {"Metric": "LP Events"}
    for region in REGION_ORDER:
        d = lp.get(region, {})
        if d.get("status") == "active" and d.get("total_events", 0) > 0:
            row[REGION_LABELS[region]] = f"{d['total_events']:,}"
        else:
            row[REGION_LABELS[region]] = _no_data_text(d.get("status", "no_data"))
    rows.append(row)

    # Row 3: Training
    row = {"Metric": "Training Submissions"}
    for region in REGION_ORDER:
        d = training.get(region, {})
        if d.get("status") == "not_applicable":
            row[REGION_LABELS[region]] = "N/A"
        elif d.get("status") == "active" and (d.get("total_submissions") or 0) > 0:
            row[REGION_LABELS[region]] = f"{d['total_submissions']:,}"
        else:
            row[REGION_LABELS[region]] = _no_data_text(d.get("status", "no_data"))
    rows.append(row)

    # Row 4: Retention (30d)
    row = {"Metric": "30-day Retention"}
    for region in REGION_ORDER:
        d = retention.get(region, {})
        r30 = d.get("retention_30d", 0)
        if d.get("status") == "active" and r30 > 0:
            row[REGION_LABELS[region]] = f"{r30:.1f}%"
        else:
            row[REGION_LABELS[region]] = _no_data_text(d.get("status", "no_data"))
    rows.append(row)

    # Row 5: FICO (avg of B+C+D)
    row = {"Metric": "FICO Avg Score"}
    for region in REGION_ORDER:
        d = fico.get(region, {})
        if d.get("status") == "active":
            avg = (d.get("b_avg", 0) + d.get("c_avg", 0) + d.get("d_avg", 0)) / 3
            row[REGION_LABELS[region]] = f"{avg:.0f}%"
        elif d.get("status") == "not_applicable":
            row[REGION_LABELS[region]] = "N/A"
        else:
            row[REGION_LABELS[region]] = "—"
    rows.append(row)

    # Row 6: Student Learning
    row = {"Metric": "Student Learning"}
    for region in REGION_ORDER:
        d = learning.get(region, {})
        if d.get("status") != "active":
            row[REGION_LABELS[region]] = _no_data_text(d.get("status", "no_data"))
        elif d.get("type") == "RCT Effect Size":
            row[REGION_LABELS[region]] = f"ES {d.get('effect_size', 0)}"
        elif d.get("type") == "Assessment Scores":
            row[REGION_LABELS[region]] = f"{d.get('avg_score', 0):.0f}%"
        elif d.get("type") == "WCPM Reading Assessment":
            row[REGION_LABELS[region]] = f"{d.get('total_assessments', 0)} WCPM"
        else:
            row[REGION_LABELS[region]] = "—"
    rows.append(row)

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Metric": st.column_config.TextColumn("Metric", width="medium"),
        }
    )


if __name__ == "__main__":
    main()
