import sqlite3
import os
from datetime import datetime


def setup_database(db_path: str, sql_file: str):
    """Seed sample database using sql script."""
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()
        
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()


def setup_results_db(results_db_path: str):
    """Initialize results.db store to log test execution history."""
    conn = sqlite3.connect(results_db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            check_name TEXT NOT NULL,
            status TEXT NOT NULL,
            records_found INTEGER,
            executed_at TEXT
        );
    """)
    conn.commit()
    conn.close()


def log_test_result(results_db_path: str, check_name: str, status: str, count: int):
    """Save execution result into results.db."""
    conn = sqlite3.connect(results_db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO test_runs (check_name, status, records_found, executed_at) VALUES (?, ?, ?, ?)",
        (check_name, status, count, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def run_data_validation_checks(db_path: str, results_db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    checks = {
        "Check 1: Orphan Orders (Missing Customer)": """
            SELECT o.order_id, o.customer_id 
            FROM orders o 
            LEFT JOIN customers c ON o.customer_id = c.customer_id 
            WHERE c.customer_id IS NULL;
        """,
        "Check 2: Orphan Items (Missing Order)": """
            SELECT oi.item_id, oi.order_id 
            FROM order_items oi 
            LEFT JOIN orders o ON oi.order_id = o.order_id 
            WHERE o.order_id IS NULL;
        """,
        "Check 3: Mismatch Order Total vs Items Sum": """
            SELECT o.order_id, o.total_amount, SUM(oi.quantity * oi.unit_price) as item_sum
            FROM orders o
            JOIN order_items oi ON o.order_id = oi.order_id
            GROUP BY o.order_id
            HAVING o.total_amount <> SUM(oi.quantity * oi.unit_price);
        """,
        "Check 4: Duplicate Emails": """
            SELECT email, COUNT(*) 
            FROM customers 
            WHERE email IS NOT NULL 
            GROUP BY email 
            HAVING COUNT(*) > 1;
        """,
        "Check 5: NULL Email Customers": """
            SELECT customer_id, name 
            FROM customers 
            WHERE email IS NULL;
        """
    }

    print("\n================ RUNNING SQL DATA VALIDATION CHECKS ================")
    
    for check_name, query in checks.items():
        cursor.execute(query)
        results = cursor.fetchall()
        fail_count = len(results)
        
        # QA Logic: Validation fails if invalid data rows exist
        status = "FAIL" if fail_count > 0 else "PASS"
        log_test_result(results_db_path, check_name, status, fail_count)

        status_flag = "🔴 FAIL" if status == "FAIL" else "🟢 PASS"
        print(f"\n{status_flag} | {check_name}")
        print(f"Discrepancies/Bugs Found: {fail_count}")
        if results:
            print(f"  Sample Affected Records: {results}")

    conn.close()


if __name__ == "__main__":
    db_file = "samples/orders.db"
    sql_file = "core/sql_exercises.sql"
    results_db = "samples/results.db"

    # Execute flow
    setup_database(db_file, sql_file)
    setup_results_db(results_db)
    run_data_validation_checks(db_file, results_db)

    print("\n===================================================================")
    print("All checks completed and logged to samples/results.db successfully!")