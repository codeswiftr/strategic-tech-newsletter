#!/usr/bin/env python3
"""
Validate Strategic Tech Newsletter environment setup

Checks:
- Python version
- Required dependencies installed
- Environment variables configured
- Data directories exist
- API connectivity
- Claude Code skills available
"""

import sys
import os
from pathlib import Path
import importlib.util

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_check(name, status, details=""):
    """Print check result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   {details}")

def check_python_version():
    """Check Python version is 3.11+"""
    print_header("Python Version")

    version = sys.version_info
    is_valid = version.major == 3 and version.minor >= 11

    print_check(
        "Python 3.11+",
        is_valid,
        f"Current: Python {version.major}.{version.minor}.{version.micro}"
    )

    return is_valid

def check_dependencies():
    """Check required packages are installed"""
    print_header("Dependencies")

    required_packages = {
        'requests': 'HTTP library for API calls',
        'bs4': 'BeautifulSoup for web scraping',
        'feedparser': 'RSS feed parsing',
        'pandas': 'Data analysis',
        'dotenv': 'Environment variable loading'
    }

    optional_packages = {
        'pytest': 'Testing framework',
        'black': 'Code formatter',
        'ruff': 'Linter'
    }

    all_good = True

    print("Required Packages:")
    for package, description in required_packages.items():
        try:
            # Try alternative import names
            import_name = 'beautifulsoup4' if package == 'bs4' else package
            import_name = 'python-dotenv' if package == 'dotenv' else import_name

            spec = importlib.util.find_spec(package)
            is_installed = spec is not None

            print_check(f"{package:20s} - {description}", is_installed)

            if not is_installed:
                all_good = False
        except Exception:
            print_check(f"{package:20s} - {description}", False)
            all_good = False

    print("\nOptional Packages:")
    for package, description in optional_packages.items():
        try:
            spec = importlib.util.find_spec(package)
            is_installed = spec is not None
            print_check(f"{package:20s} - {description}", is_installed)
        except Exception:
            print_check(f"{package:20s} - {description}", False)

    return all_good

def check_environment_variables():
    """Check environment variables configured"""
    print_header("Environment Variables")

    # Check if .env.local exists
    env_file = Path('.env.local')
    env_exists = env_file.exists()

    print_check(".env.local file", env_exists, "Contains API keys and secrets")

    if env_exists:
        # Try to load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv('.env.local')

            # Check for key variables
            env_vars = {
                'SUBSTACK_API_TOKEN': 'Optional - Substack analytics',
                'GHOST_API_KEY': 'Optional - Ghost analytics',
                'TWITTER_BEARER_TOKEN': 'Optional - Twitter trends',
                'SERPAPI_KEY': 'Optional - Google Scholar search',
                'HUNTER_API_KEY': 'Optional - Email finding',
                'OPENAI_API_KEY': 'Optional - Content analysis'
            }

            configured_count = 0
            for var, description in env_vars.items():
                is_set = bool(os.getenv(var))
                if is_set:
                    configured_count += 1
                    # Don't show full value, just first/last chars
                    value = os.getenv(var)
                    masked = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                    print_check(f"{var:25s}", True, f"{description} ({masked})")
                else:
                    print_check(f"{var:25s}", False, f"{description} (not set)")

            print(f"\n   {configured_count}/{len(env_vars)} optional API keys configured")

        except ImportError:
            print_check("python-dotenv", False, "Cannot load environment variables")
            return False
    else:
        print("   ⚠️ .env.local not found. Copy .env.example to .env.local and add API keys.")

    return True  # Environment vars are optional

def check_data_directories():
    """Check data directories and files exist"""
    print_header("Data Directory Structure")

    base_dir = Path('.')
    required_dirs = [
        'data',
        'content/essays',
        'content/drafts',
        'content/social_posts',
        'scripts',
        'tests',
        '.claude/skills'
    ]

    all_exist = True
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        exists = full_path.exists() and full_path.is_dir()
        print_check(dir_path, exists)
        if not exists:
            all_exist = False

    # Check for key data files
    print("\nData Files:")
    data_files = [
        ('data/expert_database.json', 'Expert CRM database'),
        ('data/topic_trends.csv', 'Trending topics history'),
        ('data/fact_check_library.json', 'Verified claims library')
    ]

    for file_path, description in data_files:
        full_path = base_dir / file_path
        exists = full_path.exists()
        print_check(f"{file_path:30s}", exists, description)

    return all_exist

def check_claude_skills():
    """Check Claude Code skills are available"""
    print_header("Claude Code Skills")

    skills_dir = Path('.claude/skills')

    if not skills_dir.exists():
        print_check("Skills directory", False, ".claude/skills not found")
        return False

    required_skills = [
        ('research', 'Automated research and expert sourcing'),
        ('fact_checker', 'Claim verification and citation'),
        ('social_repurpose', 'Social media content generation')
    ]

    all_exist = True
    for skill_name, description in required_skills:
        skill_path = skills_dir / skill_name / 'SKILL.md'
        exists = skill_path.exists()
        print_check(f"{skill_name:20s}", exists, description)
        if not exists:
            all_exist = False

    # Check settings.json
    settings_path = Path('.claude/settings.json')
    settings_exist = settings_path.exists()
    print_check("settings.json", settings_exist, "Claude Code configuration")

    return all_exist and settings_exist

def check_api_connectivity():
    """Check API connectivity (basic tests)"""
    print_header("API Connectivity")

    # Test Hacker News API (no auth required)
    try:
        import requests
        response = requests.get(
            'https://hacker-news.firebaseio.com/v0/topstories.json',
            timeout=5
        )
        hn_works = response.status_code == 200
        print_check(
            "Hacker News API",
            hn_works,
            f"Status: {response.status_code}" if hn_works else "Connection failed"
        )
    except Exception as e:
        print_check("Hacker News API", False, f"Error: {str(e)}")
        hn_works = False

    # Note: Other APIs require authentication, tested separately
    print("\n   ℹ️ Other APIs (Twitter, SerpAPI, etc.) require authentication.")
    print("   ℹ️ Configure API keys in .env.local to enable.")

    return hn_works

def check_tests():
    """Check if tests can run"""
    print_header("Test Suite")

    # Check pytest installed
    try:
        import pytest
        pytest_installed = True
        print_check("pytest installed", True)
    except ImportError:
        print_check("pytest installed", False, "Install with: uv pip install -e \".[dev]\"")
        return False

    # Check if tests exist
    tests_dir = Path('tests')
    if not tests_dir.exists():
        print_check("tests/ directory", False)
        return False

    # Count test files
    test_files = list(tests_dir.glob('***/test_*.py'))
    test_count = len(test_files)

    print_check(
        f"{test_count} test files found",
        test_count > 0,
        f"Run with: pytest tests/ -v"
    )

    return test_count > 0

def print_summary(checks):
    """Print overall summary"""
    print_header("Summary")

    total = len(checks)
    passed = sum(1 for check in checks.values() if check)

    percentage = (passed / total * 100) if total > 0 else 0

    print(f"   Checks passed: {passed}/{total} ({percentage:.0f}%)\n")

    if passed == total:
        print("   ✅ Environment setup is complete!")
        print("   ✅ Ready to use Strategic Tech Newsletter automation")
        print("\n   Next steps:")
        print("   1. Run: python scripts/research_sources.py --mode=trending")
        print("   2. Read: docs/WORKFLOWS.md for weekly routines")
        print("   3. Test: pytest tests/ -v\n")
    else:
        print("   ⚠️ Some checks failed. Please review issues above.")
        print("\n   Common fixes:")
        print("   - Install dependencies: uv pip install -e \".[dev]\"")
        print("   - Create .env.local: cp .env.example .env.local")
        print("   - Review setup guide: docs/SETUP_GUIDE.md\n")

def main():
    """Run all validation checks"""
    print("\n" + "="*60)
    print("  🔍 Strategic Tech Newsletter - Setup Validation")
    print("="*60)

    checks = {
        'Python Version': check_python_version(),
        'Dependencies': check_dependencies(),
        'Environment Variables': check_environment_variables(),
        'Data Directories': check_data_directories(),
        'Claude Skills': check_claude_skills(),
        'API Connectivity': check_api_connectivity(),
        'Test Suite': check_tests()
    }

    print_summary(checks)

    # Return exit code
    return 0 if all(checks.values()) else 1

if __name__ == '__main__':
    sys.exit(main())
