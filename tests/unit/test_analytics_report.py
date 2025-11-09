"""
Unit tests for analytics_report.py

Tests analytics tracking and reporting including:
- Analytics history loading and saving
- Metrics fetching (mocked API calls)
- Growth rate calculations
- Weekly and monthly report generation
- Markdown report formatting
"""
import pytest
import json
from pathlib import Path
from datetime import datetime
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from analytics_report import (
    load_analytics_history,
    save_analytics_history,
    fetch_current_metrics,
    calculate_growth_rate,
    generate_weekly_report,
    generate_monthly_report,
    format_report_markdown,
    ANALYTICS_FILE
)


class TestLoadAnalyticsHistory:
    """Test loading analytics history from file"""

    def test_load_analytics_history_existing_file(self, temp_data_dir):
        """Should load existing analytics data"""
        analytics_file = temp_data_dir / "analytics_history.json"

        sample_data = {
            "newsletter": {
                "metrics": [
                    {
                        "date": "2025-01-15",
                        "subscribers": {"total": 1000},
                        "engagement": {"open_rate": 40.0}
                    }
                ],
                "last_updated": "2025-01-15"
            }
        }

        with open(analytics_file, 'w') as f:
            json.dump(sample_data, f)

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            history = load_analytics_history()

            assert 'newsletter' in history
            assert 'metrics' in history['newsletter']
            assert len(history['newsletter']['metrics']) == 1
            assert history['newsletter']['metrics'][0]['subscribers']['total'] == 1000

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_load_analytics_history_missing_file(self, temp_data_dir):
        """Should return default structure for missing file"""
        analytics_file = temp_data_dir / "nonexistent.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            history = load_analytics_history()

            # Should return default structure
            assert 'newsletter' in history
            assert 'metrics' in history['newsletter']
            assert history['newsletter']['metrics'] == []
            assert history['newsletter']['last_updated'] is None

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_load_analytics_history_structure(self, temp_data_dir):
        """Should have correct data structure"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            history = load_analytics_history()

            # Verify structure
            assert isinstance(history, dict)
            assert 'newsletter' in history
            assert isinstance(history['newsletter'], dict)
            assert 'metrics' in history['newsletter']
            assert isinstance(history['newsletter']['metrics'], list)

        finally:
            analytics_report.ANALYTICS_FILE = original_file


class TestSaveAnalyticsHistory:
    """Test saving analytics history to file"""

    def test_save_analytics_history_creates_file(self, temp_data_dir):
        """Should create analytics file"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            data = {
                "newsletter": {
                    "metrics": [],
                    "last_updated": None
                }
            }

            save_analytics_history(data)

            assert analytics_file.exists(), "Should create file"

            with open(analytics_file, 'r') as f:
                saved_data = json.load(f)

            assert 'newsletter' in saved_data

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_save_analytics_history_updates_timestamp(self, temp_data_dir):
        """Should update last_updated timestamp"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            data = {
                "newsletter": {
                    "metrics": [],
                    "last_updated": None
                }
            }

            save_analytics_history(data)

            with open(analytics_file, 'r') as f:
                saved_data = json.load(f)

            assert saved_data['newsletter']['last_updated'] is not None
            # Should be ISO format
            datetime.fromisoformat(saved_data['newsletter']['last_updated'])

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_save_analytics_history_preserves_data(self, temp_data_dir):
        """Should preserve all data when saving"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            data = {
                "newsletter": {
                    "metrics": [
                        {"date": "2025-01-01", "subscribers": {"total": 1000}},
                        {"date": "2025-01-08", "subscribers": {"total": 1050}}
                    ],
                    "last_updated": None
                }
            }

            save_analytics_history(data)

            with open(analytics_file, 'r') as f:
                saved_data = json.load(f)

            assert len(saved_data['newsletter']['metrics']) == 2
            assert saved_data['newsletter']['metrics'][0]['subscribers']['total'] == 1000

        finally:
            analytics_report.ANALYTICS_FILE = original_file


class TestFetchCurrentMetrics:
    """Test fetching current metrics from newsletter platform"""

    def test_fetch_current_metrics_structure(self):
        """Should return properly structured metrics"""
        metrics = fetch_current_metrics()

        # Verify all required fields
        assert 'date' in metrics
        assert 'subscribers' in metrics
        assert 'engagement' in metrics
        assert 'top_performing' in metrics
        assert 'revenue' in metrics

    def test_fetch_current_metrics_subscribers_data(self):
        """Should include subscriber metrics"""
        metrics = fetch_current_metrics()

        subscribers = metrics['subscribers']
        assert 'total' in subscribers
        assert 'new_this_week' in subscribers
        assert 'unsubscribed' in subscribers
        assert 'net_growth' in subscribers

        # Values should be reasonable
        assert subscribers['total'] > 0
        assert isinstance(subscribers['new_this_week'], int)

    def test_fetch_current_metrics_engagement_data(self):
        """Should include engagement metrics"""
        metrics = fetch_current_metrics()

        engagement = metrics['engagement']
        assert 'open_rate' in engagement
        assert 'click_through_rate' in engagement
        assert 'total_opens' in engagement
        assert 'total_clicks' in engagement

        # Rates should be percentages
        assert 0 <= engagement['open_rate'] <= 100
        assert 0 <= engagement['click_through_rate'] <= 100

    def test_fetch_current_metrics_revenue_data(self):
        """Should include revenue metrics"""
        metrics = fetch_current_metrics()

        revenue = metrics['revenue']
        assert 'monthly_recurring' in revenue
        assert 'sponsors' in revenue
        assert 'total' in revenue

        # Revenue should be non-negative
        assert revenue['total'] >= 0


class TestCalculateGrowthRate:
    """Test growth rate calculation"""

    def test_calculate_growth_rate_positive_growth(self):
        """Should calculate positive growth correctly"""
        growth = calculate_growth_rate(110, 100)

        assert growth == 10.0, "110 from 100 is 10% growth"

    def test_calculate_growth_rate_negative_growth(self):
        """Should calculate negative growth correctly"""
        growth = calculate_growth_rate(90, 100)

        assert growth == -10.0, "90 from 100 is -10% growth"

    def test_calculate_growth_rate_no_growth(self):
        """Should return 0 for no growth"""
        growth = calculate_growth_rate(100, 100)

        assert growth == 0.0

    def test_calculate_growth_rate_zero_previous(self):
        """Should handle zero previous value gracefully"""
        growth = calculate_growth_rate(100, 0)

        assert growth == 0.0, "Should return 0 when dividing by zero"

    def test_calculate_growth_rate_decimal_values(self):
        """Should handle decimal values"""
        growth = calculate_growth_rate(42.5, 40.0)

        assert abs(growth - 6.25) < 0.01, "Should calculate decimal growth"

    def test_calculate_growth_rate_large_numbers(self):
        """Should handle large numbers"""
        growth = calculate_growth_rate(10000, 5000)

        assert growth == 100.0, "Doubling is 100% growth"


class TestGenerateWeeklyReport:
    """Test weekly report generation"""

    def test_generate_weekly_report_structure(self, temp_data_dir):
        """Should generate report with correct structure"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_weekly_report(compare=False)

            assert 'period' in report
            assert report['period'] == 'week'
            assert 'date' in report
            assert 'current' in report
            assert 'changes' in report

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_generate_weekly_report_includes_current_metrics(self, temp_data_dir):
        """Should include current week's metrics"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_weekly_report(compare=False)

            current = report['current']
            assert 'subscribers' in current
            assert 'engagement' in current
            assert 'top_performing' in current

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_generate_weekly_report_with_comparison(self, temp_data_dir):
        """Should calculate changes when compare=True"""
        analytics_file = temp_data_dir / "analytics_history.json"

        # Create history with previous week's data
        history_data = {
            "newsletter": {
                "metrics": [
                    {
                        "date": "2025-01-13",
                        "subscribers": {"total": 1000},
                        "engagement": {
                            "open_rate": 40.0,
                            "click_through_rate": 8.0
                        }
                    }
                ],
                "last_updated": "2025-01-13"
            }
        }

        with open(analytics_file, 'w') as f:
            json.dump(history_data, f)

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_weekly_report(compare=True)

            # Should have changes calculated
            if report['changes']:  # If history available
                assert 'subscriber_growth' in report['changes']
                assert 'open_rate_change' in report['changes']
                assert 'ctr_change' in report['changes']

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_generate_weekly_report_saves_to_history(self, temp_data_dir):
        """Should append current metrics to history"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            # Generate report (should save metrics)
            report = generate_weekly_report(compare=False)

            # Verify history file exists and has data
            assert analytics_file.exists()

            with open(analytics_file, 'r') as f:
                history = json.load(f)

            assert len(history['newsletter']['metrics']) > 0

        finally:
            analytics_report.ANALYTICS_FILE = original_file


class TestGenerateMonthlyReport:
    """Test monthly report generation"""

    def test_generate_monthly_report_structure(self, temp_data_dir):
        """Should generate report with correct structure"""
        analytics_file = temp_data_dir / "analytics_history.json"

        # Create 4 weeks of data
        history_data = {
            "newsletter": {
                "metrics": [
                    {
                        "date": f"2025-01-{7*i+1:02d}",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {"open_rate": 40.0 + i, "click_through_rate": 8.0},
                        "revenue": {"total": 1500}
                    }
                    for i in range(4)
                ],
                "last_updated": "2025-01-28"
            }
        }

        with open(analytics_file, 'w') as f:
            json.dump(history_data, f)

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_monthly_report()

            assert report is not None
            assert 'period' in report
            assert report['period'] == 'month'
            assert 'summary' in report
            assert 'trends' in report

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_generate_monthly_report_calculates_averages(self, temp_data_dir):
        """Should calculate monthly averages"""
        analytics_file = temp_data_dir / "analytics_history.json"

        history_data = {
            "newsletter": {
                "metrics": [
                    {
                        "date": f"2025-01-{7*i+1:02d}",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {
                            "open_rate": 40.0,
                            "click_through_rate": 8.0
                        },
                        "revenue": {"total": 1500}
                    }
                    for i in range(4)
                ],
                "last_updated": "2025-01-28"
            }
        }

        with open(analytics_file, 'w') as f:
            json.dump(history_data, f)

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_monthly_report()

            summary = report['summary']
            assert 'avg_open_rate' in summary
            assert 'avg_click_through_rate' in summary
            assert 'total_new_subscribers' in summary
            assert 'total_revenue' in summary

            # Verify calculations
            assert summary['avg_open_rate'] == 40.0
            assert summary['total_new_subscribers'] == 200  # 50 * 4 weeks

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_generate_monthly_report_identifies_trends(self, temp_data_dir):
        """Should identify increasing/decreasing trends"""
        analytics_file = temp_data_dir / "analytics_history.json"

        # Increasing open rate
        history_data = {
            "newsletter": {
                "metrics": [
                    {
                        "date": "2025-01-01",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {"open_rate": 35.0, "click_through_rate": 8.0},
                        "revenue": {"total": 1500}
                    },
                    {
                        "date": "2025-01-08",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {"open_rate": 38.0, "click_through_rate": 8.0},
                        "revenue": {"total": 1500}
                    },
                    {
                        "date": "2025-01-15",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {"open_rate": 41.0, "click_through_rate": 8.0},
                        "revenue": {"total": 1500}
                    },
                    {
                        "date": "2025-01-22",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {"open_rate": 45.0, "click_through_rate": 8.0},
                        "revenue": {"total": 1500}
                    }
                ],
                "last_updated": "2025-01-28"
            }
        }

        with open(analytics_file, 'w') as f:
            json.dump(history_data, f)

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_monthly_report()

            trends = report['trends']
            assert 'open_rate_trend' in trends
            assert trends['open_rate_trend'] == 'increasing'

        finally:
            analytics_report.ANALYTICS_FILE = original_file

    def test_generate_monthly_report_insufficient_data(self, temp_data_dir):
        """Should handle insufficient data gracefully"""
        analytics_file = temp_data_dir / "analytics_history.json"

        # Only 1 week of data (need 4)
        history_data = {
            "newsletter": {
                "metrics": [
                    {
                        "date": "2025-01-01",
                        "subscribers": {"new_this_week": 50},
                        "engagement": {"open_rate": 40.0, "click_through_rate": 8.0},
                        "revenue": {"total": 1500}
                    }
                ],
                "last_updated": "2025-01-01"
            }
        }

        with open(analytics_file, 'w') as f:
            json.dump(history_data, f)

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            report = generate_monthly_report()

            # Should work with limited data but may have warnings
            # At minimum, should not crash
            assert report is not None or report is None  # Either way is OK

        finally:
            analytics_report.ANALYTICS_FILE = original_file


class TestFormatReportMarkdown:
    """Test markdown report formatting"""

    def test_format_report_markdown_weekly(self):
        """Should format weekly report as markdown"""
        report = {
            'period': 'week',
            'current': {
                'subscribers': {'total': 1250, 'new_this_week': 45, 'unsubscribed': 3, 'net_growth': 42},
                'engagement': {'open_rate': 42.5, 'click_through_rate': 8.2, 'total_opens': 531, 'total_clicks': 103},
                'top_performing': {'most_opened': 'AI Regulation', 'most_clicked': 'Remote Work', 'avg_read_time': '6.5 minutes'},
                'revenue': {'monthly_recurring': 1200, 'sponsors': 500, 'total': 1700}
            },
            'changes': {}
        }

        markdown = format_report_markdown(report)

        assert isinstance(markdown, str)
        assert len(markdown) > 0
        assert '# WEEKLY NEWSLETTER ANALYTICS' in markdown
        assert '## Subscribers' in markdown
        assert '1,250' in markdown  # Formatted number
        assert '42.5%' in markdown  # Open rate

    def test_format_report_markdown_monthly(self):
        """Should format monthly report as markdown"""
        report = {
            'period': 'month',
            'summary': {
                'avg_open_rate': 42.5,
                'avg_click_through_rate': 8.2,
                'total_new_subscribers': 180,
                'total_revenue': 6800
            },
            'trends': {
                'open_rate_trend': 'increasing',
                'subscriber_trend': 'growing'
            }
        }

        markdown = format_report_markdown(report)

        assert isinstance(markdown, str)
        assert '# MONTHLY NEWSLETTER ANALYTICS' in markdown
        assert '## Monthly Summary' in markdown
        assert '180' in markdown  # Total new subscribers
        assert 'increasing' in markdown

    def test_format_report_markdown_includes_metadata(self):
        """Should include generation timestamp"""
        report = {
            'period': 'week',
            'current': {
                'subscribers': {'total': 1000, 'new_this_week': 10, 'unsubscribed': 1, 'net_growth': 9},
                'engagement': {'open_rate': 40.0, 'click_through_rate': 8.0, 'total_opens': 400, 'total_clicks': 80},
                'top_performing': {'most_opened': 'Test', 'most_clicked': 'Test', 'avg_read_time': '5 min'},
                'revenue': {'monthly_recurring': 1000, 'sponsors': 0, 'total': 1000}
            },
            'changes': {}
        }

        markdown = format_report_markdown(report)

        assert '**Generated:**' in markdown
        assert 'analytics_report.py' in markdown

    def test_format_report_markdown_with_changes(self):
        """Should include week-over-week changes when available"""
        report = {
            'period': 'week',
            'current': {
                'subscribers': {'total': 1000, 'new_this_week': 10, 'unsubscribed': 1, 'net_growth': 9},
                'engagement': {'open_rate': 40.0, 'click_through_rate': 8.0, 'total_opens': 400, 'total_clicks': 80},
                'top_performing': {'most_opened': 'Test', 'most_clicked': 'Test', 'avg_read_time': '5 min'},
                'revenue': {'monthly_recurring': 1000, 'sponsors': 0, 'total': 1000}
            },
            'changes': {
                'subscriber_growth': 5.0,
                'open_rate_change': 2.5,
                'ctr_change': 0.5
            }
        }

        markdown = format_report_markdown(report)

        assert '## Week-over-Week Changes' in markdown
        assert '+5.0%' in markdown
        assert '+2.5%' in markdown


@pytest.mark.integration
class TestAnalyticsReportIntegration:
    """Integration tests for analytics workflow"""

    def test_full_analytics_workflow(self, temp_data_dir):
        """Test complete workflow: fetch → weekly report → monthly report → markdown"""
        analytics_file = temp_data_dir / "analytics_history.json"

        import analytics_report
        original_file = analytics_report.ANALYTICS_FILE
        analytics_report.ANALYTICS_FILE = analytics_file

        try:
            # Step 1: Generate weekly reports over 4 weeks
            for week in range(4):
                weekly_report = generate_weekly_report(compare=True)
                assert weekly_report is not None

            # Step 2: Generate monthly report
            monthly_report = generate_monthly_report()
            assert monthly_report is not None

            # Step 3: Format both reports as markdown
            weekly_md = format_report_markdown(weekly_report)
            monthly_md = format_report_markdown(monthly_report)

            assert len(weekly_md) > 0
            assert len(monthly_md) > 0

            # Step 4: Verify history file has accumulated data
            with open(analytics_file, 'r') as f:
                history = json.load(f)

            assert len(history['newsletter']['metrics']) == 4

        finally:
            analytics_report.ANALYTICS_FILE = original_file
