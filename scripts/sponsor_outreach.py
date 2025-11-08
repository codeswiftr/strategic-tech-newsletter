#!/usr/bin/env python3
"""
sponsor_outreach.py - Generate prospect list and sponsorship pitches

Usage:
    python sponsor_outreach.py --generate-prospects --niche="developer-tools"
    python sponsor_outreach.py --pitch --company="Acme Corp" --template=standard
"""

import argparse
import json
from datetime import datetime
from pathlib import Path


# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
SPONSOR_PIPELINE = DATA_DIR / "sponsor_pipeline.json"
PITCH_TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "pitches"


def load_sponsor_pipeline():
    """
    Load sponsor pipeline data

    Returns:
        dict: Sponsor pipeline
    """
    if SPONSOR_PIPELINE.exists():
        with open(SPONSOR_PIPELINE, 'r') as f:
            return json.load(f)
    else:
        return {
            'prospects': [],
            'active': [],
            'closed': [],
            'last_updated': None
        }


def save_sponsor_pipeline(data):
    """
    Save sponsor pipeline to file

    Args:
        data (dict): Pipeline data
    """
    data['last_updated'] = datetime.now().isoformat()

    with open(SPONSOR_PIPELINE, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Pipeline saved to: {SPONSOR_PIPELINE}")


def generate_prospects(niche, count=20):
    """
    Generate list of potential sponsors based on newsletter niche

    Args:
        niche (str): Newsletter niche/focus area
        count (int): Number of prospects to generate

    Returns:
        list: List of potential sponsors
    """
    print(f"Generating {count} sponsor prospects for niche: {niche}")

    # Define target categories by niche
    niche_targets = {
        'developer-tools': [
            'IDE providers', 'Code hosting platforms', 'CI/CD services',
            'API platforms', 'Monitoring/observability', 'Cloud providers'
        ],
        'ai-ml': [
            'MLOps platforms', 'GPU cloud providers', 'Vector databases',
            'AI model hosting', 'Data labeling services', 'LLM platforms'
        ],
        'devops': [
            'Container platforms', 'Kubernetes tools', 'Infrastructure as code',
            'Secrets management', 'Cloud cost optimization', 'Security scanning'
        ],
        'web3': [
            'Blockchain infrastructure', 'Wallet providers', 'NFT platforms',
            'DeFi protocols', 'Layer 2 solutions', 'Web3 analytics'
        ]
    }

    target_categories = niche_targets.get(niche, ['General SaaS', 'Developer tools'])

    # Mock prospect generation
    # In production, this would:
    # 1. Scrape Crunchbase for companies in target categories
    # 2. Filter by funding stage, revenue, target audience
    # 3. Check against existing pipeline to avoid duplicates
    # 4. Score by fit (audience overlap, budget likelihood, brand alignment)

    prospects = []

    for i, category in enumerate(target_categories[:count]):
        prospect = {
            'id': f"PROSPECT_{datetime.now().strftime('%Y%m%d')}_{i:03d}",
            'company_name': f"Example {category} Company {i+1}",
            'category': category,
            'website': f"https://example-{i+1}.com",
            'estimated_budget': '$2,000 - $5,000',
            'fit_score': 85 - (i * 2),  # Decreasing fit score
            'contact_info': {
                'marketing_email': f"marketing@example-{i+1}.com",
                'linkedin': f"https://linkedin.com/company/example-{i+1}"
            },
            'status': 'prospect',
            'added_date': datetime.now().isoformat()
        }
        prospects.append(prospect)

    print(f"✓ Generated {len(prospects)} prospects")

    return prospects


def create_pitch(company_name, template='standard', custom_data=None):
    """
    Create sponsorship pitch for a specific company

    Args:
        company_name (str): Name of company to pitch
        template (str): Pitch template to use
        custom_data (dict): Custom data for personalization

    Returns:
        str: Personalized pitch
    """
    print(f"Creating pitch for {company_name} using '{template}' template")

    # Newsletter metrics for pitch (would be fetched from analytics)
    metrics = {
        'subscribers': 1250,
        'open_rate': 42.5,
        'click_through_rate': 8.2,
        'audience': 'Technical leaders, CTOs, senior engineers',
        'avg_read_time': '6.5 minutes'
    }

    # Pitch templates
    templates = {
        'standard': f"""
Subject: Partnership Opportunity - Strategic Tech Newsletter

Hi [Contact Name],

I'm reaching out about a potential sponsorship opportunity for {company_name} in my Strategic Tech Newsletter.

NEWSLETTER OVERVIEW:
• {metrics['subscribers']:,} subscribers (technical leaders, CTOs, senior engineers)
• {metrics['open_rate']}% average open rate
• {metrics['click_through_rate']}% click-through rate
• {metrics['avg_read_time']} average read time

AUDIENCE:
Our readers are {metrics['audience']} who actively seek tools and platforms to improve their workflows. Based on {company_name}'s focus on [COMPANY_CATEGORY], I believe there's strong alignment.

SPONSORSHIP FORMATS:
1. **Featured Sponsor** - Dedicated paragraph + logo ($2,500/issue)
2. **Brief Mention** - 2-3 sentence callout + link ($1,000/issue)
3. **Multi-Issue Package** - 4 issues over 8 weeks ($8,000, 20% discount)

RECENT PERFORMANCE:
• [Last sponsor] saw 120+ click-throughs and 15+ demo signups
• [Previous sponsor] reported 8% conversion from newsletter to trial

NEXT STEPS:
Would you be open to a 15-minute call next week to discuss how we can showcase {company_name} to our audience?

I'm happy to provide case studies from previous sponsors and answer any questions.

Best regards,
[Your Name]
Strategic Tech Newsletter
[Your Email]
[Newsletter URL]
""",

        'data-driven': f"""
Subject: High-Intent Developer Audience for {company_name}

Hi [Contact Name],

Quick pitch: {metrics['subscribers']:,} technical decision-makers with {metrics['open_rate']}% open rates and {metrics['click_through_rate']}% CTR.

WHY THIS WORKS:
✓ Audience matches your ICP (technical leaders, engineers, CTOs)
✓ High engagement (2-3x industry average)
✓ Long-form content = serious readers, not skimmers
✓ Previous sponsors report 8-12% newsletter → trial conversion

SPONSORSHIP OPTIONS:
→ Featured ($2,500): Dedicated 100-150 word spotlight + logo
→ Brief ($1,000): 2-3 sentence mention + link
→ Package deal: 4 issues across 8 weeks ($8,000, save 20%)

PROOF:
Last month's sponsor (dev tools company) got:
• 130 click-throughs
• 18 demo bookings
• 6 paid conversions
• ~3.5x ROI

15-minute call to discuss?

[Your Name]
[Contact]
""",

        'value-first': f"""
Subject: Thought Leadership Opportunity for {company_name}

Hi [Contact Name],

I'm working on an upcoming essay about [RELEVANT_TOPIC] and thought {company_name}'s expertise would add tremendous value to my readers.

CONCEPT:
Instead of a traditional ad, I'd love to feature {company_name} as a case study or technical deep-dive within the essay. This gives readers genuine value while showcasing your solution in context.

FORMAT OPTIONS:
1. **Technical Deep Dive**: How {company_name} solves [problem] (400-500 words)
2. **Case Study**: Customer success story with {company_name} (300 words)
3. **Expert Quote**: Technical insight from your team's engineering lead

AUDIENCE & REACH:
• {metrics['subscribers']:,} subscribers ({metrics['audience']})
• {metrics['open_rate']}% open rate, {metrics['click_through_rate']}% CTR
• Average {metrics['avg_read_time']} read time (highly engaged)

INVESTMENT:
$2,000 for integrated sponsorship + social amplification

This performs significantly better than banner ads because it's:
✓ Educational content, not interruption
✓ Builds trust through association
✓ Gets shared/referenced long-term

Interested in exploring this for [UPCOMING_TOPIC]?

[Your Name]
"""
    }

    pitch = templates.get(template, templates['standard'])

    # Add custom data if provided
    if custom_data:
        for key, value in custom_data.items():
            pitch = pitch.replace(f"[{key.upper()}]", str(value))

    return pitch


def update_prospect_status(prospect_id, new_status, notes=""):
    """
    Update prospect status in pipeline

    Args:
        prospect_id (str): Prospect ID
        new_status (str): New status (prospect, contacted, negotiating, active, closed)
        notes (str): Additional notes
    """
    pipeline = load_sponsor_pipeline()

    # Find prospect across all categories
    for category in ['prospects', 'active', 'closed']:
        for i, prospect in enumerate(pipeline[category]):
            if prospect['id'] == prospect_id:
                # Update status
                prospect['status'] = new_status
                prospect['last_updated'] = datetime.now().isoformat()
                if notes:
                    if 'notes' not in prospect:
                        prospect['notes'] = []
                    prospect['notes'].append({
                        'date': datetime.now().isoformat(),
                        'note': notes
                    })

                # Move to appropriate category
                pipeline[category].pop(i)
                if new_status in ['prospect', 'contacted', 'negotiating']:
                    pipeline['prospects'].append(prospect)
                elif new_status == 'active':
                    pipeline['active'].append(prospect)
                elif new_status == 'closed':
                    pipeline['closed'].append(prospect)

                save_sponsor_pipeline(pipeline)
                print(f"✓ Updated prospect {prospect_id} to status: {new_status}")
                return

    print(f"⚠ Prospect {prospect_id} not found")


def main():
    """Main entry point for sponsor_outreach script"""
    parser = argparse.ArgumentParser(
        description='Manage sponsor prospecting and outreach'
    )
    parser.add_argument(
        '--generate-prospects',
        action='store_true',
        help='Generate new sponsor prospects'
    )
    parser.add_argument(
        '--niche',
        default='developer-tools',
        help='Newsletter niche for targeting'
    )
    parser.add_argument(
        '--pitch',
        action='store_true',
        help='Generate sponsorship pitch'
    )
    parser.add_argument(
        '--company',
        help='Company name for pitch'
    )
    parser.add_argument(
        '--template',
        choices=['standard', 'data-driven', 'value-first'],
        default='standard',
        help='Pitch template to use'
    )
    parser.add_argument(
        '--update-status',
        help='Update prospect status (use with --prospect-id and --status)'
    )
    parser.add_argument(
        '--prospect-id',
        help='Prospect ID for status update'
    )

    args = parser.parse_args()

    if args.generate_prospects:
        # Generate new prospects
        prospects = generate_prospects(args.niche)

        # Load pipeline and add prospects
        pipeline = load_sponsor_pipeline()
        pipeline['prospects'].extend(prospects)
        save_sponsor_pipeline(pipeline)

        # Display top prospects
        print(f"\nTop 5 Prospects:")
        for i, p in enumerate(sorted(prospects, key=lambda x: x['fit_score'], reverse=True)[:5], 1):
            print(f"{i}. {p['company_name']} ({p['category']}) - Fit Score: {p['fit_score']}")

    elif args.pitch and args.company:
        # Generate pitch
        pitch = create_pitch(args.company, args.template)

        print("\n" + "="*60)
        print(f"SPONSORSHIP PITCH FOR: {args.company}")
        print("="*60)
        print(pitch)
        print("="*60 + "\n")

        # Save pitch to file
        pitch_file = DATA_DIR / f"pitch_{args.company.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(pitch_file, 'w') as f:
            f.write(pitch)
        print(f"✓ Pitch saved to: {pitch_file}")

    elif args.update_status and args.prospect_id:
        # Update prospect status
        update_prospect_status(args.prospect_id, args.update_status)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
