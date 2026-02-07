"""
Sidebar component with filters (region selection moved to main page tabs).
Apple-aesthetic design - clean, no emoji clutter.
"""
import streamlit as st


def render_sidebar() -> dict:
    """
    Render the sidebar with filters.
    Note: Region selection is now handled by tabs on the main page.

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

        # Filters section
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Filters</div>', unsafe_allow_html=True)

        # Time period filter
        time_period = st.selectbox(
            "Time Period",
            options=["Last 7 Days", "Last 30 Days", "Last 90 Days", "This Year", "All Time"],
            index=4,  # Default to All Time
            help="Filter by date range"
        )

        # Subject filter
        subject = st.selectbox(
            "Subject",
            options=["All Subjects", "Mathematics", "English", "Science", "Urdu", "Social Studies", "Islamiat"],
            index=0,
            help="Filter by subject taught"
        )

        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)

        # Observation type filter
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Observation Type</div>', unsafe_allow_html=True)
        obs_type = st.radio(
            "Select observation source",
            options=["All Observations", "AI Only (Rumi)", "Human Only (Coaches)"],
            index=0,
            label_visibility="collapsed"
        )

        st.divider()

        # Data status with breathing dots (uses CSS from design_system.py)
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">Data Sources</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="font-family: 'Inter', -apple-system, sans-serif; font-size: 0.75rem;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">BigQuery (ICT)</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">Balochistan (Neon)</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">SchoolPilot (Moawin)</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #6B7280;">Rumi (Supabase)</span>
                <span style="color: #10B981;"><span class="status-dot-pulse"></span> Live</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Return filter values (region is now handled by tabs)
    return {
        "region": "Combined",  # Default for backwards compatibility
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
