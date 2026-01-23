"""
Database connection management for the observability dashboard.
Handles connections to Balochistan, Islamabad, and Moawin databases.
"""
import os
from typing import Optional, Any, Dict
from functools import lru_cache

# Import psycopg2 for PostgreSQL connections
try:
    import psycopg2
    import psycopg2.extras
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

# Import BigQuery client
try:
    from google.cloud import bigquery
    BIGQUERY_AVAILABLE = True
except ImportError:
    BIGQUERY_AVAILABLE = False

# Import SSH tunnel for Balochistan RDS
try:
    from sshtunnel import SSHTunnelForwarder
    SSHTUNNEL_AVAILABLE = True
except ImportError:
    SSHTUNNEL_AVAILABLE = False


# ============================================================================
# BALOCHISTAN DATABASE (NIETE RDS via SSH Tunnel)
# ============================================================================

BALOCHISTAN_CONFIG = {
    # SSH Tunnel settings
    "ssh_host": "52.76.227.229",
    "ssh_username": "ubuntu",
    "ssh_key_path": os.environ.get("BALOCHISTAN_SSH_KEY", ""),

    # RDS settings (accessed via tunnel)
    "db_host": "terraform-2024112712521102930000000c.cl66yoig6i08.ap-southeast-1.rds.amazonaws.com",
    "db_port": 5432,
    "db_name": "tbniete_balochistan_db",
    "db_user": "niete_balochistan_ecs",
    "db_password": os.environ.get("BALOCHISTAN_DB_PASSWORD", "7xV8L9qxKLXdhZ84764erjhrf8"),

    # Local tunnel port
    "local_port": 5420
}

# Global tunnel reference
_balochistan_tunnel = None


def get_balochistan_connection():
    """
    Get connection to Balochistan database via SSH tunnel.

    Returns:
        psycopg2 connection object or None if unavailable
    """
    global _balochistan_tunnel

    if not PSYCOPG2_AVAILABLE:
        print("psycopg2 not available")
        return None

    try:
        # Try direct connection first (if tunnel already established externally)
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=BALOCHISTAN_CONFIG["local_port"],
                database=BALOCHISTAN_CONFIG["db_name"],
                user=BALOCHISTAN_CONFIG["db_user"],
                password=BALOCHISTAN_CONFIG["db_password"],
                connect_timeout=5
            )
            return conn
        except:
            pass

        # Try direct RDS connection (if accessible)
        try:
            conn = psycopg2.connect(
                host=BALOCHISTAN_CONFIG["db_host"],
                port=BALOCHISTAN_CONFIG["db_port"],
                database=BALOCHISTAN_CONFIG["db_name"],
                user=BALOCHISTAN_CONFIG["db_user"],
                password=BALOCHISTAN_CONFIG["db_password"],
                connect_timeout=10
            )
            return conn
        except Exception as e:
            print(f"Direct RDS connection failed: {e}")

        # SSH tunnel would be needed - skip for Replit deployment
        # Users can establish tunnel manually: ssh -L 5420:rds-host:5432 ubuntu@52.76.227.229
        return None

    except Exception as e:
        print(f"Balochistan connection error: {e}")
        return None


def query_balochistan(sql: str, params: tuple = None) -> list:
    """
    Execute a query against Balochistan database.

    Args:
        sql: SQL query string
        params: Query parameters (optional)

    Returns:
        List of rows as dictionaries, or empty list on error
    """
    conn = get_balochistan_connection()
    if not conn:
        return []

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            results = [dict(row) for row in cur.fetchall()]
        conn.close()
        return results
    except Exception as e:
        print(f"Balochistan query error: {e}")
        if conn:
            conn.close()
        return []


# ============================================================================
# ISLAMABAD DATABASE (BigQuery)
# ============================================================================

ISLAMABAD_CONFIG = {
    "project_id": "niete-bq-prod",
    "dataset_id": "tbproddb",
    "credentials_path": os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "/Users/sabeenaabbasi/Downloads/niete-bq-prod-8c5203708f8e.json"
    )
}

_bigquery_client = None


def get_bigquery_client():
    """
    Get BigQuery client for Islamabad data.

    Returns:
        BigQuery client or None if unavailable
    """
    global _bigquery_client

    if not BIGQUERY_AVAILABLE:
        print("google-cloud-bigquery not available")
        return None

    if _bigquery_client is not None:
        return _bigquery_client

    try:
        # Set credentials path
        if os.path.exists(ISLAMABAD_CONFIG["credentials_path"]):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ISLAMABAD_CONFIG["credentials_path"]

        _bigquery_client = bigquery.Client(project=ISLAMABAD_CONFIG["project_id"])
        return _bigquery_client
    except Exception as e:
        print(f"BigQuery client error: {e}")
        return None


def query_islamabad(sql: str) -> list:
    """
    Execute a query against Islamabad BigQuery dataset.

    Args:
        sql: SQL query string

    Returns:
        List of rows as dictionaries, or empty list on error
    """
    client = get_bigquery_client()
    if not client:
        return []

    try:
        query_job = client.query(sql)
        results = query_job.result()
        return [dict(row) for row in results]
    except Exception as e:
        print(f"BigQuery query error: {e}")
        return []


# ============================================================================
# MOAWIN DATABASE (SchoolPilot via MCP)
# ============================================================================

# SchoolPilot is accessed via MCP tool, not direct connection
# The MCP tool mcp__schoolpilot-db__query handles the connection

def query_moawin_direct(sql: str) -> list:
    """
    Direct query to SchoolPilot database (for non-MCP environments).

    Uses the Neon PostgreSQL connection directly.

    Args:
        sql: SQL query string

    Returns:
        List of rows as dictionaries, or empty list on error
    """
    if not PSYCOPG2_AVAILABLE:
        return []

    MOAWIN_CONFIG = {
        "host": "ep-lucky-flower-af17db2g.c-2.us-west-2.aws.neon.tech",
        "port": 5432,
        "database": "neondb",
        "user": "analyst_readonly_schoolpilot",
        "password": os.environ.get("SCHOOLPILOT_DB_PASSWORD", "")
    }

    try:
        conn = psycopg2.connect(
            host=MOAWIN_CONFIG["host"],
            port=MOAWIN_CONFIG["port"],
            database=MOAWIN_CONFIG["database"],
            user=MOAWIN_CONFIG["user"],
            password=MOAWIN_CONFIG["password"],
            sslmode="require",
            connect_timeout=10
        )

        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql)
            results = [dict(row) for row in cur.fetchall()]

        conn.close()
        return results
    except Exception as e:
        print(f"Moawin direct query error: {e}")
        return []


# ============================================================================
# RUMI DATABASE (Supabase)
# ============================================================================

RUMI_CONFIG = {
    "host": "aws-1-ap-southeast-1.pooler.supabase.com",
    "port": 6543,
    "database": "postgres",
    "user": "analyst.jlpenspfdcwxkopaidys",
    "password": os.environ.get("RUMI_DB_PASSWORD", "RumiAnalytics2026!")
}


def get_rumi_connection():
    """
    Get connection to Rumi Supabase database.

    Returns:
        psycopg2 connection object or None if unavailable
    """
    if not PSYCOPG2_AVAILABLE:
        return None

    try:
        conn = psycopg2.connect(
            host=RUMI_CONFIG["host"],
            port=RUMI_CONFIG["port"],
            database=RUMI_CONFIG["database"],
            user=RUMI_CONFIG["user"],
            password=RUMI_CONFIG["password"],
            sslmode="require",
            connect_timeout=10
        )
        return conn
    except Exception as e:
        print(f"Rumi connection error: {e}")
        return None


def query_rumi(sql: str, params: tuple = None) -> list:
    """
    Execute a query against Rumi database.

    Args:
        sql: SQL query string
        params: Query parameters (optional)

    Returns:
        List of rows as dictionaries, or empty list on error
    """
    conn = get_rumi_connection()
    if not conn:
        return []

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            results = [dict(row) for row in cur.fetchall()]
        conn.close()
        return results
    except Exception as e:
        print(f"Rumi query error: {e}")
        if conn:
            conn.close()
        return []


# ============================================================================
# CONNECTION STATUS CHECK
# ============================================================================

def check_all_connections() -> Dict[str, bool]:
    """
    Check connectivity to all databases.

    Returns:
        Dict with database names and their connection status
    """
    status = {}

    # Check Balochistan
    conn = get_balochistan_connection()
    status["balochistan"] = conn is not None
    if conn:
        conn.close()

    # Check BigQuery
    client = get_bigquery_client()
    status["islamabad"] = client is not None

    # Check Rumi
    conn = get_rumi_connection()
    status["rumi"] = conn is not None
    if conn:
        conn.close()

    # Check Moawin (direct)
    results = query_moawin_direct("SELECT 1 as test")
    status["moawin"] = len(results) > 0

    return status
