#!/usr/bin/env python3
"""
Daily data refresh script for the Observability Dashboard.

Queries all 5 databases and saves results to a local JSON cache.
Designed to run via cron/launchd at 8 AM daily.

Usage:
    python scripts/refresh_cache.py

Exit codes:
    0 - All databases refreshed successfully
    1 - One or more databases failed (partial refresh)
    2 - Script error
"""
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.db_connections import (
    query_balochistan,
    query_islamabad,
    query_moawin_direct,
    query_rumi,
    check_all_connections,
)

CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def refresh_bigquery() -> dict:
    """Pull key metrics from BigQuery (ICT, RWP, Balochistan unified views)."""
    dataset = "niete-bq-prod.taleemabad_analytics"
    metrics = {}

    # Program summary
    rows = query_islamabad(f"""
        SELECT * FROM `{dataset}.program_summary`
    """)
    metrics["program_summary"] = rows

    # LP usage (last 30 days)
    rows = query_islamabad(f"""
        SELECT program, COUNT(DISTINCT user_id) as unique_users, COUNT(*) as total_events
        FROM `{dataset}.unified_lp_usage`
        WHERE timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        GROUP BY program
    """)
    metrics["lp_usage_30d"] = rows

    # Training submissions
    rows = query_islamabad(f"""
        SELECT program, COUNT(DISTINCT user_id) as unique_users, COUNT(*) as total_submissions
        FROM `{dataset}.unified_training_submissions`
        GROUP BY program
    """)
    metrics["training_submissions"] = rows

    # Retention (30-day active users)
    rows = query_islamabad(f"""
        SELECT program,
            COUNT(DISTINCT CASE WHEN timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY) THEN user_id END) as active_7d,
            COUNT(DISTINCT CASE WHEN timestamp > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY) THEN user_id END) as active_30d,
            COUNT(DISTINCT user_id) as total_users
        FROM `{dataset}.unified_events`
        GROUP BY program
    """)
    metrics["retention"] = rows

    # FICO scores (ICT TEACH observations)
    rows = query_islamabad("""
        SELECT
            AVG(SAFE_CAST(TOL AS FLOAT64)) as section_b_avg,
            AVG(SAFE_CAST(CU AS FLOAT64)) as section_c_avg,
            AVG(SAFE_CAST(CT AS FLOAT64)) as section_d_avg,
            COUNT(*) as obs_count
        FROM `niete-bq-prod.tbproddb.TEACH_TOOL_OBSERVATION_CLEANED`
    """)
    metrics["fico_ict"] = rows

    return metrics


def refresh_balochistan() -> dict:
    """Pull key metrics from Balochistan Neon."""
    metrics = {}

    rows = query_balochistan("""
        SELECT COUNT(*) as count,
            COUNT(CASE WHEN ai_results IS NOT NULL THEN 1 END) as ai_count,
            COUNT(CASE WHEN human_results IS NOT NULL THEN 1 END) as human_count
        FROM observations
    """)
    metrics["observation_counts"] = rows

    # FICO section averages from AI results
    rows = query_balochistan("""
        SELECT
            AVG((ai_results->'section_b'->>'score')::float) as section_b,
            AVG((ai_results->'section_c'->>'score')::float) as section_c,
            AVG((ai_results->'section_d'->>'score')::float) as section_d
        FROM observations
        WHERE ai_results IS NOT NULL
    """)
    metrics["fico_scores"] = rows

    return metrics


def refresh_moawin() -> dict:
    """Pull key metrics from SchoolPilot/Moawin."""
    metrics = {}

    rows = query_moawin_direct("SELECT COUNT(*) as count FROM schools")
    metrics["school_count"] = rows

    rows = query_moawin_direct("SELECT COUNT(*) as count FROM teachers")
    metrics["teacher_count"] = rows

    rows = query_moawin_direct("""
        SELECT subject, COUNT(*) as count, AVG(score) as avg_score
        FROM student_scores
        GROUP BY subject
    """)
    metrics["student_scores"] = rows

    rows = query_moawin_direct("SELECT COUNT(*) as count FROM task_completions")
    metrics["task_completions"] = rows

    rows = query_moawin_direct("SELECT COUNT(*) as count FROM attendance")
    metrics["attendance_count"] = rows

    return metrics


def refresh_rumi() -> dict:
    """Pull key metrics from Rumi Supabase."""
    metrics = {}

    rows = query_rumi("SELECT COUNT(*) as count FROM users")
    metrics["user_count"] = rows

    rows = query_rumi("""
        SELECT COUNT(*) as total_sessions,
            COUNT(CASE WHEN type = 'coaching' THEN 1 END) as coaching_sessions,
            COUNT(CASE WHEN type = 'lesson_plan' THEN 1 END) as lp_sessions
        FROM sessions
    """)
    metrics["session_counts"] = rows

    rows = query_rumi("SELECT COUNT(*) as count FROM lesson_plans")
    metrics["lesson_plan_count"] = rows

    return metrics


def _serialize(obj):
    """JSON serializer for non-standard types."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    if isinstance(obj, bytes):
        return obj.decode("utf-8", errors="replace")
    return str(obj)


def main():
    log("Starting daily data refresh...")
    today = datetime.now().strftime("%Y-%m-%d")
    results = {"timestamp": datetime.now().isoformat(), "databases": {}}
    failures = 0

    # Check connections first
    log("Checking database connections...")
    status = check_all_connections()
    for db, ok in status.items():
        log(f"  {db}: {'connected' if ok else 'FAILED'}")

    # Refresh each database
    db_tasks = [
        ("bigquery", refresh_bigquery),
        ("balochistan", refresh_balochistan),
        ("moawin", refresh_moawin),
        ("rumi", refresh_rumi),
    ]

    for name, func in db_tasks:
        log(f"Refreshing {name}...")
        try:
            data = func()
            results["databases"][name] = {"status": "ok", "data": data}
            log(f"  {name}: OK")
        except Exception as e:
            results["databases"][name] = {"status": "error", "error": str(e)}
            log(f"  {name}: FAILED - {e}")
            failures += 1

    # Save cache file
    cache_file = CACHE_DIR / f"metrics_{today}.json"
    with open(cache_file, "w") as f:
        json.dump(results, f, indent=2, default=_serialize)
    log(f"Cache saved to {cache_file}")

    # Also save as latest.json for easy access
    latest_file = CACHE_DIR / "latest.json"
    with open(latest_file, "w") as f:
        json.dump(results, f, indent=2, default=_serialize)
    log(f"Latest cache updated at {latest_file}")

    if failures > 0:
        log(f"Completed with {failures} failure(s)")
        return 1
    else:
        log("All databases refreshed successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())
