#!/usr/bin/env python3
"""
social_repurpose.py - Generate social posts from newsletter essays

Usage:
    python social_repurpose.py --essay=content/essays/ai_regulation.md --formats=all
    python social_repurpose.py --essay=content/essays/ai_regulation.md --formats=twitter
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime


# Configuration
CONTENT_DIR = Path(__file__).parent.parent / "content"
SOCIAL_DIR = CONTENT_DIR / "social_posts"

# Social media constraints
TWITTER_MAX_LENGTH = 280
TWITTER_THREAD_MAX = 10
LINKEDIN_OPTIMAL = 1300


def read_essay(essay_path):
    """
    Read and parse essay content

    Args:
        essay_path (str): Path to essay markdown file

    Returns:
        dict: Parsed essay with title, content, key points
    """
    essay_file = Path(essay_path)

    if not essay_file.exists():
        print(f"Error: Essay not found: {essay_path}")
        return None

    with open(essay_file, 'r') as f:
        content = f.read()

    # Extract title (first H1 heading)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Untitled Essay"

    # Extract key points (look for bullet points or numbered lists)
    bullet_pattern = r'^[-*]\s+(.+)$'
    key_points = re.findall(bullet_pattern, content, re.MULTILINE)

    # Extract first paragraph as hook
    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and not p.startswith('#')]
    hook = paragraphs[0] if paragraphs else ""

    return {
        'title': title,
        'content': content,
        'hook': hook,
        'key_points': key_points[:5],  # Top 5 key points
        'word_count': len(content.split())
    }


def generate_twitter_thread(essay):
    """
    Generate Twitter thread from essay

    Args:
        essay (dict): Parsed essay content

    Returns:
        list: Twitter thread (list of tweets)
    """
    print("Generating Twitter thread...")

    thread = []

    # Tweet 1: Hook + Title
    hook_tweet = f"{essay['title']}\n\nA thread 🧵👇"
    if len(hook_tweet) <= TWITTER_MAX_LENGTH:
        thread.append(hook_tweet)
    else:
        thread.append(f"{essay['title']}\n\n🧵👇")

    # Tweet 2: Hook/Introduction
    if essay['hook']:
        intro = essay['hook'][:TWITTER_MAX_LENGTH - 10] + "..."
        thread.append(intro)

    # Tweets 3-N: Key points
    for i, point in enumerate(essay['key_points'][:5], 1):
        tweet = f"{i}/ {point}"
        if len(tweet) > TWITTER_MAX_LENGTH:
            tweet = tweet[:TWITTER_MAX_LENGTH - 3] + "..."
        thread.append(tweet)

    # Final tweet: CTA
    cta = "Read the full analysis in my newsletter:\n[INSERT LINK]\n\nLike/RT if you found this useful!"
    thread.append(cta)

    print(f"✓ Generated {len(thread)} tweets")
    return thread


def generate_linkedin_post(essay):
    """
    Generate LinkedIn post from essay

    Args:
        essay (dict): Parsed essay content

    Returns:
        str: LinkedIn post
    """
    print("Generating LinkedIn post...")

    # LinkedIn structure: Hook → Context → Key Insights → CTA
    post_parts = []

    # Hook (attention-grabbing first line)
    post_parts.append(essay['title'])
    post_parts.append("")

    # Context (2-3 sentences)
    if essay['hook']:
        context = essay['hook'][:300]  # Keep it concise
        post_parts.append(context)
        post_parts.append("")

    # Key insights (3-5 bullet points)
    if essay['key_points']:
        post_parts.append("Key insights:")
        for point in essay['key_points'][:5]:
            post_parts.append(f"• {point}")
        post_parts.append("")

    # CTA
    post_parts.append("Read the full analysis in my newsletter (link in comments)")
    post_parts.append("")
    post_parts.append("What's your take? Share your thoughts below. 👇")
    post_parts.append("")
    post_parts.append("#TechStrategy #Innovation #Leadership")

    linkedin_post = "\n".join(post_parts)

    # Ensure optimal length
    if len(linkedin_post) > LINKEDIN_OPTIMAL:
        print(f"⚠ LinkedIn post is {len(linkedin_post)} chars (optimal: {LINKEDIN_OPTIMAL})")
    else:
        print(f"✓ LinkedIn post: {len(linkedin_post)} chars")

    return linkedin_post


def generate_newsletter_teaser(essay):
    """
    Generate short newsletter teaser for social sharing

    Args:
        essay (dict): Parsed essay content

    Returns:
        str: Newsletter teaser
    """
    print("Generating newsletter teaser...")

    teaser = f"""
🚀 New Essay: {essay['title']}

{essay['hook'][:200]}...

Read the full essay: [INSERT NEWSLETTER LINK]

Subscribe for weekly strategic tech insights 👉 [INSERT SUBSCRIBE LINK]
    """.strip()

    return teaser


def save_social_content(essay_name, formats_content):
    """
    Save generated social content to files

    Args:
        essay_name (str): Name of the essay (for filename)
        formats_content (dict): Generated content by format
    """
    # Create social_posts directory if it doesn't exist
    SOCIAL_DIR.mkdir(parents=True, exist_ok=True)

    # Create subfolder for this essay
    essay_folder = SOCIAL_DIR / essay_name
    essay_folder.mkdir(exist_ok=True)

    # Save each format
    for format_name, content in formats_content.items():
        output_file = essay_folder / f"{format_name}.txt"

        if format_name == "twitter" and isinstance(content, list):
            # Save Twitter thread with tweet numbers
            with open(output_file, 'w') as f:
                for i, tweet in enumerate(content, 1):
                    f.write(f"Tweet {i}/{len(content)}:\n")
                    f.write(tweet)
                    f.write("\n\n" + "="*50 + "\n\n")
        else:
            with open(output_file, 'w') as f:
                f.write(content)

        print(f"✓ Saved {format_name} content to: {output_file}")

    # Save metadata
    metadata = {
        'essay_name': essay_name,
        'generated_date': datetime.now().isoformat(),
        'formats': list(formats_content.keys())
    }

    metadata_file = essay_folder / "metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)


def main():
    """Main entry point for social_repurpose script"""
    parser = argparse.ArgumentParser(
        description='Generate social media content from newsletter essays'
    )
    parser.add_argument(
        '--essay',
        required=True,
        help='Path to essay markdown file'
    )
    parser.add_argument(
        '--formats',
        default='all',
        help='Formats to generate: all, twitter, linkedin, teaser (comma-separated)'
    )

    args = parser.parse_args()

    # Parse essay
    essay = read_essay(args.essay)
    if not essay:
        return

    print(f"\n{'='*60}")
    print(f"SOCIAL REPURPOSE: {essay['title']}")
    print(f"{'='*60}\n")

    # Determine which formats to generate
    if args.formats == 'all':
        formats = ['twitter', 'linkedin', 'teaser']
    else:
        formats = [f.strip() for f in args.formats.split(',')]

    # Generate content
    generated_content = {}

    if 'twitter' in formats:
        generated_content['twitter'] = generate_twitter_thread(essay)

    if 'linkedin' in formats:
        generated_content['linkedin'] = generate_linkedin_post(essay)

    if 'teaser' in formats:
        generated_content['teaser'] = generate_newsletter_teaser(essay)

    # Save all generated content
    essay_name = Path(args.essay).stem
    save_social_content(essay_name, generated_content)

    print(f"\n{'='*60}")
    print(f"✓ Social content generated and saved!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
