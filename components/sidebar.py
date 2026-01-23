"""
Sidebar component with region selector and filters.
"""
import streamlit as st


def render_sidebar() -> dict:
    """
    Render the sidebar with region selector and filters.

    Returns:
        dict: Selected filter values
    """
    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="margin: 0;">📊 Taleemabad</h2>
            <p style="color: #6B7280; font-size: 0.875rem;">Observability Dashboard</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Region Selector
        st.markdown("### 🌍 Region")
        region = st.radio(
            "Select region to view",
            options=["Combined", "Balochistan", "Islamabad", "Moawin", "Rawalpindi (Coming Soon)"],
            index=0,
            label_visibility="collapsed",
            help="Filter all data by geographic region"
        )

        # Show region description
        region_descriptions = {
            "Combined": "All regions combined",
            "Balochistan": "Winter School FLN program (522 AI + 54 human observations)",
            "Islamabad": "ICT - Federal area schools (BigQuery)",
            "Moawin": "SchoolPilot platform (236 schools, 602 teachers)",
            "Rawalpindi (Coming Soon)": "⚠️ Database access pending"
        }
        st.caption(region_descriptions[region])

        st.divider()

        # Pre-built Filters
        st.markdown("### 📊 Filters")

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
            index=1,  # Default: Last 30 Days
            help="Filter by date range"
        )

        # Observation type filter
        st.markdown("### 🔍 Observation Type")
        obs_type = st.radio(
            "Select observation source",
            options=["All Observations", "AI Only (Rumi)", "Human Only (Coaches)"],
            index=0,
            label_visibility="collapsed"
        )

        st.divider()

        # Data freshness indicator
        st.markdown("### 📡 Data Status")
        st.markdown("""
        <div style="font-family: 'Fira Code', monospace; font-size: 0.75rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span>SchoolPilot</span>
                <span style="color: #10B981;">● Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span>Rumi</span>
                <span style="color: #10B981;">● Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span>Digital Coach</span>
                <span style="color: #F59E0B;">● Daily</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Quick links
        st.markdown("### 🔗 Quick Links")
        st.page_link("pages/1_fico_analysis.py", label="📋 FICO Deep Dive", icon="📋")
        st.page_link("pages/2_observations.py", label="👁️ Observations", icon="👁️")
        st.page_link("pages/3_students.py", label="👨‍🎓 Student Outcomes", icon="👨‍🎓")

    # Normalize region name (remove "(Coming Soon)" suffix)
    normalized_region = region.replace(" (Coming Soon)", "") if "(Coming Soon)" in region else region

    # Return filter values
    return {
        "region": normalized_region,
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
            "schoolpilot": "1=0",  # Coming soon - no access yet
            "rumi": "1=0",
            "digital_coach": "1=0"
        },
        "Islamabad": {
            "schoolpilot": "1=0",  # Islamabad uses BigQuery
            "rumi": "1=1",
            "digital_coach": "1=0",
            "bigquery": "1=1"  # All BigQuery data is Islamabad
        },
        "Balochistan": {
            "schoolpilot": "1=0",  # No Balochistan in SchoolPilot
            "rumi": "1=0",
            "digital_coach": "1=1",  # All Digital Coach data is Balochistan
            "balochistan_rds": "1=1"  # NIETE Balochistan database
        },
        "Moawin": {
            "schoolpilot": "1=1",  # All SchoolPilot data is Moawin
            "rumi": "1=0",
            "digital_coach": "1=0"
        }
    }

    return filters.get(region, {}).get(database, "1=1")
