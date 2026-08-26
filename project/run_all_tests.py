import subprocess
import os
import sys

def run_all():
    test_files = [
        "tests/test_model.py",
        "tests/test_db.py",
        "tests/test_auth.py",
        "tests/test_api.py",
        "tests/test_validation.py",
        "tests/test_files.py",
        "tests/test_helpers.py",
        "tests/test_services.py",
        "tests/test_email.py",
        "tests/test_security.py",
        "tests/test_ui_pages.py"
    ]
    
    print("="*50)
    print("STUDENT PERFORMANCE SYSTEM - MASTER TEST SUITE")
    print("="*50)
    
    all_passed = True
    for test in test_files:
        print(f"Running: {test}...", end=" ", flush=True)
        try:
            # Use sys.executable to ensure we use the same python
            result = subprocess.run([sys.executable, test], capture_output=True, text=True, check=True)
            print("OK")
        except subprocess.CalledProcessError as e:
            print("FAILED")
            # Log error details
            print(f"-- Error details for {test}:")
            print(e.stdout)
            print(e.stderr)
            all_passed = False
            
    print("="*50)
    if all_passed:
        print("SUMMARY: ALL SYSTEMS CORE GREEN. 100% SUCCESS.")
    else:
        print("SUMMARY: SOME TESTS FAILED. CHECK LOGS.")
    print("="*50)

if __name__ == "__main__":
    run_all()
