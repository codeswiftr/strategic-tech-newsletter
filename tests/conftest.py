"""
Shared pytest fixtures for Strategic Tech Newsletter tests
"""
import pytest
from pathlib import Path
import json
import tempfile
import csv
from datetime import datetime


@pytest.fixture
def temp_data_dir():
    """Create temporary data directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_expert_database():
    """Sample expert database for testing"""
    return {
        "experts": [
            {
                "name": "Dr. Jane Smith",
                "expertise": ["AI", "Machine Learning"],
                "twitter_handle": "@janesmith",
                "email": "jane@example.com",
                "affiliation": "MIT AI Lab",
                "last_contacted": "2025-01-01",
                "topics": ["Neural networks", "Deep learning"],
                "credibility_score": 95,
                "notes": "Leading researcher in AI safety"
            },
            {
                "name": "John Doe",
                "expertise": ["DevOps", "Cloud Infrastructure"],
                "twitter_handle": "@johndoe",
                "email": "john@example.com",
                "affiliation": "Google Cloud",
                "last_contacted": "2024-12-15",
                "topics": ["Kubernetes", "Terraform"],
                "credibility_score": 88,
                "notes": "Author of popular DevOps blog"
            }
        ],
        "last_updated": "2025-01-20",
        "total_experts": 2
    }


@pytest.fixture
def sample_essay_content():
    """Sample essay markdown for testing"""
    return """# The Future of AI Regulation

The AI industry is experiencing 45% year-over-year growth according to [McKinsey 2024](https://example.com/mckinsey-report).

## Current Landscape

Recent studies show that:
- Regulation frameworks are emerging across 12 countries
- Investment reached $50,000,000 in Q4 2024
- Major tech companies are adopting self-regulation protocols

According to [Gartner's 2024 report](https://gartner.com/report), 67% of enterprises have implemented AI governance.

## Key Insights

The regulatory environment is evolving rapidly. Industry experts predict that 80% of jurisdictions will have AI-specific laws by 2026.

## Conclusion

This is a pivotal moment for the industry. Organizations must prepare for increased compliance requirements.
"""


@pytest.fixture
def sample_essay_file(temp_data_dir, sample_essay_content):
    """Create a sample essay file for testing"""
    essay_path = temp_data_dir / "sample_essay.md"
    essay_path.write_text(sample_essay_content)
    return essay_path


@pytest.fixture
def sample_fact_check_library():
    """Sample fact-check library with verified claims"""
    return {
        "verified_claims": [
            {
                "claim": "AI industry is experiencing 45% year-over-year growth",
                "source_url": "https://example.com/mckinsey-report",
                "verification_date": "2024-12-15",
                "context": "Based on McKinsey's annual AI report 2024",
                "confidence": 0.95,
                "category": "AI/ML"
            },
            {
                "claim": "67% of enterprises have implemented AI governance",
                "source_url": "https://gartner.com/report",
                "verification_date": "2025-01-10",
                "context": "Gartner survey of 500+ enterprises",
                "confidence": 0.92,
                "category": "AI Governance"
            }
        ],
        "last_updated": "2025-01-20",
        "total_verified_claims": 2
    }


@pytest.fixture
def sample_topic_trends():
    """Sample topic trends data"""
    return [
        {
            "date": "2025-01-20",
            "topic": "AI Regulation in the EU: What Tech Leaders Need to Know",
            "source_platform": "Hacker News",
            "engagement_score": 342,
            "url": "https://news.ycombinator.com/item?id=12345678"
        },
        {
            "date": "2025-01-19",
            "topic": "The Rise of Rust in Production Systems",
            "source_platform": "Hacker News",
            "engagement_score": 287,
            "url": "https://news.ycombinator.com/item?id=12345679"
        },
        {
            "date": "2025-01-19",
            "topic": "Why Platform Engineering is Replacing DevOps",
            "source_platform": "Twitter",
            "engagement_score": 156,
            "url": "https://twitter.com/example/status/1234567890"
        }
    ]


@pytest.fixture
def mock_hacker_news_response():
    """Mock HN API response for testing"""
    return {
        "topstories": [123, 456, 789],
        "items": {
            123: {
                "by": "techuser",
                "descendants": 45,
                "id": 123,
                "score": 450,
                "time": 1704067200,
                "title": "New AI Framework Released",
                "type": "story",
                "url": "https://example.com/ai-framework"
            },
            456: {
                "by": "devuser",
                "descendants": 32,
                "id": 456,
                "score": 380,
                "time": 1704063600,
                "title": "Kubernetes 2.0 Announced",
                "type": "story",
                "url": "https://example.com/k8s-2"
            },
            789: {
                "by": "cloudexpert",
                "descendants": 28,
                "id": 789,
                "score": 320,
                "time": 1704060000,
                "title": "Cloud Cost Optimization Guide",
                "type": "story",
                "url": "https://example.com/cloud-costs"
            }
        }
    }


@pytest.fixture
def sample_expert_database_file(temp_data_dir, sample_expert_database):
    """Create sample expert database JSON file"""
    db_path = temp_data_dir / "expert_database.json"
    with open(db_path, 'w') as f:
        json.dump(sample_expert_database, f, indent=2)
    return db_path


@pytest.fixture
def sample_trends_csv_file(temp_data_dir, sample_topic_trends):
    """Create sample trends CSV file"""
    csv_path = temp_data_dir / "topic_trends.csv"

    with open(csv_path, 'w', newline='') as f:
        fieldnames = ['date', 'topic', 'source_platform', 'engagement_score', 'url']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for trend in sample_topic_trends:
            writer.writerow(trend)

    return csv_path


@pytest.fixture
def sample_fact_check_library_file(temp_data_dir, sample_fact_check_library):
    """Create sample fact-check library JSON file"""
    lib_path = temp_data_dir / "fact_check_library.json"
    with open(lib_path, 'w') as f:
        json.dump(sample_fact_check_library, f, indent=2)
    return lib_path


@pytest.fixture(autouse=True)
def reset_environment(monkeypatch):
    """Reset environment variables for each test"""
    # Clear any API keys that might be set
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TWITTER_API_KEY", raising=False)
    monkeypatch.delenv("SUBSTACK_API_TOKEN", raising=False)
    yield
