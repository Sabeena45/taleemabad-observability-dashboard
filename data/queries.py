"""
SQL queries and data fetching functions for the observability dashboard.
"""
import os
import json
from typing import Dict, Any, Optional
from functools import lru_cache

# Database connection imports (will be configured later)
try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False


# ============================================================================
# DATABASE CONNECTION CONFIGS
# ============================================================================

RUMI_CONFIG = {
    "host": "aws-1-ap-southeast-1.pooler.supabase.com",
    "port": 6543,
    "database": "postgres",
    "user": "analyst.jlpenspfdcwxkopaidys",
    "password": "RumiAnalytics2026!"
}

DIGITAL_COACH_CONFIG = {
    "host": "ep-lucky-flower-a17i7db2g-z-2.us-west-2.aws.neon.tech",
    "port": 5432,
    "database": "neondb",
    "user": "analyst_readonly",
    "password": "readonly_analyst_2026"
}


# ============================================================================
# SUMMARY METRICS
# ============================================================================

def get_summary_metrics(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get summary metrics for the dashboard cards.

    Args:
        filters: Selected filter values (region, subject, time_period, etc.)

    Returns:
        Dictionary of metric values
    """
    # TODO: Replace with live queries
    # For now, return sample data based on region

    region = filters.get("region", "Combined")

    if region == "Combined":
        return {
            "schools": 236,
            "teachers": 599,
            "ai_sessions": 128,
            "human_observations": 576,
            "avg_score": 72.3,
            "students": 16898
        }
    elif region == "Rawalpindi":
        return {
            "schools": 89,
            "teachers": 210,
            "ai_sessions": 45,
            "human_observations": 0,
            "avg_score": 71.8,
            "students": 6200
        }
    elif region == "Islamabad":
        return {
            "schools": 52,
            "teachers": 145,
            "ai_sessions": 38,
            "human_observations": 0,
            "avg_score": 74.2,
            "students": 4100
        }
    elif region == "Balochistan":
        return {
            "schools": 95,
            "teachers": 244,
            "ai_sessions": 45,
            "human_observations": 576,
            "avg_score": 68.5,
            "students": 6598
        }

    return {}


# ============================================================================
# FICO SECTION QUERIES
# ============================================================================

def get_fico_section_c_metrics(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get Section C (Checking for Understanding) metrics.

    Returns:
        Dict with open_questions, closed_questions, question_ratio
    """
    if not PSYCOPG2_AVAILABLE:
        return _sample_section_c_data()

    try:
        conn = psycopg2.connect(**RUMI_CONFIG)
        cur = conn.cursor()

        # Query question metrics from Rumi
        cur.execute("""
            SELECT
                AVG((analysis_data->'questions'->>'open_ended_count')::int) as avg_open,
                AVG((analysis_data->'questions'->>'closed_ended_count')::int) as avg_closed
            FROM coaching_sessions
            WHERE analysis_data IS NOT NULL
              AND status = 'completed'
        """)

        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            avg_open = row[0] or 0
            avg_closed = row[1] or 0
            total = avg_open + avg_closed
            ratio = (avg_open / total * 100) if total > 0 else 0

            return {
                "avg_open_questions": round(avg_open, 1),
                "avg_closed_questions": round(avg_closed, 1),
                "open_question_ratio": round(ratio, 1)
            }

    except Exception as e:
        print(f"Error fetching Section C metrics: {e}")

    return _sample_section_c_data()


def _sample_section_c_data() -> Dict[str, Any]:
    """Return sample Section C data."""
    return {
        "avg_open_questions": 7.6,
        "avg_closed_questions": 28.5,
        "open_question_ratio": 21.1
    }


def get_fico_section_d_metrics(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get Section D (Student Participation) metrics.

    Returns:
        Dict with student_talk_time, teacher_talk_time
    """
    # TODO: Extract talk time from analysis_data
    # Current Rumi data structure needs investigation

    return {
        "student_talk_time": 21.2,
        "teacher_talk_time": 78.8,
        "target_student_time": 40.0
    }


# ============================================================================
# OBSERVATION QUERIES
# ============================================================================

def get_observation_counts(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get AI vs Human observation counts.

    Returns:
        Dict with ai_count, human_count, total
    """
    region = filters.get("region", "Combined")

    # Sample data by region
    if region == "Combined":
        return {"ai_count": 128, "human_count": 576, "total": 704}
    elif region == "Balochistan":
        return {"ai_count": 522, "human_count": 54, "total": 576}
    else:
        return {"ai_count": 45, "human_count": 0, "total": 45}


def get_observation_trend(filters: Dict[str, Any], weeks: int = 8) -> list:
    """
    Get weekly observation counts for trend chart.

    Args:
        filters: Selected filters
        weeks: Number of weeks to include

    Returns:
        List of {week, ai_count, human_count} dicts
    """
    # TODO: Implement with real queries
    # Sample trend data
    return [
        {"week": "Week 1", "ai": 12, "human": 45},
        {"week": "Week 2", "ai": 15, "human": 52},
        {"week": "Week 3", "ai": 18, "human": 48},
        {"week": "Week 4", "ai": 14, "human": 61},
        {"week": "Week 5", "ai": 22, "human": 55},
        {"week": "Week 6", "ai": 19, "human": 68},
        {"week": "Week 7", "ai": 16, "human": 72},
        {"week": "Week 8", "ai": 12, "human": 75},
    ]


# ============================================================================
# SCHOOL & TEACHER QUERIES
# ============================================================================

def get_school_count(filters: Dict[str, Any]) -> int:
    """Get count of schools based on filters."""
    # TODO: Query SchoolPilot via MCP
    return 236


def get_teacher_count(filters: Dict[str, Any]) -> int:
    """Get count of teachers based on filters."""
    # TODO: Query SchoolPilot via MCP
    return 599


def get_student_count(filters: Dict[str, Any]) -> int:
    """Get count of students based on filters."""
    # TODO: Query SchoolPilot via MCP
    return 16898


# ============================================================================
# COACHING SESSION QUERIES
# ============================================================================

def get_recent_sessions(filters: Dict[str, Any], limit: int = 10) -> list:
    """
    Get recent coaching sessions.

    Args:
        filters: Selected filters
        limit: Number of sessions to return

    Returns:
        List of session dicts with key metrics
    """
    if not PSYCOPG2_AVAILABLE:
        return _sample_sessions()

    try:
        conn = psycopg2.connect(**RUMI_CONFIG)
        cur = conn.cursor()

        cur.execute(f"""
            SELECT
                id,
                created_at,
                analysis_data->>'subject' as subject,
                analysis_data->'scores'->>'percentage' as score,
                (analysis_data->'questions'->>'open_ended_count')::int as open_q,
                (analysis_data->'questions'->>'closed_ended_count')::int as closed_q
            FROM coaching_sessions
            WHERE analysis_data IS NOT NULL
              AND status = 'completed'
            ORDER BY created_at DESC
            LIMIT {limit}
        """)

        sessions = []
        for row in cur.fetchall():
            sessions.append({
                "id": row[0],
                "date": row[1].strftime("%Y-%m-%d") if row[1] else None,
                "subject": row[2] or "Unknown",
                "score": float(row[3]) if row[3] else None,
                "open_questions": row[4] or 0,
                "closed_questions": row[5] or 0
            })

        cur.close()
        conn.close()
        return sessions

    except Exception as e:
        print(f"Error fetching sessions: {e}")
        return _sample_sessions()


def _sample_sessions() -> list:
    """Return sample session data."""
    return [
        {"id": "1", "date": "2026-01-20", "subject": "Mathematics", "score": 72.5, "open_questions": 8, "closed_questions": 25},
        {"id": "2", "date": "2026-01-19", "subject": "English", "score": 68.3, "open_questions": 5, "closed_questions": 32},
        {"id": "3", "date": "2026-01-18", "subject": "Science", "score": 75.1, "open_questions": 12, "closed_questions": 18},
    ]


# ============================================================================
# STUDENT SCORES QUERIES
# ============================================================================

def get_student_scores_by_subject(filters: Dict[str, Any]) -> list:
    """
    Get average student scores by subject.

    Returns:
        List of {subject, avg_score, pass_rate, count} dicts
    """
    # TODO: Query SchoolPilot student_scores via MCP
    return [
        {"subject": "English", "avg_score": 68.5, "pass_rate": 72.3, "count": 2450},
        {"subject": "Math", "avg_score": 65.2, "pass_rate": 68.1, "count": 2380},
        {"subject": "Urdu", "avg_score": 71.8, "pass_rate": 78.5, "count": 2410},
        {"subject": "Science", "avg_score": 62.4, "pass_rate": 64.2, "count": 1820},
    ]


# ============================================================================
# ATTENDANCE QUERIES
# ============================================================================

def get_attendance_trend(filters: Dict[str, Any], days: int = 30) -> list:
    """
    Get daily attendance rates.

    Returns:
        List of {date, rate} dicts
    """
    # TODO: Query SchoolPilot attendance via MCP
    return [
        {"date": "2026-01-15", "rate": 87.5},
        {"date": "2026-01-16", "rate": 89.2},
        {"date": "2026-01-17", "rate": 85.8},
        {"date": "2026-01-20", "rate": 91.3},
        {"date": "2026-01-21", "rate": 88.7},
    ]
