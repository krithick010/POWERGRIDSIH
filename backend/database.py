"""
Database connection and session management
"""

import os
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from typing import Generator

DATABASE_URL = "postgresql://vmeenakshisundaram@localhost:5432/powergrid_tickets"

# Connection pool for better performance
connection_pool = None

def init_db_pool(minconn=1, maxconn=10):
    """Initialize database connection pool"""
    global connection_pool
    if connection_pool is None:
        connection_pool = SimpleConnectionPool(minconn, maxconn, DATABASE_URL)
    return connection_pool

def get_db_pool():
    """Get the database connection pool"""
    if connection_pool is None:
        init_db_pool()
    return connection_pool

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    pool = get_db_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        pool.putconn(conn)

@contextmanager
def get_db_cursor(cursor_factory=RealDictCursor) -> Generator:
    """Context manager for database cursors"""
    with get_db_connection() as conn:
        cursor = conn.cursor(cursor_factory=cursor_factory)
        try:
            yield cursor
        finally:
            cursor.close()
