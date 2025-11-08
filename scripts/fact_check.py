#!/usr/bin/env python3
"""
fact_check.py - Validate claims against sources

Usage:
    python fact_check.py --draft=content/drafts/essay.md --strict
    python fact_check.py --claim="GPT-4 has 1.7T parameters"
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime

# Configuration
DATA_DIR = Path(__file__).parent.parent / "data"
FACT_CHECK_LIBRARY = DATA_DIR / "fact_check_library.json"


def extract_claims_from_draft(draft_path):
    """
    Extract factual claims from a draft essay

    Args:
        draft_path (str): Path to draft markdown file

    Returns:
        list: Extracted claims with context
    """
    print(f"Extracting claims from: {draft_path}")

    draft_file = Path(draft_path)
    if not draft_file.exists():
        print(f"Error: Draft file not found: {draft_path}")
        return []

    with open(draft_file, 'r') as f:
        content = f.read()

    # Extract claims (simple heuristic - look for sentences with numbers or statistics)
    claims = []

    # Pattern 1: Sentences with percentages
    percentage_pattern = r'[^.!?]*\d+%[^.!?]*[.!?]'
    percentage_claims = re.findall(percentage_pattern, content)
    claims.extend([{'claim': c.strip(), 'type': 'percentage'} for c in percentage_claims])

    # Pattern 2: Sentences with large numbers
    number_pattern = r'[^.!?]*\d{1,3}(?:,\d{3})+[^.!?]*[.!?]'
    number_claims = re.findall(number_pattern, content)
    claims.extend([{'claim': c.strip(), 'type': 'statistic'} for c in number_claims])

    # Pattern 3: Sentences with citations [source](url)
    citation_pattern = r'[^.!?]*\[([^\]]+)\]\(([^)]+)\)[^.!?]*[.!?]'
    cited_sentences = re.findall(citation_pattern, content)

    print(f"Found {len(claims)} potential factual claims")
    print(f"Found {len(cited_sentences)} citations")

    return claims


def verify_claim(claim_text, strict=True):
    """
    Verify a specific claim against fact-check library

    Args:
        claim_text (str): Claim to verify
        strict (bool): If True, require exact source match

    Returns:
        dict: Verification result with confidence score
    """
    print(f"Verifying claim: {claim_text[:100]}...")

    # Load fact-check library
    if FACT_CHECK_LIBRARY.exists():
        with open(FACT_CHECK_LIBRARY, 'r') as f:
            library = json.load(f)
    else:
        library = {'verified_claims': []}

    # Check if claim exists in library
    for verified in library['verified_claims']:
        if claim_text.lower() in verified['claim'].lower() or \
           verified['claim'].lower() in claim_text.lower():
            print(f"✓ Claim found in library (verified: {verified['verification_date']})")
            return {
                'verified': True,
                'confidence': 0.95,
                'source': verified.get('source_url', 'Unknown'),
                'verification_date': verified['verification_date']
            }

    # Claim not in library - needs manual verification
    print(f"⚠ Claim not in fact-check library - manual verification required")

    if strict:
        return {
            'verified': False,
            'confidence': 0.0,
            'source': None,
            'note': 'Requires manual verification and source citation'
        }
    else:
        return {
            'verified': None,
            'confidence': 0.5,
            'source': None,
            'note': 'Unverified - proceed with caution'
        }


def check_draft(draft_path, strict=True):
    """
    Run comprehensive fact-check on a draft essay

    Args:
        draft_path (str): Path to draft file
        strict (bool): Strict verification mode

    Returns:
        dict: Fact-check report
    """
    print(f"\n{'='*60}")
    print(f"FACT-CHECK REPORT: {draft_path}")
    print(f"{'='*60}\n")

    claims = extract_claims_from_draft(draft_path)

    report = {
        'draft': draft_path,
        'check_date': datetime.now().isoformat(),
        'total_claims': len(claims),
        'verified': 0,
        'unverified': 0,
        'failed': 0,
        'details': []
    }

    for claim in claims:
        result = verify_claim(claim['claim'], strict)

        claim_report = {
            'claim': claim['claim'],
            'type': claim['type'],
            'verification': result
        }

        if result['verified'] is True:
            report['verified'] += 1
        elif result['verified'] is False:
            report['failed'] += 1
        else:
            report['unverified'] += 1

        report['details'].append(claim_report)

    # Print summary
    print(f"\nFACT-CHECK SUMMARY:")
    print(f"Total claims analyzed: {report['total_claims']}")
    print(f"✓ Verified: {report['verified']}")
    print(f"⚠ Unverified: {report['unverified']}")
    print(f"✗ Failed: {report['failed']}")

    if strict and report['failed'] > 0:
        print(f"\n⚠ STRICT MODE: {report['failed']} claims failed verification")
        print("Cannot proceed to publication until all claims are verified")
        return report

    if report['unverified'] > 0:
        print(f"\n⚠ Warning: {report['unverified']} claims need manual verification")

    print(f"\n{'='*60}\n")

    return report


def add_to_library(claim, source_url, context=""):
    """
    Add a verified claim to the fact-check library

    Args:
        claim (str): The verified claim
        source_url (str): Source URL for verification
        context (str): Additional context
    """
    # Load existing library
    if FACT_CHECK_LIBRARY.exists():
        with open(FACT_CHECK_LIBRARY, 'r') as f:
            library = json.load(f)
    else:
        library = {'verified_claims': []}

    # Add new verified claim
    new_entry = {
        'claim': claim,
        'source_url': source_url,
        'verification_date': datetime.now().isoformat(),
        'context': context
    }

    library['verified_claims'].append(new_entry)

    # Save updated library
    with open(FACT_CHECK_LIBRARY, 'w') as f:
        json.dump(library, f, indent=2)

    print(f"✓ Added claim to fact-check library")


def main():
    """Main entry point for fact_check script"""
    parser = argparse.ArgumentParser(
        description='Fact-check newsletter drafts and claims'
    )
    parser.add_argument(
        '--draft',
        help='Path to draft file to fact-check'
    )
    parser.add_argument(
        '--claim',
        help='Single claim to verify'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Strict mode - fail on any unverified claims'
    )
    parser.add_argument(
        '--add',
        action='store_true',
        help='Add verified claim to library (use with --claim and --source)'
    )
    parser.add_argument(
        '--source',
        help='Source URL for claim verification'
    )

    args = parser.parse_args()

    if args.draft:
        report = check_draft(args.draft, args.strict)
        # Optionally save report to file
        report_path = Path(args.draft).parent / f"{Path(args.draft).stem}_factcheck.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {report_path}")

    elif args.claim:
        if args.add and args.source:
            add_to_library(args.claim, args.source)
        else:
            result = verify_claim(args.claim, args.strict)
            print(f"\nVerification result: {json.dumps(result, indent=2)}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
