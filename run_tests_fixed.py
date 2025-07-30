#!/usr/bin/env python3
"""
Fixed Test Runner for Chat with DB
This script fixes the GitHub Issues by properly setting up the environment before running tests.
"""

import os
import sys
import subprocess

def setup_environment():
    """Set up the test environment"""
    # Set environment variables
    os.environ['DATABASE_PATH'] = '/workspace/test_data/test.db'
    os.environ['LLM_PROVIDER_TYPE'] = 'ollama'
    os.environ['LLM_API_KEY'] = 'test_key'
    os.environ['LLM_MODEL'] = 'llama3.2:3b'
    os.environ['LLM_BASE_URL'] = 'http://localhost:11434'
    
    # Add local bin to PATH
    current_path = os.environ.get('PATH', '')
    local_bin = '/home/ubuntu/.local/bin'
    if local_bin not in current_path:
        os.environ['PATH'] = f"{current_path}:{local_bin}"

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Failed: {description}")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False
    
    print()
    return True

def main():
    """Main test runner"""
    print("🧪 Fixed Test Runner for Chat with DB")
    print("============================================================")
    print("This fixes the GitHub Issues by properly setting up the environment")
    print()
    
    # Setup environment
    setup_environment()
    
    # Ensure test database exists
    os.makedirs('/workspace/test_data', exist_ok=True)
    if not os.path.exists('/workspace/test_data/test.db'):
        open('/workspace/test_data/test.db', 'a').close()
    
    # Run tests
    success = True
    
    # Unit tests
    success &= run_command(
        ['pytest', 'tests/unit/', '-v', '--tb=short'],
        "Running unit tests"
    )
    
    # Integration tests
    success &= run_command(
        ['pytest', 'tests/integration/', '-v', '--tb=short'],
        "Running integration tests"
    )
    
    # E2E tests
    success &= run_command(
        ['pytest', 'tests/e2e/', '-v', '--tb=short'],
        "Running e2e tests"
    )
    
    # Summary
    print("============================================================")
    if success:
        print("✅ All tests passed! The GitHub Issues have been fixed.")
        print("🎉 Development environment is properly configured.")
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
