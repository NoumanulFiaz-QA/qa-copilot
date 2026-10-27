# core/techniques.py

# =========================================================
# Task 1: Boundary Value Analysis (BVA) Helper
# =========================================================
def boundary_values(min_val: int, max_val: int) -> dict:
    """
    Returns 6 boundary values for a given min and max range.
    """
    if min_val > max_val:
        raise ValueError("min_val max_val se barra nahi ho sakta")
        
    return {
        "invalid_low": min_val - 1,
        "valid_min": min_val,
        "valid_min_plus_1": min_val + 1,
        "valid_max_minus_1": max_val - 1,
        "valid_max": max_val,
        "invalid_high": max_val + 1
    }


# =========================================================
# Task 2: Equivalence Partitioning (EP) Helper
# =========================================================
def partition_age(age: int) -> str:
    """
    Returns ticket pricing equivalence class based on age.
    """
    if not isinstance(age, (int, float)) or age < 0:
        return "Invalid Age"
    elif age <= 12:
        return "Child"
    elif age <= 59:
        return "Adult"
    else:
        return "Senior"


# =========================================================
# Task 3: Loop over 20 Mock Results and Print Summary
# =========================================================
def summarize_test_results(results: list) -> dict:
    """
    Loops through test execution results and prints pass/fail counts.
    """
    passed = 0
    failed = 0
    
    for result in results:
        if result.get("status") == "PASS":
            passed += 1
        elif result.get("status") == "FAIL":
            failed += 1

    print("=" * 30)
    print("      TEST RESULTS SUMMARY     ")
    print("=" * 30)
    print(f"Total Tests Executed : {len(results)}")
    print(f"Total Passed         : {passed}")
    print(f"Total Failed         : {failed}")
    print("=" * 30)

    return {"total": len(results), "passed": passed, "failed": failed}


# =========================================================
# Task 4: Self-Checks (5+ Assertions)
# =========================================================
if __name__ == "__main__":
    # --- Assert Check 1: BVA correct boundary values ---
    bva_res = boundary_values(1, 100)
    assert bva_res["invalid_low"] == 0, "Assert Fail: invalid_low should be 0"
    assert bva_res["valid_min"] == 1, "Assert Fail: valid_min should be 1"
    assert bva_res["invalid_high"] == 101, "Assert Fail: invalid_high should be 101"

    # --- Assert Check 2: EP Invalid Age ---
    assert partition_age(-5) == "Invalid Age", "Assert Fail: Negative age check"

    # --- Assert Check 3: EP Child Ticket ---
    assert partition_age(10) == "Child", "Assert Fail: Child age check"

    # --- Assert Check 4: EP Adult Ticket ---
    assert partition_age(25) == "Adult", "Assert Fail: Adult age check"

    # --- Assert Check 5: EP Senior Ticket ---
    assert partition_age(65) == "Senior", "Assert Fail: Senior age check"

    # --- Assert Check 6: Mock Results Summary ---
    mock_results = [
        {"id": 1, "status": "PASS"}, {"id": 2, "status": "PASS"},
        {"id": 3, "status": "FAIL"}, {"id": 4, "status": "PASS"},
        {"id": 5, "status": "PASS"}, {"id": 6, "status": "FAIL"},
        {"id": 7, "status": "PASS"}, {"id": 8, "status": "PASS"},
        {"id": 9, "status": "PASS"}, {"id": 10, "status": "PASS"},
        {"id": 11, "status": "FAIL"}, {"id": 12, "status": "PASS"},
        {"id": 13, "status": "PASS"}, {"id": 14, "status": "PASS"},
        {"id": 15, "status": "PASS"}, {"id": 16, "status": "FAIL"},
        {"id": 17, "status": "PASS"}, {"id": 18, "status": "PASS"},
        {"id": 19, "status": "PASS"}, {"id": 20, "status": "PASS"}
    ]
    summary = summarize_test_results(mock_results)
    assert summary["passed"] == 16, "Assert Fail: Passed count wrong"
    assert summary["failed"] == 4, "Assert Fail: Failed count wrong"

    print("\n All 6 Asserts Passed Successfully!")