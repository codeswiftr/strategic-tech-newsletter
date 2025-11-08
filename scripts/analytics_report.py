#!/usr/bin/env python3
"""
analytics_report.py - Weekly metrics and insights for newsletter performance

Usage:
    python analytics_report.py --period=week --output=markdown
    python analytics_report.py --period=month --compare=true
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
ANALYTICS_FILE = DATA_DIR / "analytics_history.json"


def load_analytics_history():
    """
    Load historical analytics data

    Returns:
        dict: Analytics history
    """
    if ANALYTICS_FILE.exists():
        with open(ANALYTICS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {
            'newsletter': {
                'metrics': [],
                'last_updated': None
            }
        }


def save_analytics_history(data):
    """
    Save analytics history to file

    Args:
        data (dict): Analytics data to save
    """
    data['newsletter']['last_updated'] = datetime.now().isoformat()

    with open(ANALYTICS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def fetch_current_metrics():
    """
    Fetch current metrics from newsletter platform

    In a real implementation, this would connect to:
    - Substack API
    - Ghost API
    - Beehiiv API
    - ConvertKit API
    etc.

    Returns:
        dict: Current metrics
    """
    print("Fetching current metrics from newsletter platform...")

    # Mock data for demonstration
    # In production, replace with actual API calls
    metrics = {
        'date': datetime.now().isoformat(),
        'subscribers': {
            'total': 1250,
            'new_this_week': 45,
            'unsubscribed': 3,
            'net_growth': 42
        },
        'engagement': {
            'open_rate': 42.5,
            'click_through_rate': 8.2,
            'total_opens': 531,
            'total_clicks': 103
        },
        'top_performing': {
            'most_opened': 'AI Regulation Deep Dive',
            'most_clicked': 'The Future of Remote Work',
            'avg_read_time': '6.5 minutes'
        },
        'revenue': {
            'monthly_recurring': 1200,
            'sponsors': 500,
            'total': 1700
        }
    }

    print("✓ Metrics fetched successfully")
    return metrics


def calculate_growth_rate(current, previous):
    """
    Calculate growth rate between periods

    Args:
        current (float): Current value
        previous (float): Previous value

    Returns:
        float: Growth rate as percentage
    """
    if previous == 0:
        return 0.0

    return ((current - previous) / previous) * 100


def generate_weekly_report(compare=False):
    """
    Generate weekly analytics report

    Args:
        compare (bool): Compare with previous week

    Returns:
        dict: Weekly report
    """
    print("\n" + "="*60)
    print("WEEKLY ANALYTICS REPORT")
    print("="*60 + "\n")

    # Fetch current metrics
    current_metrics = fetch_current_metrics()

    # Load historical data
    history = load_analytics_history()

    # Calculate week-over-week changes
    report = {
        'period': 'week',
        'date': datetime.now().isoformat(),
        'current': current_metrics,
        'changes': {}
    }

    if compare and history['newsletter']['metrics']:
        # Get last week's metrics
        previous = history['newsletter']['metrics'][-1]

        # Calculate changes
        report['changes'] = {
            'subscriber_growth': calculate_growth_rate(
                current_metrics['subscribers']['total'],
                previous['subscribers']['total']
            ),
            'open_rate_change': current_metrics['engagement']['open_rate'] -
                                previous['engagement']['open_rate'],
            'ctr_change': current_metrics['engagement']['click_through_rate'] -
                         previous['engagement']['click_through_rate']
        }

    # Save current metrics to history
    history['newsletter']['metrics'].append(current_metrics)
    save_analytics_history(history)

    return report


def generate_monthly_report():
    """
    Generate monthly analytics report

    Returns:
        dict: Monthly report
    """
    print("\n" + "="*60)
    print("MONTHLY ANALYTICS REPORT")
    print("="*60 + "\n")

    history = load_analytics_history()

    # Get last 4 weeks of data
    recent_metrics = history['newsletter']['metrics'][-4:]

    if not recent_metrics:
        print("⚠ Insufficient data for monthly report")
        return None

    # Calculate monthly averages
    avg_open_rate = sum(m['engagement']['open_rate'] for m in recent_metrics) / len(recent_metrics)
    avg_ctr = sum(m['engagement']['click_through_rate'] for m in recent_metrics) / len(recent_metrics)

    total_new_subscribers = sum(m['subscribers']['new_this_week'] for m in recent_metrics)

    report = {
        'period': 'month',
        'date': datetime.now().isoformat(),
        'summary': {
            'avg_open_rate': round(avg_open_rate, 2),
            'avg_click_through_rate': round(avg_ctr, 2),
            'total_new_subscribers': total_new_subscribers,
            'total_revenue': sum(m['revenue']['total'] for m in recent_metrics)
        },
        'trends': {
            'open_rate_trend': 'increasing' if recent_metrics[-1]['engagement']['open_rate'] >
                                              recent_metrics[0]['engagement']['open_rate'] else 'decreasing',
            'subscriber_trend': 'growing' if total_new_subscribers > 0 else 'stable'
        }
    }

    return report


def format_report_markdown(report):
    """
    Format report as markdown

    Args:
        report (dict): Report data

    Returns:
        str: Markdown formatted report
    """
    period = report['period'].upper()
    md = [f"# {period}LY NEWSLETTER ANALYTICS\n"]
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    md.append("---\n")

    if period == "WEEK":
        # Weekly report format
        current = report['current']

        md.append("## Subscribers")
        md.append(f"- **Total:** {current['subscribers']['total']:,}")
        md.append(f"- **New this week:** {current['subscribers']['new_this_week']}")
        md.append(f"- **Unsubscribed:** {current['subscribers']['unsubscribed']}")
        md.append(f"- **Net growth:** {current['subscribers']['net_growth']}\n")

        md.append("## Engagement")
        md.append(f"- **Open rate:** {current['engagement']['open_rate']}%")
        md.append(f"- **Click-through rate:** {current['engagement']['click_through_rate']}%")
        md.append(f"- **Total opens:** {current['engagement']['total_opens']:,}")
        md.append(f"- **Total clicks:** {current['engagement']['total_clicks']}\n")

        md.append("## Top Performing")
        md.append(f"- **Most opened:** {current['top_performing']['most_opened']}")
        md.append(f"- **Most clicked:** {current['top_performing']['most_clicked']}")
        md.append(f"- **Avg read time:** {current['top_performing']['avg_read_time']}\n")

        md.append("## Revenue")
        md.append(f"- **Monthly recurring:** ${current['revenue']['monthly_recurring']:,}")
        md.append(f"- **Sponsors:** ${current['revenue']['sponsors']:,}")
        md.append(f"- **Total:** ${current['revenue']['total']:,}\n")

        # Week-over-week changes
        if 'changes' in report and report['changes']:
            md.append("## Week-over-Week Changes")
            changes = report['changes']
            md.append(f"- **Subscriber growth:** {changes['subscriber_growth']:+.1f}%")
            md.append(f"- **Open rate change:** {changes['open_rate_change']:+.1f}%")
            md.append(f"- **CTR change:** {changes['ctr_change']:+.1f}%\n")

    else:
        # Monthly report format
        summary = report['summary']

        md.append("## Monthly Summary")
        md.append(f"- **Avg open rate:** {summary['avg_open_rate']}%")
        md.append(f"- **Avg click-through rate:** {summary['avg_click_through_rate']}%")
        md.append(f"- **Total new subscribers:** {summary['total_new_subscribers']}")
        md.append(f"- **Total revenue:** ${summary['total_revenue']:,}\n")

        md.append("## Trends")
        trends = report['trends']
        md.append(f"- **Open rate:** {trends['open_rate_trend']}")
        md.append(f"- **Subscribers:** {trends['subscriber_trend']}\n")

    md.append("---")
    md.append("\n*Generated by analytics_report.py*")

    return "\n".join(md)


def main():
    """Main entry point for analytics_report script"""
    parser = argparse.ArgumentParser(
        description='Generate newsletter analytics reports'
    )
    parser.add_argument(
        '--period',
        choices=['week', 'month'],
        default='week',
        help='Report period'
    )
    parser.add_argument(
        '--output',
        choices=['json', 'markdown'],
        default='markdown',
        help='Output format'
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare with previous period'
    )

    args = parser.parse_args()

    # Generate report
    if args.period == 'week':
        report = generate_weekly_report(compare=args.compare)
    else:
        report = generate_monthly_report()

    if not report:
        return

    # Output report
    if args.output == 'markdown':
        markdown_report = format_report_markdown(report)
        print("\n" + markdown_report)

        # Save to file
        report_file = DATA_DIR / f"analytics_report_{args.period}_{datetime.now().strftime('%Y%m%d')}.md"
        with open(report_file, 'w') as f:
            f.write(markdown_report)
        print(f"\n✓ Report saved to: {report_file}")

    else:
        print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
