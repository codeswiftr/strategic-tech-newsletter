"""
Unit tests for research_sources.py

Tests the research functionality including:
- Trending topic fetching from Hacker News
- Expert database updates
- Topic trends CSV management
- Deep research workflow
"""
import pytest
import json
import csv
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from research_sources import (
    fetch_trending_topics,
    research_topic,
    update_expert_database,
    save_trends,
    HACKER_NEWS_API,
    DATA_DIR,
    EXPERT_DB_PATH,
    TRENDS_PATH
)


class TestFetchTrendingTopics:
    """Test fetching trending topics from Hacker News"""

    @patch('research_sources.requests.get')
    def test_fetch_trending_topics_success(self, mock_get, temp_data_dir):
        """Should fetch and parse HN top stories successfully"""
        # Mock the API responses
        mock_topstories_response = Mock()
        mock_topstories_response.json.return_value = [123, 456, 789]

        mock_story_responses = {
            123: {
                'title': 'New AI Framework Released',
                'score': 450,
                'url': 'https://example.com/ai-framework',
                'by': 'techuser'
            },
            456: {
                'title': 'Kubernetes 2.0 Announced',
                'score': 380,
                'url': 'https://example.com/k8s',
                'by': 'devuser'
            },
            789: {
                'title': 'Cloud Cost Optimization',
                'score': 320,
                'url': 'https://example.com/cloud',
                'by': 'cloudexpert'
            }
        }

        def get_side_effect(url, timeout=None):
            if 'topstories' in url:
                return mock_topstories_response
            else:
                # Extract story ID from URL
                story_id = int(url.split('/')[-1].replace('.json', ''))
                mock_response = Mock()
                mock_response.json.return_value = mock_story_responses.get(story_id, {})
                return mock_response

        mock_get.side_effect = get_side_effect

        # Monkey patch the paths
        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.TRENDS_PATH = temp_data_dir / "topic_trends.csv"

        try:
            topics = fetch_trending_topics(days=7)

            # Verify we got topics
            assert len(topics) > 0, "Should return topics"
            assert len(topics) <= 30, "Should limit to top 30 stories"

            # Verify structure
            for topic in topics:
                assert 'topic' in topic, "Should have topic field"
                assert 'source_platform' in topic, "Should have source_platform"
                assert topic['source_platform'] == 'Hacker News'
                assert 'engagement_score' in topic, "Should have engagement_score"
                assert 'url' in topic, "Should have url"
                assert 'date' in topic, "Should have date"

            # Verify specific content
            topic_titles = [t['topic'] for t in topics]
            assert 'New AI Framework Released' in topic_titles
            assert any(t['engagement_score'] == 450 for t in topics)

        finally:
            research_sources.TRENDS_PATH = original_trends_path

    @patch('research_sources.requests.get')
    def test_fetch_trending_topics_api_failure(self, mock_get, temp_data_dir, capsys):
        """Should handle API failures gracefully"""
        mock_get.side_effect = Exception("API connection failed")

        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.TRENDS_PATH = temp_data_dir / "topic_trends.csv"

        try:
            topics = fetch_trending_topics(days=7)

            # Should return empty list on failure
            assert isinstance(topics, list), "Should return list even on failure"

            # Should print error message
            captured = capsys.readouterr()
            assert "Error fetching from Hacker News" in captured.out

        finally:
            research_sources.TRENDS_PATH = original_trends_path

    @patch('research_sources.requests.get')
    def test_fetch_trending_topics_saves_to_csv(self, mock_get, temp_data_dir):
        """Should save fetched topics to CSV file"""
        # Mock minimal response
        mock_topstories_response = Mock()
        mock_topstories_response.json.return_value = [123]

        mock_story_response = Mock()
        mock_story_response.json.return_value = {
            'title': 'Test Story',
            'score': 100,
            'url': 'https://example.com/test',
            'by': 'testuser'
        }

        def get_side_effect(url, timeout=None):
            if 'topstories' in url:
                return mock_topstories_response
            return mock_story_response

        mock_get.side_effect = get_side_effect

        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        trends_csv_path = temp_data_dir / "topic_trends.csv"
        research_sources.TRENDS_PATH = trends_csv_path

        try:
            topics = fetch_trending_topics(days=7)

            # Verify CSV file was created
            assert trends_csv_path.exists(), "Should create CSV file"

            # Verify CSV content
            with open(trends_csv_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                assert len(rows) > 0, "Should have rows in CSV"
                assert rows[0]['topic'] == 'Test Story'
                assert rows[0]['engagement_score'] == '100'

        finally:
            research_sources.TRENDS_PATH = original_trends_path

    @patch('research_sources.requests.get')
    def test_fetch_trending_topics_respects_days_parameter(self, mock_get):
        """Should accept days parameter (note: API doesn't filter, but param should work)"""
        mock_topstories_response = Mock()
        mock_topstories_response.json.return_value = []
        mock_get.return_value = mock_topstories_response

        # Should not raise error with different day values
        fetch_trending_topics(days=3)
        fetch_trending_topics(days=14)
        fetch_trending_topics(days=30)


class TestResearchTopic:
    """Test deep research on specific topics"""

    def test_research_topic_basic_depth(self, capsys):
        """Should handle basic research mode"""
        result = research_topic("AI regulation", depth="basic")

        assert isinstance(result, dict), "Should return dict"
        assert 'topic' in result, "Should include topic"
        assert result['topic'] == "AI regulation"
        assert 'research_date' in result, "Should include research date"
        assert 'sources' in result, "Should include sources list"
        assert 'key_insights' in result, "Should include key insights"

        # Should print TODO message (current implementation)
        captured = capsys.readouterr()
        assert "TODO" in captured.out or "Researching topic" in captured.out

    def test_research_topic_expert_depth(self, capsys):
        """Should handle expert research mode"""
        result = research_topic("Kubernetes at scale", depth="expert")

        assert isinstance(result, dict), "Should return dict"
        assert result['topic'] == "Kubernetes at scale"

        # Verify expected structure
        assert 'sources' in result
        assert 'key_insights' in result

        # Should indicate deeper research
        captured = capsys.readouterr()
        assert "expert" in captured.out.lower() or "depth" in captured.out.lower()

    def test_research_topic_returns_structured_data(self):
        """Should return properly structured research data"""
        result = research_topic("Test Topic", depth="expert")

        # Verify all required fields exist
        required_fields = ['topic', 'research_date', 'sources', 'key_insights']
        for field in required_fields:
            assert field in result, f"Should have {field} field"

        # Verify types
        assert isinstance(result['sources'], list), "Sources should be list"
        assert isinstance(result['key_insights'], list), "Key insights should be list"


class TestUpdateExpertDatabase:
    """Test expert database management"""

    def test_update_expert_database_new_source(self, temp_data_dir):
        """Should add new expert to empty database"""
        db_path = temp_data_dir / "expert_database.json"

        import research_sources
        original_db_path = research_sources.EXPERT_DB_PATH
        research_sources.EXPERT_DB_PATH = db_path

        try:
            new_sources = [
                {
                    'name': 'Dr. Jane Smith',
                    'expertise': ['AI', 'ML'],
                    'twitter_handle': '@janesmith',
                    'email': 'jane@example.com',
                    'credibility_score': 95
                }
            ]

            update_expert_database(new_sources)

            # Verify file created
            assert db_path.exists(), "Should create database file"

            # Verify content
            with open(db_path, 'r') as f:
                db = json.load(f)

            assert 'experts' in db, "Should have experts field"
            assert len(db['experts']) == 1, "Should have 1 expert"
            assert db['experts'][0]['name'] == 'Dr. Jane Smith'

        finally:
            research_sources.EXPERT_DB_PATH = original_db_path

    def test_update_expert_database_avoid_duplicates(self, temp_data_dir, sample_expert_database):
        """Should not add duplicate experts"""
        db_path = temp_data_dir / "expert_database.json"

        # Create existing database
        with open(db_path, 'w') as f:
            json.dump(sample_expert_database, f)

        import research_sources
        original_db_path = research_sources.EXPERT_DB_PATH
        research_sources.EXPERT_DB_PATH = db_path

        try:
            # Try to add expert with same name
            duplicate_source = [
                {
                    'name': 'Dr. Jane Smith',  # Already exists in sample_expert_database
                    'expertise': ['Different'],
                    'twitter_handle': '@different',
                    'email': 'different@example.com',
                    'credibility_score': 80
                }
            ]

            original_count = len(sample_expert_database['experts'])
            update_expert_database(duplicate_source)

            # Verify no duplicate added
            with open(db_path, 'r') as f:
                db = json.load(f)

            assert len(db['experts']) == original_count, "Should not add duplicate"

        finally:
            research_sources.EXPERT_DB_PATH = original_db_path

    def test_update_expert_database_add_to_existing(self, temp_data_dir, sample_expert_database):
        """Should append to existing database"""
        db_path = temp_data_dir / "expert_database.json"

        with open(db_path, 'w') as f:
            json.dump(sample_expert_database, f)

        import research_sources
        original_db_path = research_sources.EXPERT_DB_PATH
        research_sources.EXPERT_DB_PATH = db_path

        try:
            new_source = [
                {
                    'name': 'Dr. Alice Johnson',  # New expert
                    'expertise': ['Blockchain'],
                    'twitter_handle': '@alicejohnson',
                    'email': 'alice@example.com',
                    'credibility_score': 88
                }
            ]

            original_count = len(sample_expert_database['experts'])
            update_expert_database(new_source)

            with open(db_path, 'r') as f:
                db = json.load(f)

            assert len(db['experts']) == original_count + 1, "Should add new expert"
            assert db['experts'][-1]['name'] == 'Dr. Alice Johnson'

        finally:
            research_sources.EXPERT_DB_PATH = original_db_path

    def test_update_expert_database_prints_confirmation(self, temp_data_dir, capsys):
        """Should print confirmation when adding expert"""
        db_path = temp_data_dir / "expert_database.json"

        import research_sources
        original_db_path = research_sources.EXPERT_DB_PATH
        research_sources.EXPERT_DB_PATH = db_path

        try:
            new_source = [{'name': 'Test Expert', 'expertise': []}]
            update_expert_database(new_source)

            captured = capsys.readouterr()
            assert "Test Expert" in captured.out, "Should print expert name"
            assert "Added" in captured.out or "added" in captured.out

        finally:
            research_sources.EXPERT_DB_PATH = original_db_path


class TestSaveTrends:
    """Test saving trends to CSV"""

    def test_save_trends_creates_csv(self, temp_data_dir):
        """Should create new CSV file with trends"""
        trends_path = temp_data_dir / "topic_trends.csv"

        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.TRENDS_PATH = trends_path

        try:
            topics = [
                {
                    'date': '2025-01-20',
                    'topic': 'AI Trends',
                    'source_platform': 'Hacker News',
                    'engagement_score': 500,
                    'url': 'https://example.com/ai'
                }
            ]

            save_trends(topics)

            # Verify file created
            assert trends_path.exists(), "Should create CSV file"

            # Verify content
            with open(trends_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            assert len(rows) == 1, "Should have 1 row"
            assert rows[0]['topic'] == 'AI Trends'
            assert rows[0]['engagement_score'] == '500'

        finally:
            research_sources.TRENDS_PATH = original_trends_path

    def test_save_trends_appends_to_existing(self, temp_data_dir, sample_trends_csv_file):
        """Should append new trends to existing CSV"""
        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.TRENDS_PATH = sample_trends_csv_file

        try:
            # Read original count
            with open(sample_trends_csv_file, 'r') as f:
                original_rows = len(list(csv.DictReader(f)))

            # Add new trends
            new_topics = [
                {
                    'date': '2025-01-21',
                    'topic': 'New Topic',
                    'source_platform': 'Twitter',
                    'engagement_score': 200,
                    'url': 'https://example.com/new'
                }
            ]

            save_trends(new_topics)

            # Verify appended
            with open(sample_trends_csv_file, 'r') as f:
                reader = csv.DictReader(f)
                all_rows = list(reader)

            assert len(all_rows) == original_rows + 1, "Should append new row"
            assert all_rows[-1]['topic'] == 'New Topic'

        finally:
            research_sources.TRENDS_PATH = original_trends_path

    def test_save_trends_handles_empty_list(self, temp_data_dir):
        """Should handle empty topic list gracefully"""
        trends_path = temp_data_dir / "topic_trends.csv"

        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.TRENDS_PATH = trends_path

        try:
            save_trends([])

            # Should not create file for empty list
            # Or create file with just headers
            # Implementation may vary, just ensure no error

        finally:
            research_sources.TRENDS_PATH = original_trends_path

    def test_save_trends_preserves_existing_data(self, temp_data_dir):
        """Should not lose existing data when appending"""
        trends_path = temp_data_dir / "topic_trends.csv"

        import research_sources
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.TRENDS_PATH = trends_path

        try:
            # Create initial trends
            initial_topics = [
                {
                    'date': '2025-01-20',
                    'topic': 'Initial Topic',
                    'source_platform': 'HN',
                    'engagement_score': 100,
                    'url': 'https://example.com/1'
                }
            ]
            save_trends(initial_topics)

            # Append new trends
            new_topics = [
                {
                    'date': '2025-01-21',
                    'topic': 'Second Topic',
                    'source_platform': 'Twitter',
                    'engagement_score': 200,
                    'url': 'https://example.com/2'
                }
            ]
            save_trends(new_topics)

            # Verify both exist
            with open(trends_path, 'r') as f:
                reader = csv.DictReader(f)
                all_rows = list(reader)

            assert len(all_rows) == 2, "Should have both topics"
            topics_list = [row['topic'] for row in all_rows]
            assert 'Initial Topic' in topics_list
            assert 'Second Topic' in topics_list

        finally:
            research_sources.TRENDS_PATH = original_trends_path


@pytest.mark.integration
class TestResearchSourcesIntegration:
    """Integration tests for research workflow"""

    @patch('research_sources.requests.get')
    def test_full_research_workflow(self, mock_get, temp_data_dir):
        """Test complete workflow: fetch trends → update DB"""
        # Setup temporary paths
        db_path = temp_data_dir / "expert_database.json"
        trends_path = temp_data_dir / "topic_trends.csv"

        import research_sources
        original_db_path = research_sources.EXPERT_DB_PATH
        original_trends_path = research_sources.TRENDS_PATH
        research_sources.EXPERT_DB_PATH = db_path
        research_sources.TRENDS_PATH = trends_path

        try:
            # Mock HN API
            mock_topstories = Mock()
            mock_topstories.json.return_value = [123]

            mock_story = Mock()
            mock_story.json.return_value = {
                'title': 'Integration Test Story',
                'score': 500,
                'by': 'testuser'
            }

            def get_side_effect(url, timeout=None):
                if 'topstories' in url:
                    return mock_topstories
                return mock_story

            mock_get.side_effect = get_side_effect

            # Step 1: Fetch trending topics
            topics = fetch_trending_topics(days=7)
            assert len(topics) > 0, "Should fetch topics"

            # Step 2: Verify trends saved to CSV
            assert trends_path.exists(), "Should create trends CSV"

            # Step 3: Update expert database (manual for now)
            new_expert = [{
                'name': 'Integration Test Expert',
                'expertise': ['Testing'],
                'credibility_score': 90
            }]
            update_expert_database(new_expert)

            # Step 4: Verify expert DB created
            assert db_path.exists(), "Should create expert database"

            with open(db_path, 'r') as f:
                db = json.load(f)
            assert len(db['experts']) == 1

        finally:
            research_sources.EXPERT_DB_PATH = original_db_path
            research_sources.TRENDS_PATH = original_trends_path
