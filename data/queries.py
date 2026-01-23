"""
Main query router for the observability dashboard.
Routes queries to appropriate regional modules based on selected filters.
"""
from typing import Dict, Any, List

# Import regional query modules
from . import balochistan_queries
from . import moawin_queries
from . import islamabad_queries


# ============================================================================
# SUMMARY METRICS ROUTER
# ============================================================================

def get_summary_metrics(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get summary metrics based on selected region.

    Args:
        filters: Selected filter values (region, time_period, observation_type)

    Returns:
        Dictionary of metric values
    """
    region = filters.get("region", "Combined")
    time_period = filters.get("time_period", "All Time")
    obs_type = filters.get("observation_type", "All Observations")

    if region == "Balochistan":
        return balochistan_queries.get_summary_metrics(obs_type)

    elif region == "Moawin":
        return moawin_queries.get_summary_metrics(time_period)

    elif region == "Islamabad":
        return islamabad_queries.get_summary_metrics(time_period)

    elif region == "Rawalpindi" or "Coming Soon" in str(region):
        # Rawalpindi not yet available
        return {
            "schools": 0,
            "teachers": 0,
            "ai_sessions": 0,
            "human_observations": 0,
            "avg_score": 0,
            "students": 0,
            "note": "Rawalpindi data coming soon"
        }

    elif region == "Combined":
        # Combine all available regions
        bal = balochistan_queries.get_summary_metrics(obs_type)
        mow = moawin_queries.get_summary_metrics(time_period)
        isl = islamabad_queries.get_summary_metrics(time_period)

        return {
            "schools": bal["schools"] + mow["schools"] + isl["schools"],
            "teachers": bal["teachers"] + mow["teachers"] + isl["teachers"],
            "ai_sessions": bal["ai_sessions"],  # Only Balochistan has AI
            "human_observations": bal["human_observations"] + isl["human_observations"],
            "avg_score": round((bal["avg_score"] + mow["avg_score"] + isl["avg_score"]) / 3, 1),
            "students": bal["students"] + mow["students"] + isl["students"]
        }

    return {}


# ============================================================================
# FICO SECTION QUERIES ROUTER
# ============================================================================

def get_fico_section_c_metrics(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get Section C (Checking for Understanding / Question) metrics.

    Returns:
        Dict with avg_open_questions, avg_closed_questions, open_question_ratio
    """
    region = filters.get("region", "Combined")
    obs_type = filters.get("observation_type", "All Observations")

    if region == "Balochistan":
        return balochistan_queries.get_question_metrics(obs_type)

    elif region == "Moawin":
        return moawin_queries.get_question_metrics(obs_type)

    elif region == "Islamabad":
        return islamabad_queries.get_question_metrics(obs_type)

    elif region == "Combined":
        # Only Balochistan has question data
        return balochistan_queries.get_question_metrics(obs_type)

    # Default fallback
    return {
        "avg_open_questions": None,
        "avg_closed_questions": None,
        "open_question_ratio": None,
        "note": "Question data not available for this region"
    }


def get_fico_section_d_metrics(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get Section D (Student Participation / Talk Time) metrics.

    Returns:
        Dict with student_talk_time, teacher_talk_time, target_student_time
    """
    region = filters.get("region", "Combined")
    obs_type = filters.get("observation_type", "All Observations")

    if region == "Balochistan":
        return balochistan_queries.get_talk_time_metrics(obs_type)

    elif region == "Moawin":
        return moawin_queries.get_talk_time_metrics(obs_type)

    elif region == "Islamabad":
        return islamabad_queries.get_talk_time_metrics(obs_type)

    elif region == "Combined":
        # Only Balochistan has talk time data
        return balochistan_queries.get_talk_time_metrics(obs_type)

    # Default fallback
    return {
        "student_talk_time": None,
        "teacher_talk_time": None,
        "target_student_time": 40.0,
        "note": "Talk time data not available for this region"
    }


def get_fico_scores(filters: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Get all FICO section scores (B, C, D).

    Returns:
        Dict with section_b, section_c, section_d dictionaries
    """
    region = filters.get("region", "Combined")

    if region == "Balochistan":
        return balochistan_queries.get_fico_scores()

    elif region == "Islamabad":
        return islamabad_queries.get_fico_scores()

    elif region == "Combined":
        # Prefer Balochistan as it has more detailed FICO data
        return balochistan_queries.get_fico_scores()

    # Default fallback
    return {
        "section_b": {},
        "section_c": {},
        "section_d": {}
    }


# ============================================================================
# OBSERVATION QUERIES ROUTER
# ============================================================================

def get_observation_counts(filters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get AI vs Human observation counts.

    Returns:
        Dict with ai_count, human_count, total
    """
    region = filters.get("region", "Combined")
    obs_type = filters.get("observation_type", "All Observations")

    if region == "Balochistan":
        return balochistan_queries.get_observation_counts(obs_type)

    elif region == "Moawin":
        return moawin_queries.get_observation_counts(obs_type)

    elif region == "Islamabad":
        return islamabad_queries.get_observation_counts(obs_type)

    elif region == "Combined":
        bal = balochistan_queries.get_observation_counts(obs_type)
        isl = islamabad_queries.get_observation_counts(obs_type)

        return {
            "ai_count": bal["ai_count"] + isl.get("ai_count", 0),
            "human_count": bal["human_count"] + isl.get("human_count", 0),
            "total": bal["total"] + isl.get("total", 0)
        }

    return {"ai_count": 0, "human_count": 0, "total": 0}


def get_observation_trend(filters: Dict[str, Any], weeks: int = 8) -> List[Dict[str, Any]]:
    """
    Get weekly observation counts for trend chart.

    Args:
        filters: Selected filters
        weeks: Number of weeks to include

    Returns:
        List of {week, ai, human} dicts
    """
    region = filters.get("region", "Combined")

    if region == "Balochistan":
        return balochistan_queries.get_observation_trend(weeks)

    elif region == "Islamabad":
        return islamabad_queries.get_observation_trend(weeks)

    elif region == "Combined":
        # Use Balochistan as primary since it has both AI and human
        return balochistan_queries.get_observation_trend(weeks)

    # Default fallback
    return []


# ============================================================================
# SCHOOL & TEACHER QUERIES ROUTER
# ============================================================================

def get_school_count(filters: Dict[str, Any]) -> int:
    """Get count of schools based on filters."""
    region = filters.get("region", "Combined")

    if region == "Moawin":
        return moawin_queries.get_school_count()

    elif region == "Balochistan":
        metrics = balochistan_queries.get_summary_metrics()
        return metrics.get("schools", 0)

    elif region == "Islamabad":
        metrics = islamabad_queries.get_summary_metrics()
        return metrics.get("schools", 0)

    elif region == "Combined":
        return (
            moawin_queries.get_school_count() +
            balochistan_queries.get_summary_metrics().get("schools", 0) +
            islamabad_queries.get_summary_metrics().get("schools", 0)
        )

    return 0


def get_teacher_count(filters: Dict[str, Any]) -> int:
    """Get count of teachers based on filters."""
    region = filters.get("region", "Combined")

    if region == "Moawin":
        return moawin_queries.get_teacher_count()

    elif region == "Balochistan":
        metrics = balochistan_queries.get_summary_metrics()
        return metrics.get("teachers", 0)

    elif region == "Islamabad":
        return islamabad_queries.get_teacher_count()

    elif region == "Combined":
        return (
            moawin_queries.get_teacher_count() +
            balochistan_queries.get_summary_metrics().get("teachers", 0) +
            islamabad_queries.get_teacher_count()
        )

    return 0


def get_student_count(filters: Dict[str, Any]) -> int:
    """Get count of students based on filters."""
    region = filters.get("region", "Combined")

    if region == "Moawin":
        return moawin_queries.get_student_count()

    elif region == "Balochistan":
        metrics = balochistan_queries.get_summary_metrics()
        return metrics.get("students", 0)

    elif region == "Islamabad":
        metrics = islamabad_queries.get_summary_metrics()
        return metrics.get("students", 0)

    elif region == "Combined":
        return (
            moawin_queries.get_student_count() +
            balochistan_queries.get_summary_metrics().get("students", 0) +
            islamabad_queries.get_summary_metrics().get("students", 0)
        )

    return 0


# ============================================================================
# COACHING SESSION QUERIES
# ============================================================================

def get_recent_sessions(filters: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent coaching/observation sessions.

    Args:
        filters: Selected filters
        limit: Number of sessions to return

    Returns:
        List of session dicts with key metrics
    """
    region = filters.get("region", "Combined")

    if region == "Balochistan":
        return balochistan_queries.get_recent_observations(limit)

    elif region == "Combined":
        return balochistan_queries.get_recent_observations(limit)

    # Default fallback
    return []


# ============================================================================
# STUDENT SCORES QUERIES
# ============================================================================

def get_student_scores_by_subject(filters: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Get average student scores by subject.

    Returns:
        List of {subject, avg_score, pass_rate, count} dicts
    """
    region = filters.get("region", "Combined")

    if region == "Moawin":
        return moawin_queries.get_student_scores_by_subject()

    elif region == "Combined":
        return moawin_queries.get_student_scores_by_subject()

    # Default fallback
    return []


# ============================================================================
# ATTENDANCE QUERIES
# ============================================================================

def get_attendance_trend(filters: Dict[str, Any], days: int = 30) -> List[Dict[str, Any]]:
    """
    Get daily attendance rates.

    Returns:
        List of {date, rate} dicts
    """
    region = filters.get("region", "Combined")

    if region == "Moawin":
        return moawin_queries.get_attendance_trend(days)

    elif region == "Combined":
        return moawin_queries.get_attendance_trend(days)

    # Default fallback
    return []
