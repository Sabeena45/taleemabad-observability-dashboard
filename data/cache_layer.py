"""
Caching layer for the observability dashboard.
Tracks data freshness and provides cache clearing utilities.
All query functions use @st.cache_data(ttl=28800) for 8-hour TTL.
"""
import streamlit as st
from datetime import datetime
from typing import Optional


# Cache TTL: 8 hours (28800 seconds)
CACHE_TTL = 28800


def get_last_refresh_time() -> str:
    """Get formatted timestamp of last data refresh."""
    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = datetime.now()
    return st.session_state["last_refresh"].strftime("%d %b %Y, %I:%M %p")


def clear_all_caches():
    """Clear all cached data to force refresh."""
    st.cache_data.clear()
    st.session_state["last_refresh"] = datetime.now()


def data_freshness_banner() -> str:
    """Generate HTML for the data freshness banner."""
    refresh_time = get_last_refresh_time()
    return (
        '<div style="background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; '
        'padding: 0.5rem 1rem; margin-bottom: 1rem; display: flex; align-items: center; '
        'justify-content: space-between;">'
        '<div style="display: flex; align-items: center; gap: 0.5rem;">'
        '<span style="color: #16A34A; font-size: 0.625rem;">&#9679;</span>'
        f'<span style="font-size: 0.75rem; color: #166534;">Data refreshed: {refresh_time}</span>'
        '</div>'
        '<span style="font-size: 0.6875rem; color: #6B7280;">5 databases connected</span>'
        '</div>'
    )
