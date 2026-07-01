import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="data/index.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    filename TEXT,
                    size INTEGER,
                    modified_time TEXT,
                    hash TEXT,
                    parent_dir TEXT,
                    indexed_at TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    scan_path TEXT,
                    scan_date TEXT,
                    files_count INTEGER,
                    total_size INTEGER
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS backup_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    check_date TEXT NOT NULL,
                    original_path TEXT,
                    backup_path TEXT,
                    missing_count INTEGER,
                    changed_count INTEGER,
                    extra_count INTEGER,
                    details TEXT
                )
            """)
            conn.commit()

    def save_file(self, path, filename, size, modified_time, hash_value, parent_dir):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO files
                (path, filename, size, modified_time, hash, parent_dir, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (path, filename, size, modified_time, hash_value, parent_dir,
                  datetime.now().isoformat()))
            conn.commit()

    def get_all_files(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT * FROM files").fetchall()

    def get_files_count(self):
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]

    def get_total_size(self):
        with sqlite3.connect(self.db_path) as conn:
            result = conn.execute("SELECT SUM(size) FROM files").fetchone()[0]
            return result if result else 0

    def save_scan_history(self, path, count, total_size):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO scans (scan_path, scan_date, files_count, total_size)
                VALUES (?, ?, ?, ?)
            """, (path, datetime.now().isoformat(), count, total_size))
            conn.commit()

    def save_backup_check(self, orig_path, backup_path, missing, changed, extra):
        import json
        with sqlite3.connect(self.db_path) as conn:
            details = json.dumps({
                'missing': missing,
                'changed': changed,
                'extra': extra
            })
            conn.execute("""
                INSERT INTO backup_checks
                (check_date, original_path, backup_path, missing_count, changed_count, extra_count, details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), orig_path, backup_path,
                  len(missing), len(changed), len(extra), details))
            conn.commit()