"""
Taleemabad Observability Dashboard
3-Section Layout: Program Details, Implementation Fidelity, Student Learning

Design Philosophy:
- Five-second rule: Most important insight visible immediately
- Cross-region comparison: Same metrics across all 5 regions
- Definitions included: User knows how each metric is calculated
- "No data available" shown clearly when data doesn't exist
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
from data.common_metrics import (
    get_observation_metrics,
    get_lp_engagement_metrics,
    get_training_metrics,
    get_fico_metrics,
    get_student_learning_metrics,
    METRIC_DEFINITIONS,
    REGION_PARAMETERS,
    REGIONS,
    REGION_COLORS,
)
from data.cache_layer import data_freshness_banner, clear_all_caches
from data import balochistan_queries, moawin_queries
from styles.design_system import (
    inject_css,
    section_title,
    insight_card,
    metric_card,
    grade_row,
    divider,
    COLORS,
    plotly_layout_defaults,
)

# === INJECT DESIGN SYSTEM ===
inject_css()

# Consistent region order and labels
REGION_ORDER = ["ICT", "Balochistan", "RWP", "Moawin", "Rumi"]
REGION_LABELS = {
    "ICT": "ICT (Islamabad)",
    "Balochistan": "Balochistan",
    "RWP": "Rawalpindi",
    "Moawin": "Moawin",
    "Rumi": "Rumi",
}
REGION_SHORT = {
    "ICT": "ICT",
    "Balochistan": "Balochistan",
    "RWP": "RWP",
    "Moawin": "Moawin",
    "Rumi": "Rumi",
}


def _no_data_html(region_label: str, reason: str = "No data available") -> str:
    """Return styled HTML for a region with no data."""
    return (
        f'<div style="background: #F9FAFB; border-radius: 8px; padding: 1rem; '
        f'text-align: center; border: 1px dashed #E5E7EB;">'
        f'<div style="font-size: 0.8125rem; font-weight: 600; color: #9CA3AF;">'
        f'{region_label}</div>'
        f'<div style="font-size: 0.75rem; color: #D1D5DB; margin-top: 0.25rem;">'
        f'{reason}</div>'
        f'</div>'
    )


def _metric_definition_expander(key: str):
    """Render a metric definition in a small expander."""
    defn = METRIC_DEFINITIONS.get(key, {})
    if defn:
        with st.expander("How is this calculated?", expanded=False):
            st.caption(defn.get("definition", ""))


def main():
    """Main dashboard entry point."""

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

    # =====================================================================
    # SECTION 1: PROGRAM DETAILS
    # =====================================================================
    _render_program_details()

    st.markdown(divider(), unsafe_allow_html=True)

    # =====================================================================
    # SECTION 2: IMPLEMENTATION FIDELITY
    # =====================================================================
    _render_implementation_fidelity()

    st.markdown(divider(), unsafe_allow_html=True)

    # =====================================================================
    # SECTION 3: STUDENT LEARNING
    # =====================================================================
    _render_student_learning()


# =============================================================================
# SECTION 1: PROGRAM DETAILS
# =============================================================================

def _render_program_details():
    st.markdown(section_title("1. Program Details"), unsafe_allow_html=True)

    # 5 region cards in a row
    cols = st.columns(5)
    for i, region in enumerate(REGION_ORDER):
        params = REGION_PARAMETERS.get(region, {})
        color = REGION_COLORS[region]
        with cols[i]:
            schools = params.get("schools", "—")
            teachers = params.get("teachers", "—")
            students = params.get("students", "—")
            coaches = params.get("coaches", "—")
            coaches_detail = params.get("coaches_detail", "")

            schools_str = f"{schools:,}" if isinstance(schools, int) else str(schools)
            teachers_str = f"{teachers:,}" if isinstance(teachers, int) else str(teachers)
            students_str = f"{students:,}" if isinstance(students, int) else str(students)

            # Calculate teacher:student ratio
            if isinstance(teachers, int) and isinstance(students, int) and teachers > 0:
                ratio = round(students / teachers)
                ratio_str = f"1:{ratio}"
            else:
                ratio_str = "—"

            # Coaches display
            if coaches == "AI-only":
                coaches_str = "AI-only"
            elif isinstance(coaches, int):
                coaches_str = str(coaches)
                if coaches_detail:
                    coaches_str += f" ({coaches_detail})"
            else:
                coaches_str = "—"

            st.markdown(
                f'<div style="border-left: 3px solid {color}; padding: 0.75rem; '
                f'background: white; border-radius: 6px; '
                f'box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
                f'<div style="font-size: 0.8125rem; font-weight: 600; color: {color}; '
                f'margin-bottom: 0.5rem;">{REGION_LABELS[region]}</div>'
                f'<div style="font-size: 0.6875rem; color: #374151; line-height: 1.8;">'
                f'<div><span style="color: #9CA3AF;">Schools</span> <strong>{schools_str}</strong></div>'
                f'<div><span style="color: #9CA3AF;">Teachers</span> <strong>{teachers_str}</strong></div>'
                f'<div><span style="color: #9CA3AF;">Students</span> <strong>{students_str}</strong></div>'
                f'<div><span style="color: #9CA3AF;">Ratio</span> <strong>{ratio_str}</strong></div>'
                f'<div><span style="color: #9CA3AF;">Coaches</span> <strong>{coaches_str}</strong></div>'
                f'</div></div>',
                unsafe_allow_html=True
            )

    # Cross-region comparison table
    st.markdown("")
    st.markdown(
        '<div style="font-size: 0.6875rem; font-weight: 600; color: #9CA3AF; '
        'text-transform: uppercase; letter-spacing: 0.05em; margin-top: 1rem;">'
        'Cross-Region Comparison</div>',
        unsafe_allow_html=True
    )

    # Build comparison table
    rows = []
    for region in REGION_ORDER:
        params = REGION_PARAMETERS.get(region, {})
        schools = params.get("schools", "—")
        teachers = params.get("teachers", "—")
        students = params.get("students", "—")
        coaches = params.get("coaches", "—")

        if isinstance(teachers, int) and isinstance(students, int) and teachers > 0:
            ratio = f"1:{round(students / teachers)}"
        else:
            ratio = "—"

        rows.append({
            "Region": REGION_SHORT[region],
            "Schools": f"{schools:,}" if isinstance(schools, int) else str(schools),
            "Teachers": f"{teachers:,}" if isinstance(teachers, int) else str(teachers),
            "Students": f"{students:,}" if isinstance(students, int) else str(students),
            "Ratio": ratio,
            "Coaches": str(coaches),
        })

    import pandas as pd
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


# =============================================================================
# SECTION 2: IMPLEMENTATION FIDELITY
# =============================================================================

def _render_implementation_fidelity():
    st.markdown(section_title("2. Implementation Fidelity"), unsafe_allow_html=True)

    # --- 2a. Observations ---
    _render_observations_subsection()
    st.markdown("")

    # --- 2b. Lesson Plan Engagement ---
    _render_lp_subsection()
    st.markdown("")

    # --- 2c. Teacher Training ---
    _render_training_subsection()
    st.markdown("")

    # --- 2d. FICO Scores ---
    _render_fico_subsection()


def _render_observations_subsection():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">2a. Observations (vs Benchmark)</div>',
        unsafe_allow_html=True
    )
    _metric_definition_expander("observations")

    data = get_observation_metrics()

    regions_active = []
    actuals = []
    benchmarks = []
    bar_colors = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")

        if status == "active" and d.get("actual") is not None and d["actual"] > 0:
            regions_active.append(REGION_SHORT[region])
            actuals.append(d["actual"])
            benchmarks.append(d.get("benchmark_monthly"))
            bar_colors.append(REGION_COLORS[region])
        elif status == "launching_q2_2026":
            annotations.append(f"**{REGION_SHORT[region]}**: Launching Q2 2026")
        elif status == "not_applicable":
            annotations.append(f"**{REGION_SHORT[region]}**: N/A")
        else:
            annotations.append(f"**{REGION_SHORT[region]}**: No data")

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

        bm_x = [r for r, b in zip(regions_active, benchmarks) if b is not None]
        bm_y = [b for b in benchmarks if b is not None]
        if bm_x:
            fig.add_trace(go.Scatter(
                x=bm_x, y=bm_y,
                mode="markers",
                marker=dict(symbol="line-ew-open", size=16, color="#9CA3AF", line_width=3),
                name="Monthly Benchmark",
            ))

        base_layout = plotly_layout_defaults(height=280)
        base_layout["showlegend"] = bool(bm_x)
        base_layout["legend"] = dict(
            orientation="h", yanchor="bottom", y=1.02,
            xanchor="right", x=1, font=dict(size=11)
        )
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if annotations:
        st.caption(" · ".join(annotations))


def _render_lp_subsection():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">2b. Lesson Plan Engagement</div>',
        unsafe_allow_html=True
    )
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
            regions_show.append(REGION_SHORT[region])
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
            annotations.append(f"**{REGION_SHORT[region]}**: No data")

    if values:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=regions_show, x=values,
            orientation="h",
            marker_color=bar_colors,
            text=[f"{v:,}" for v in values],
            textposition="outside",
            hovertext=hover_texts,
            hoverinfo="text",
        ))

        base_layout = plotly_layout_defaults(height=220)
        base_layout["margin"] = dict(t=10, b=40, l=100, r=80)
        base_layout["yaxis"] = dict(autorange="reversed")
        base_layout["showlegend"] = False
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if annotations:
        st.caption(" · ".join(annotations))


def _render_training_subsection():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">2c. Teacher Training Engagement</div>',
        unsafe_allow_html=True
    )
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
            annotations.append(f"**{REGION_SHORT[region]}**: N/A (coaching only)")
            continue

        total = d.get("total_submissions", 0) or 0
        if status == "active" and total > 0:
            regions_show.append(REGION_SHORT[region])
            values.append(total)
            bar_colors.append(REGION_COLORS[region])
            teachers = d.get("unique_teachers", 0)
            per_t = d.get("per_teacher", 0)
            hover_texts.append(
                f"Submissions: {total:,}<br>Teachers: {teachers:,}<br>Per teacher: {per_t}"
            )
        else:
            annotations.append(f"**{REGION_SHORT[region]}**: No data")

    if values:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=regions_show, x=values,
            orientation="h",
            marker_color=bar_colors,
            text=[f"{v:,}" for v in values],
            textposition="outside",
            hovertext=hover_texts,
            hoverinfo="text",
        ))

        base_layout = plotly_layout_defaults(height=220)
        base_layout["margin"] = dict(t=10, b=40, l=100, r=80)
        base_layout["yaxis"] = dict(autorange="reversed")
        base_layout["showlegend"] = False
        fig.update_layout(**base_layout)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    if annotations:
        st.caption(" · ".join(annotations))


def _render_fico_subsection():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">2d. FICO Scores by Section (B, C, D)</div>',
        unsafe_allow_html=True
    )
    _metric_definition_expander("fico")

    data = get_fico_metrics()

    regions_with_data = []
    annotations = []

    for region in REGION_ORDER:
        d = data.get(region, {})
        status = d.get("status", "no_data")
        if status == "active":
            regions_with_data.append(region)
        elif status == "not_applicable":
            annotations.append(f"**{REGION_SHORT[region]}**: N/A")
        elif status == "launching_q2_2026":
            annotations.append(f"**{REGION_SHORT[region]}**: Launching Q2 2026")
        else:
            annotations.append(f"**{REGION_SHORT[region]}**: No data")

    if regions_with_data:
        sections = ["Section B", "Section C", "Section D"]
        fig = go.Figure()
        for region in regions_with_data:
            d = data[region]
            fig.add_trace(go.Bar(
                x=sections,
                y=[d.get("b_avg", 0), d.get("c_avg", 0), d.get("d_avg", 0)],
                name=f"{REGION_SHORT[region]} ({d.get('type', '')})",
                marker_color=REGION_COLORS[region],
                text=[
                    f"{d.get('b_avg', 0):.0f}%",
                    f"{d.get('c_avg', 0):.0f}%",
                    f"{d.get('d_avg', 0):.0f}%",
                ],
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

        # Cross-region insight
        if "ICT" in regions_with_data and "Balochistan" in regions_with_data:
            ict_d = data["ICT"]
            bal_d = data["Balochistan"]
            st.markdown(
                insight_card(
                    f"ICT uses <strong>TEACH Tool (human observers)</strong> while Balochistan uses "
                    f"<strong>AI + Human</strong> scoring. "
                    f"Section D (Participation) is weakest across both: "
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
# SECTION 3: STUDENT LEARNING
# =============================================================================

def _render_student_learning():
    st.markdown(section_title("3. Student Learning"), unsafe_allow_html=True)
    _metric_definition_expander("student_learning")

    # --- 3a. ICT: Effect Size ---
    _render_ict_learning()
    st.markdown("")

    # --- 3b. Moawin: Subject Scores ---
    _render_moawin_learning()
    st.markdown("")

    # --- 3c. Rumi: Reading Assessments ---
    _render_rumi_learning()
    st.markdown("")

    # --- 3d. Balochistan: Student Participation ---
    _render_balochistan_learning()
    st.markdown("")

    # --- 3e. RWP: No data yet ---
    _render_rwp_learning()


def _render_ict_learning():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">3a. ICT — RCT Learning Impact</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            f'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04); '
            f'border-top: 3px solid {REGION_COLORS["ICT"]};">'
            f'<div style="font-size: 2.5rem; font-weight: 700; color: {REGION_COLORS["ICT"]};">0.46</div>'
            f'<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">'
            f'Effect Size (Cohen\'s d)</div>'
            f'<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
            f'RCT-validated · Medium-to-large</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
            '<div style="font-size: 2.5rem; font-weight: 700; color: #10B981;">$50-100</div>'
            '<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">'
            'Cost Per Teacher</div>'
            '<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
            '20-50x cheaper than coaching</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
            '<div style="font-size: 2.5rem; font-weight: 700; color: #374151;">10.2%</div>'
            '<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">'
            'Improvement in Observation Scores</div>'
            '<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
            'Certified vs non-certified teachers</div>'
            '</div>',
            unsafe_allow_html=True
        )


def _render_moawin_learning():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">3b. Moawin — Student Assessment Scores</div>',
        unsafe_allow_html=True
    )

    scores = moawin_queries.get_student_scores_by_subject()
    if not scores:
        st.markdown(_no_data_html("Moawin", "No student assessment data available"), unsafe_allow_html=True)
        return

    # Subject score cards
    cols = st.columns(len(scores))
    for i, s in enumerate(scores):
        with cols[i]:
            pass_color = "#10B981" if s["pass_rate"] >= 70 else "#F59E0B" if s["pass_rate"] >= 50 else "#EF4444"
            st.markdown(
                f'<div style="background: white; border-radius: 8px; padding: 1rem; '
                f'text-align: center; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">'
                f'<div style="font-size: 1.5rem; font-weight: 700; color: {REGION_COLORS["Moawin"]};">'
                f'{s["avg_score"]:.0f}%</div>'
                f'<div style="font-size: 0.75rem; font-weight: 600; color: #374151; margin-top: 0.25rem;">'
                f'{s["subject"]}</div>'
                f'<div style="font-size: 0.6875rem; color: {pass_color}; margin-top: 0.25rem;">'
                f'{s["pass_rate"]:.0f}% pass rate</div>'
                f'<div style="font-size: 0.625rem; color: #D1D5DB; margin-top: 0.25rem;">'
                f'{s["count"]:,} assessments</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    # Bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[s["subject"] for s in scores],
        y=[s["avg_score"] for s in scores],
        marker_color=REGION_COLORS["Moawin"],
        text=[f'{s["avg_score"]:.0f}%' for s in scores],
        textposition="outside",
    ))
    base_layout = plotly_layout_defaults(height=250)
    base_layout["yaxis"] = dict(range=[0, 100], ticksuffix="%")
    base_layout["showlegend"] = False
    fig.update_layout(**base_layout)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def _render_rumi_learning():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">3c. Rumi — WCPM Reading Assessments</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            f'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04); '
            f'border-top: 3px solid {REGION_COLORS["Rumi"]};">'
            f'<div style="font-size: 2.5rem; font-weight: 700; color: {REGION_COLORS["Rumi"]};">197</div>'
            f'<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">'
            f'WCPM Assessments</div>'
            f'<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
            f'Words Correct Per Minute</div>'
            f'</div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
            '<div style="font-size: 2.5rem; font-weight: 700; color: #F59E0B;">34%</div>'
            '<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">'
            'At Grade Level</div>'
            '<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
            'Reading at expected fluency</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            'text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
            '<div style="font-size: 2.5rem; font-weight: 700; color: #374151;">52</div>'
            '<div style="font-size: 0.75rem; color: #6B7280; margin-top: 0.25rem;">'
            'Avg WCPM</div>'
            '<div style="font-size: 0.6875rem; color: #9CA3AF; margin-top: 0.5rem;">'
            'Average words correct per minute</div>'
            '</div>',
            unsafe_allow_html=True
        )


def _render_balochistan_learning():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">3d. Balochistan — Student Participation (from Observations)</div>',
        unsafe_allow_html=True
    )

    known = balochistan_queries.BALOCHISTAN_KNOWN_VALUES

    # Talk time and question type cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
            '<div style="font-size: 0.6875rem; font-weight: 600; color: #9CA3AF; '
            'text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">'
            'Talk Time Distribution</div>'
            f'<div style="display: flex; justify-content: space-between; align-items: baseline;">'
            f'<div style="text-align: center; flex: 1;">'
            f'<div style="font-size: 2rem; font-weight: 700; color: #EF4444;">{known["teacher_talk_time"]}%</div>'
            f'<div style="font-size: 0.6875rem; color: #6B7280;">Teacher</div></div>'
            f'<div style="text-align: center; flex: 1;">'
            f'<div style="font-size: 2rem; font-weight: 700; color: #F59E0B;">{known["student_talk_time"]}%</div>'
            f'<div style="font-size: 0.6875rem; color: #6B7280;">Student</div></div>'
            f'<div style="text-align: center; flex: 1;">'
            f'<div style="font-size: 2rem; font-weight: 700; color: #9CA3AF;">{known["other_talk_time"]}%</div>'
            f'<div style="font-size: 0.6875rem; color: #6B7280;">Other</div></div>'
            f'</div>'
            f'<div style="font-size: 0.625rem; color: #D1D5DB; margin-top: 0.75rem; text-align: center;">'
            f'Target: 40% student talk time</div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        total_q = known["avg_open_questions"] + known["avg_closed_questions"]
        closed_pct = round(known["avg_closed_questions"] / total_q * 100) if total_q > 0 else 87
        open_pct = 100 - closed_pct
        st.markdown(
            '<div style="background: white; border-radius: 10px; padding: 1.25rem; '
            'box-shadow: 0 1px 3px rgba(0,0,0,0.04);">'
            '<div style="font-size: 0.6875rem; font-weight: 600; color: #9CA3AF; '
            'text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">'
            'Question Types</div>'
            f'<div style="display: flex; justify-content: space-between; align-items: baseline;">'
            f'<div style="text-align: center; flex: 1;">'
            f'<div style="font-size: 2rem; font-weight: 700; color: #EF4444;">{closed_pct}%</div>'
            f'<div style="font-size: 0.6875rem; color: #6B7280;">Closed-ended</div></div>'
            f'<div style="text-align: center; flex: 1;">'
            f'<div style="font-size: 2rem; font-weight: 700; color: #10B981;">{open_pct}%</div>'
            f'<div style="font-size: 0.6875rem; color: #6B7280;">Open-ended</div></div>'
            f'</div>'
            f'<div style="font-size: 0.625rem; color: #D1D5DB; margin-top: 0.75rem; text-align: center;">'
            f'Avg {known["avg_open_questions"]} open vs {known["avg_closed_questions"]} closed per class</div>'
            '</div>',
            unsafe_allow_html=True
        )

    # FICO Section D indicators chart
    st.markdown(
        '<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; '
        'margin-top: 1rem; margin-bottom: 0.5rem;">'
        'FICO Section D — Student Participation Indicators</div>',
        unsafe_allow_html=True
    )

    fico_d = known.get("fico_d", {})
    d_labels = {
        "D1": "Students ask questions",
        "D2": "Students show interest",
        "D3": "Students lead activities",
        "D4": "Students collaborate",
        "D5": "Students present work",
        "D6": "Students evaluate peers",
    }

    for indicator, score in fico_d.items():
        label = d_labels.get(indicator, indicator)
        color = "#10B981" if score >= 50 else "#F59E0B" if score >= 25 else "#EF4444"
        st.markdown(grade_row(f"{indicator}: {label}", score, color), unsafe_allow_html=True)

    st.markdown(
        insight_card(
            f"Student participation is critically low across all D indicators. "
            f"D6 (peer evaluation) scores <strong>0%</strong>, D3 (student-led activities) "
            f"only <strong>6%</strong>. Combined with only <strong>{known['student_talk_time']}% "
            f"student talk time</strong>, classrooms remain heavily teacher-centered.",
            title="Balochistan Participation Gap",
            border_color=REGION_COLORS["Balochistan"]
        ),
        unsafe_allow_html=True
    )


def _render_rwp_learning():
    st.markdown(
        '<div style="font-size: 0.875rem; font-weight: 600; color: #374151; '
        'margin-bottom: 0.5rem;">3e. Rawalpindi — Student Learning</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        _no_data_html("Rawalpindi", "No data yet — launching Q2 2026"),
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
