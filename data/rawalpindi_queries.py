"""
Rawalpindi queries for the observability dashboard.
Data source: BigQuery unified views (niete-bq-prod.taleemabad_analytics)

Uses unified cross-program views filtered to program = 'rawalpindi'.

Verified counts (Feb 2026):
- 21 schools (from rwp_proddb)
- 143 teachers
- 0 students (no student data yet)
- 196 users
- 444,656 analytics events
"""
from typing import Dict, Any, List
from .db_connections import query_islamabad

# Fallback values from BigQuery unified views (Feb 2026)
RAWALPINDI_KNOWN_VALUES = {
    "schools": 21,
    "teachers": 143,
    "students": 0,
    "users": 196,
    "events": 444656,
}

# All queries use the taleemabad_analytics dataset (unified views)
ANALYTICS_DATASET = "niete-bq-prod.taleemabad_analytics"


def get_summary_metrics(time_period: str = "All Time") -> Dict[str, Any]:
    """
    Get summary metrics for Rawalpindi from unified BigQuery views.

    Args:
        time_period: Time filter (not applicable to most unified views)

    Returns:
        Dict with schools, teachers, ai_sessions, human_observations, avg_score, students
    """
    # Get counts from program_summary view
    sql = f"""
        SELECT *
        FROM `{ANALYTICS_DATASET}.program_summary`
        WHERE LOWER(program) = 'rawalpindi'
    """
    results = query_islamabad(sql)
    if results:
        r = results[0]
        return {
            "schools": int(r.get("schools", 0) or 0),
            "teachers": int(r.get("total_teachers", 0) or 0),
            "ai_sessions": 0,
            "human_observations": 0,
            "avg_score": 0,
            "students": int(r.get("students", 0) or 0),
        }

    # Fallback: query individual unified views
    schools = get_school_count()
    teachers = get_teacher_count()
    students = get_student_count()

    return {
        "schools": schools,
        "teachers": teachers,
        "ai_sessions": 0,
        "human_observations": 0,
        "avg_score": 0,
        "students": students,
    }


def get_school_count() -> int:
    """Get count of Rawalpindi schools from unified view."""
    sql = f"""
        SELECT COUNT(*) as count
        FROM `{ANALYTICS_DATASET}.unified_schools`
        WHERE LOWER(program) = 'rawalpindi'
    """
    results = query_islamabad(sql)
    if results:
        return int(results[0].get("count", 0) or 0)
    return RAWALPINDI_KNOWN_VALUES["schools"]


def get_teacher_count() -> int:
    """Get count of Rawalpindi teachers from unified view."""
    sql = f"""
        SELECT COUNT(*) as count
        FROM `{ANALYTICS_DATASET}.unified_teachers`
        WHERE LOWER(program) = 'rawalpindi'
    """
    results = query_islamabad(sql)
    if results:
        return int(results[0].get("count", 0) or 0)
    return RAWALPINDI_KNOWN_VALUES["teachers"]


def get_student_count() -> int:
    """Get count of Rawalpindi students from unified view."""
    sql = f"""
        SELECT COUNT(*) as count
        FROM `{ANALYTICS_DATASET}.unified_students`
        WHERE LOWER(program) = 'rawalpindi'
    """
    results = query_islamabad(sql)
    if results:
        return int(results[0].get("count", 0) or 0)
    return RAWALPINDI_KNOWN_VALUES["students"]


def get_event_count() -> int:
    """Get count of Rawalpindi analytics events."""
    sql = f"""
        SELECT COUNT(*) as count
        FROM `{ANALYTICS_DATASET}.unified_events`
        WHERE LOWER(program) = 'rawalpindi'
    """
    results = query_islamabad(sql)
    if results:
        return int(results[0].get("count", 0) or 0)
    return RAWALPINDI_KNOWN_VALUES["events"]


def get_observation_counts(obs_type: str = "All Observations") -> Dict[str, Any]:
    """
    Rawalpindi doesn't have observation data yet.
    Returns zeros.
    """
    return {
        "ai_count": 0,
        "human_count": 0,
        "total": 0,
        "note": "Observation data not yet available for Rawalpindi"
    }


def get_observation_trend(weeks: int = 8) -> List[Dict[str, Any]]:
    """No observation trend data for Rawalpindi yet."""
    return []


def get_talk_time_metrics(obs_type: str = "All Observations") -> Dict[str, Any]:
    """No talk time data for Rawalpindi."""
    return {
        "student_talk_time": None,
        "teacher_talk_time": None,
        "target_student_time": 40.0,
        "note": "Talk time data not available for Rawalpindi"
    }


def get_question_metrics(obs_type: str = "All Observations") -> Dict[str, Any]:
    """No question data for Rawalpindi."""
    return {
        "avg_open_questions": None,
        "avg_closed_questions": None,
        "open_question_ratio": None,
        "note": "Question data not available for Rawalpindi"
    }


def get_fico_scores() -> Dict[str, Dict]:
    """No FICO scores for Rawalpindi yet."""
    return {
        "section_b": {},
        "section_c": {},
        "section_d": {},
    }
