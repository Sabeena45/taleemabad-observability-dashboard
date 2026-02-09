"""
Rawalpindi queries for the observability dashboard.
Data source: BigQuery unified views (niete-bq-prod.taleemabad_analytics)

Uses unified cross-program views filtered to program = 'rawalpindi'.

Program parameters (user-provided Feb 2026):
- 260 schools
- 900 teachers
- 37,000 students
- 4 Training Managers + 23 AEOs = 27 coaches
- Observation benchmark: 27 coaches x 4 obs/day x 22 days = 2,376/month

BigQuery counts (Feb 2026 - data still populating):
- 21 schools in BigQuery (260 total in program)
- 143 teachers in BigQuery (900 total in program)
- 0 students in BigQuery (37,000 total in program)
- 196 users
- 444,656 analytics events
"""
from typing import Dict, Any, List
from .db_connections import query_islamabad

# Program parameters (user-provided, Feb 2026)
# BigQuery unified views may show lower counts as data is still populating
RAWALPINDI_KNOWN_VALUES = {
    "schools": 260,
    "teachers": 900,
    "students": 37000,
    "users": 196,
    "events": 444656,
    "coaches": 27,  # 4 TMs + 23 AEOs
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
