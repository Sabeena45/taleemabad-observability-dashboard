"""
Common metrics module for cross-region comparison.
Provides 6 standardized metrics across all 5 regions:
  1. Observations (vs Benchmark)
  2. Lesson Plan Engagement
  3. Teacher Training Engagement
  4. Retention (7-day & 30-day)
  5. FICO / Observation Scores by Section
  6. Student Learning
"""
import streamlit as st
from typing import Dict, Any
from . import (
    islamabad_queries,
    balochistan_queries,
    rawalpindi_queries,
    moawin_queries,
    rumi_queries,
)
from .db_connections import query_islamabad, query_rumi, query_moawin_direct

CACHE_TTL = 28800  # 8 hours

REGIONS = ["ICT", "Balochistan", "RWP", "Moawin", "Rumi"]

REGION_COLORS = {
    "ICT": "#3B82F6",
    "Balochistan": "#F59E0B",
    "RWP": "#8B5CF6",
    "Moawin": "#16A34A",
    "Rumi": "#EF4444",
}

ANALYTICS_DATASET = "niete-bq-prod.taleemabad_analytics"

OBSERVATION_BENCHMARKS = {
    "ICT": {"coaches": 55, "obs_per_day": 4, "working_days_per_month": 22},
    "RWP": {"coaches": 27, "obs_per_day": 4, "working_days_per_month": 22},
    "Balochistan": None,
    "Moawin": None,
    "Rumi": None,
}

METRIC_DEFINITIONS = {
    "observations": {
        "name": "Observations (vs Benchmark)",
        "definition": (
            "Total classroom observations (AI + human) compared to expected capacity. "
            "Benchmark = coaches x 4 observations/day x 22 working days/month. "
            "ICT: 55 coaches. RWP: 4 TMs + 23 AEOs = 27 coaches."
        ),
    },
    "lp_engagement": {
        "name": "Lesson Plan Engagement",
        "definition": (
            "Total lesson plan interactions per unique active teacher. "
            "Measures whether teachers are using the platform's instructional resources. "
            "Source: BigQuery unified_lp_usage for ICT/Balochistan/RWP, "
            "SchoolPilot task_completions for Moawin, Supabase lesson_plans for Rumi."
        ),
    },
    "training": {
        "name": "Teacher Training Engagement",
        "definition": (
            "Total training module submissions per unique teacher. "
            "Measures professional development uptake. "
            "Source: BigQuery unified_training_submissions for ICT/Balochistan/RWP, "
            "SchoolPilot teacher_training_progress for Moawin. "
            "Rumi is coaching-only (not applicable)."
        ),
    },
    "retention": {
        "name": "Retention (7-day & 30-day)",
        "definition": (
            "Percentage of total users who were active in the last 7 or 30 days. "
            "Measures sustained platform engagement. "
            "Calculated as: active users in window / total users x 100. "
            "Source: BigQuery unified_events for ICT/Balochistan/RWP, "
            "SchoolPilot attendance for Moawin (school-level), "
            "Supabase chat_sessions for Rumi."
        ),
    },
    "fico": {
        "name": "FICO / Observation Scores by Section",
        "definition": (
            "Average instructional quality scores across FICO framework sections. "
            "Section B: Explanation & Lesson Facilitation. "
            "Section C: Understanding & Feedback. "
            "Section D: Participation & Socio-emotional Skills. "
            "Scores represent % of 'Yes' or positive responses per indicator. "
            "Source: BigQuery TEACH observations for ICT, Neon JSONB for Balochistan."
        ),
    },
    "student_learning": {
        "name": "Student Learning",
        "definition": (
            "Average student assessment scores and pass rates where direct data is available. "
            "For research programs, reports effect size from RCT/quasi-experimental studies. "
            "Source: Teacher certification RCT for ICT (effect size 0.46), "
            "SchoolPilot student_scores for Moawin, "
            "Supabase reading_assessments (WCPM) for Rumi."
        ),
    },
}

REGION_PARAMETERS = {
    "ICT": {
        "coaches": 55,
        "schools": 465,
        "teachers": 10309,
        "students": 90000,
    },
    "RWP": {
        "coaches": 27,
        "coaches_detail": "4 TMs + 23 AEOs",
        "schools": 260,
        "teachers": 900,
        "students": 37000,
    },
    "Balochistan": {
        "schools": 69,
        "teachers": 933,
        "students": 6733,
    },
    "Moawin": {
        "schools": 236,
        "teachers": 602,
        "students": 18758,
    },
    "Rumi": {
        "coaches": "AI-only",
        "teachers": 1871,
    },
}


# ============================================================================
# METRIC 1: Observations (vs Benchmark)
# ============================================================================

@st.cache_data(ttl=CACHE_TTL)
def get_observation_metrics() -> Dict[str, Dict[str, Any]]:
    """Get observation counts and benchmarks per region."""
    results = {}

    # ICT: Human observations from BigQuery TEACH table
    ict_obs = islamabad_queries.get_observation_counts()
    bm = OBSERVATION_BENCHMARKS["ICT"]
    ict_monthly = bm["coaches"] * bm["obs_per_day"] * bm["working_days_per_month"]
    results["ICT"] = {
        "actual": ict_obs.get("total", 2423),
        "benchmark_monthly": ict_monthly,
        "type": "Human (TEACH)",
        "status": "active",
    }

    # Balochistan: AI + Human from Neon
    bal_obs = balochistan_queries.get_observation_counts()
    results["Balochistan"] = {
        "actual": bal_obs.get("total", 576),
        "ai": bal_obs.get("ai_count", 522),
        "human": bal_obs.get("human_count", 54),
        "benchmark_monthly": None,
        "type": "AI + Human",
        "status": "active",
    }

    # RWP: Not yet deployed
    bm_rwp = OBSERVATION_BENCHMARKS["RWP"]
    rwp_monthly = bm_rwp["coaches"] * bm_rwp["obs_per_day"] * bm_rwp["working_days_per_month"]
    results["RWP"] = {
        "actual": 0,
        "benchmark_monthly": rwp_monthly,
        "type": None,
        "status": "launching_q2_2026",
    }

    # Moawin: Not applicable
    results["Moawin"] = {
        "actual": None,
        "benchmark_monthly": None,
        "type": None,
        "status": "not_applicable",
    }

    # Rumi: Audio coaching sessions
    rumi_obs = rumi_queries.get_observation_counts()
    results["Rumi"] = {
        "actual": rumi_obs.get("ai_count", 135),
        "benchmark_monthly": None,
        "type": "AI Audio Coaching",
        "status": "active",
    }

    return results


# ============================================================================
# METRIC 2: Lesson Plan Engagement
# ============================================================================

@st.cache_data(ttl=CACHE_TTL)
def get_lp_engagement_metrics() -> Dict[str, Dict[str, Any]]:
    """Get LP engagement per region."""
    results = {}

    # BigQuery programs (ICT, Balochistan, RWP)
    sql = f"""
        SELECT
            program,
            COUNT(*) as total_events,
            COUNT(DISTINCT user_id) as unique_teachers
        FROM `{ANALYTICS_DATASET}.unified_lp_usage`
        GROUP BY program
    """
    bq_results = query_islamabad(sql)

    bq_data = {}
    if bq_results:
        for r in bq_results:
            prog = r.get("program", "").lower()
            bq_data[prog] = {
                "total_events": int(r.get("total_events", 0) or 0),
                "unique_teachers": int(r.get("unique_teachers", 0) or 0),
            }

    for region, bq_key in [("ICT", "ict"), ("Balochistan", "balochistan"), ("RWP", "rawalpindi")]:
        d = bq_data.get(bq_key, {})
        total = d.get("total_events", 0)
        teachers = d.get("unique_teachers", 0)
        results[region] = {
            "total_events": total,
            "unique_teachers": teachers,
            "per_teacher": round(total / teachers, 1) if teachers > 0 else 0,
            "status": "active" if total > 0 else "no_data",
        }

    # Moawin: task_completions as LP proxy
    moawin_tasks = moawin_queries.get_task_completion_rate()
    results["Moawin"] = {
        "total_events": moawin_tasks.get("total_tasks", 2280),
        "unique_teachers": 0,
        "per_teacher": 0,
        "type": "Task Completions",
        "status": "active",
    }

    # Rumi: lesson_plans table
    rumi_lp = rumi_queries.get_lesson_plan_metrics()
    total = rumi_lp.get("total_plans", 1815)
    teachers = rumi_lp.get("unique_teachers", 0)
    results["Rumi"] = {
        "total_events": total,
        "unique_teachers": teachers,
        "per_teacher": round(total / teachers, 1) if teachers > 0 else 0,
        "type": "AI-Generated Plans",
        "status": "active",
    }

    return results


# ============================================================================
# METRIC 3: Teacher Training Engagement
# ============================================================================

@st.cache_data(ttl=CACHE_TTL)
def get_training_metrics() -> Dict[str, Dict[str, Any]]:
    """Get training engagement per region."""
    results = {}

    # BigQuery programs
    sql = f"""
        SELECT
            program,
            COUNT(*) as total_submissions,
            COUNT(DISTINCT user_id) as unique_teachers
        FROM `{ANALYTICS_DATASET}.unified_training_submissions`
        GROUP BY program
    """
    bq_results = query_islamabad(sql)

    bq_data = {}
    if bq_results:
        for r in bq_results:
            prog = r.get("program", "").lower()
            bq_data[prog] = {
                "total_submissions": int(r.get("total_submissions", 0) or 0),
                "unique_teachers": int(r.get("unique_teachers", 0) or 0),
            }

    for region, bq_key in [("ICT", "ict"), ("Balochistan", "balochistan"), ("RWP", "rawalpindi")]:
        d = bq_data.get(bq_key, {})
        total = d.get("total_submissions", 0)
        teachers = d.get("unique_teachers", 0)
        results[region] = {
            "total_submissions": total,
            "unique_teachers": teachers,
            "per_teacher": round(total / teachers, 1) if teachers > 0 else 0,
            "status": "active" if total > 0 else "no_data",
        }

    # Moawin: teacher_training_progress
    moawin_training = moawin_queries.get_training_progress()
    results["Moawin"] = {
        "total_submissions": moawin_training.get("teachers_started", 0),
        "unique_teachers": moawin_training.get("teachers_completed", 0),
        "per_teacher": 0,
        "avg_progress": moawin_training.get("avg_progress", 0),
        "status": "active",
    }

    # Rumi: N/A (coaching, not training)
    results["Rumi"] = {
        "total_submissions": None,
        "unique_teachers": None,
        "per_teacher": None,
        "status": "not_applicable",
    }

    return results


# ============================================================================
# METRIC 4: Retention (7-day & 30-day)
# ============================================================================

@st.cache_data(ttl=CACHE_TTL)
def get_retention_metrics() -> Dict[str, Dict[str, Any]]:
    """Get retention metrics per region."""
    results = {}

    # BigQuery programs
    sql = f"""
        SELECT
            program,
            COUNT(DISTINCT CASE
                WHEN timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
                THEN user_id END) as active_7d,
            COUNT(DISTINCT CASE
                WHEN timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
                THEN user_id END) as active_30d,
            COUNT(DISTINCT user_id) as total_users
        FROM `{ANALYTICS_DATASET}.unified_events`
        GROUP BY program
    """
    bq_results = query_islamabad(sql)

    bq_data = {}
    if bq_results:
        for r in bq_results:
            prog = r.get("program", "").lower()
            total = int(r.get("total_users", 0) or 0)
            a7 = int(r.get("active_7d", 0) or 0)
            a30 = int(r.get("active_30d", 0) or 0)
            bq_data[prog] = {
                "active_7d": a7,
                "active_30d": a30,
                "total_users": total,
                "retention_7d": round(a7 / total * 100, 1) if total > 0 else 0,
                "retention_30d": round(a30 / total * 100, 1) if total > 0 else 0,
            }

    default_val = {"active_7d": 0, "active_30d": 0, "total_users": 0,
                   "retention_7d": 0, "retention_30d": 0}

    for region, bq_key in [("ICT", "ict"), ("Balochistan", "balochistan"), ("RWP", "rawalpindi")]:
        d = bq_data.get(bq_key, default_val.copy())
        d["status"] = "active"
        results[region] = d

    # Moawin: attendance as retention proxy (school-level)
    attendance_sql = """
        SELECT
            COUNT(DISTINCT CASE WHEN date >= CURRENT_DATE - INTERVAL '7 days'
                THEN school_id END) as active_7d,
            COUNT(DISTINCT CASE WHEN date >= CURRENT_DATE - INTERVAL '30 days'
                THEN school_id END) as active_30d,
            COUNT(DISTINCT school_id) as total_schools
        FROM attendance
        WHERE total_students > 0
    """
    moawin_results = query_moawin_direct(attendance_sql)
    if moawin_results and moawin_results[0].get("total_schools"):
        r = moawin_results[0]
        total = int(r.get("total_schools", 0) or 0)
        a7 = int(r.get("active_7d", 0) or 0)
        a30 = int(r.get("active_30d", 0) or 0)
        results["Moawin"] = {
            "active_7d": a7, "active_30d": a30, "total_users": total,
            "retention_7d": round(a7 / total * 100, 1) if total > 0 else 0,
            "retention_30d": round(a30 / total * 100, 1) if total > 0 else 0,
            "type": "School attendance",
            "status": "active",
        }
    else:
        results["Moawin"] = {
            "active_7d": 0, "active_30d": 0, "total_users": 236,
            "retention_7d": 0, "retention_30d": 0,
            "type": "School attendance", "status": "active",
        }

    # Rumi: chat sessions
    conv = rumi_queries.get_conversation_metrics()
    total_users = 1871
    a7 = conv.get("active_users_7d", 0)
    a30 = conv.get("active_users_30d", 0)
    results["Rumi"] = {
        "active_7d": a7, "active_30d": a30, "total_users": total_users,
        "retention_7d": round(a7 / total_users * 100, 1) if total_users > 0 else 0,
        "retention_30d": round(a30 / total_users * 100, 1) if total_users > 0 else 0,
        "type": "Chat sessions",
        "status": "active",
    }

    return results


# ============================================================================
# METRIC 5: FICO / Observation Scores by Section
# ============================================================================

@st.cache_data(ttl=CACHE_TTL)
def get_fico_metrics() -> Dict[str, Dict[str, Any]]:
    """Get FICO section scores per region."""
    results = {}

    # ICT
    ict_fico = islamabad_queries.get_fico_scores()
    if ict_fico.get("section_b"):
        b_vals = [v for v in ict_fico["section_b"].values() if v]
        c_vals = [v for v in ict_fico["section_c"].values() if v]
        d_vals = [v for v in ict_fico["section_d"].values() if v]
        results["ICT"] = {
            "section_b": ict_fico["section_b"],
            "section_c": ict_fico["section_c"],
            "section_d": ict_fico["section_d"],
            "b_avg": round(sum(b_vals) / len(b_vals), 1) if b_vals else 0,
            "c_avg": round(sum(c_vals) / len(c_vals), 1) if c_vals else 0,
            "d_avg": round(sum(d_vals) / len(d_vals), 1) if d_vals else 0,
            "type": "TEACH Tool (Human)",
            "status": "active",
        }
    else:
        results["ICT"] = {"status": "no_data"}

    # Balochistan
    bal_fico = balochistan_queries.get_fico_scores()
    if bal_fico.get("section_b"):
        b_vals = [v for v in bal_fico["section_b"].values() if v]
        c_vals = [v for v in bal_fico["section_c"].values() if v]
        d_vals = [v for v in bal_fico["section_d"].values() if v]
        results["Balochistan"] = {
            "section_b": bal_fico["section_b"],
            "section_c": bal_fico["section_c"],
            "section_d": bal_fico["section_d"],
            "b_avg": round(sum(b_vals) / len(b_vals), 1) if b_vals else 0,
            "c_avg": round(sum(c_vals) / len(c_vals), 1) if c_vals else 0,
            "d_avg": round(sum(d_vals) / len(d_vals), 1) if d_vals else 0,
            "type": "AI (Rumi) + Human",
            "status": "active",
        }
    else:
        results["Balochistan"] = {"status": "no_data"}

    results["RWP"] = {"status": "no_data"}
    results["Moawin"] = {"status": "not_applicable"}
    results["Rumi"] = {"status": "not_applicable"}

    return results


# ============================================================================
# METRIC 6: Student Learning
# ============================================================================

@st.cache_data(ttl=CACHE_TTL)
def get_student_learning_metrics() -> Dict[str, Dict[str, Any]]:
    """Get student learning metrics per region."""
    results = {}

    # ICT: Research effect size
    results["ICT"] = {
        "type": "RCT Effect Size",
        "effect_size": 0.46,
        "description": "0.46 SD improvement (Cohen's d) from teacher certification",
        "status": "active",
    }

    # Balochistan: No direct student data
    results["Balochistan"] = {"status": "no_data"}

    # RWP: No data yet
    results["RWP"] = {"status": "no_data"}

    # Moawin: Student scores
    scores = moawin_queries.get_student_scores_by_subject()
    if scores:
        avg_score = sum(s["avg_score"] for s in scores) / len(scores)
        avg_pass = sum(s["pass_rate"] for s in scores) / len(scores)
        total_count = sum(s["count"] for s in scores)
        results["Moawin"] = {
            "type": "Assessment Scores",
            "subjects": scores,
            "avg_score": round(avg_score, 1),
            "avg_pass_rate": round(avg_pass, 1),
            "total_assessments": total_count,
            "status": "active",
        }
    else:
        results["Moawin"] = {"status": "no_data"}

    # Rumi: Reading assessments
    results["Rumi"] = {
        "type": "WCPM Reading Assessment",
        "total_assessments": 197,
        "description": "197 Words Correct Per Minute reading assessments",
        "status": "active",
    }

    return results


# ============================================================================
# ALL METRICS
# ============================================================================

def get_all_metrics() -> Dict[str, Any]:
    """Get all 6 metrics in a single call."""
    return {
        "observations": get_observation_metrics(),
        "lp_engagement": get_lp_engagement_metrics(),
        "training": get_training_metrics(),
        "retention": get_retention_metrics(),
        "fico": get_fico_metrics(),
        "student_learning": get_student_learning_metrics(),
        "parameters": REGION_PARAMETERS,
        "definitions": METRIC_DEFINITIONS,
    }
