"""
Sidebar component with region selector and filters.
Apple-aesthetic design - clean, no emoji clutter.
"""
import streamlit as st


def render_sidebar() -> dict:
    """
    Render the sidebar with region selector and filters.

    Returns:
        dict: Selected filter values
    """
    with st.sidebar:
        # Clean header
        st.markdown("""
        <div style="padding: 1rem 0 1.5rem 0; border-bottom: 1px solid #E5E7EB;">
            <div style="font-size: 0.625rem; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.15em;">TALEEMABAD</div>
            <div style="font-size: 1.25rem; font-weight: 600; color: #1A1A1A; margin-top: 0.25rem;">Observability</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

        # Region Selector
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Region</div>', unsafe_allow_html=True)
        region = st.radio(
            "Select region to view",
            options=["Combined", "Balochistan", "Islamabad", "Moawin", "Rawalpindi"],
            index=0,
            label_visibility="collapsed",
            help="Filter all data by geographic region"
        )

        # Show region description
        region_descriptions = {
            "Combined": "All regions combined",
            "Balochistan": "Winter School FLN program",
            "Islamabad": "ICT Federal area schools",
            "Moawin": "SchoolPilot platform",
            "Rawalpindi": "Prevail longitudinal study"
        }
        st.caption(region_descriptions[region])

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        st.divider()

        # Filters
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Filters</div>', unsafe_allow_html=True)

        # Subject filter
        subject = st.selectbox(
            "Subject",
            options=["All Subjects", "Mathematics", "English", "Science", "Urdu", "Social Studies", "Islamiat"],
            index=0,
            help="Filter by subject taught"
        )

        # Time period filter
        time_period = st.selectbox(
            "Time Period",
            options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year", "All Time"],
            index=1,
            help="Filter by date range"
        )

        # Observation type filter
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Observation Type</div>', unsafe_allow_html=True)
        obs_type = st.radio(
            "Select observation source",
            options=["All Observations", "AI Only (Rumi)", "Human Only (Coaches)"],
            index=0,
            label_visibility="collapsed"
        )

        st.divider()

        # Data status with breathing dots (uses CSS from design_system.py)
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Data Status</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="font-family: 'Inter', -apple-system, sans-serif; font-size: 0.75rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">BigQuery</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">Rumi</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">SchoolPilot</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">Balochistan</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Return filter values
    return {
        "region": region,
        "subject": subject if subject != "All Subjects" else None,
        "time_period": time_period,
        "observation_type": obs_type
    }


def get_time_filter_sql(time_period: str) -> str:
    """Convert time period selection to SQL WHERE clause."""
    mapping = {
        "Last 7 Days": "created_at > NOW() - INTERVAL '7 days'",
        "Last 30 Days": "created_at > NOW() - INTERVAL '30 days'",
        "Last 90 Days": "created_at > NOW() - INTERVAL '90 days'",
        "This Year": "EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())",
        "All Time": "1=1"  # No filter
    }
    return mapping.get(time_period, "1=1")


def get_region_filter(region: str, database: str) -> str:
    """
    Get SQL filter clause for region based on database.

    Args:
        region: Selected region name
        database: Database to query (schoolpilot, rumi, digital_coach)

    Returns:
        SQL WHERE clause fragment
    """
    if region == "Combined":
        return "1=1"  # No filter

    filters = {
        "Rawalpindi": {
            "schoolpilot": "1=0",
            "rumi": "1=0",
            "digital_coach": "1=0",
            "bigquery": "1=1"
        },
        "Islamabad": {
            "schoolpilot": "1=0",
            "rumi": "1=1",
            "digital_coach": "1=0",
            "bigquery": "1=1"
        },
        "Balochistan": {
            "schoolpilot": "1=0",
            "rumi": "1=0",
            "digital_coach": "1=1",
            "balochistan_rds": "1=1"
        },
        "Moawin": {
            "schoolpilot": "1=1",
            "rumi": "1=0",
            "digital_coach": "1=0"
        }
    }

    return filters.get(region, {}).get(database, "1=1")
