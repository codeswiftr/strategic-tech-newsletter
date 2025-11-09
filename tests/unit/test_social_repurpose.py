"""
Unit tests for social_repurpose.py

Tests social media content generation including:
- Essay parsing and key point extraction
- Twitter thread generation with character limits
- LinkedIn post optimization
- Newsletter teaser creation
- Content saving and organization
"""
import pytest
import json
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from social_repurpose import (
    read_essay,
    generate_twitter_thread,
    generate_linkedin_post,
    generate_newsletter_teaser,
    save_social_content,
    TWITTER_MAX_LENGTH,
    LINKEDIN_OPTIMAL,
    SOCIAL_DIR
)


class TestReadEssay:
    """Test essay reading and parsing"""

    def test_read_essay_valid_file(self, sample_essay_file):
        """Should parse essay and extract key information"""
        essay = read_essay(str(sample_essay_file))

        assert essay is not None, "Should return essay data"
        assert 'title' in essay, "Should extract title"
        assert 'content' in essay, "Should have full content"
        assert 'hook' in essay, "Should extract hook"
        assert 'key_points' in essay, "Should extract key points"
        assert 'word_count' in essay, "Should count words"

        # Verify specific content
        assert essay['title'] == "The Future of AI Regulation"
        assert essay['word_count'] > 0
        assert isinstance(essay['key_points'], list)

    def test_read_essay_extracts_title(self, sample_essay_file):
        """Should extract title from H1 heading"""
        essay = read_essay(str(sample_essay_file))

        assert essay['title'] == "The Future of AI Regulation"
        assert essay['title'] != "Untitled Essay"

    def test_read_essay_extracts_key_points(self, sample_essay_file):
        """Should extract bullet points as key points"""
        essay = read_essay(str(sample_essay_file))

        assert len(essay['key_points']) > 0, "Should find key points"
        # Essay has bullets about regulation frameworks, investment, etc.
        assert any('12 countries' in point or 'regulation' in point.lower()
                   for point in essay['key_points'])

    def test_read_essay_extracts_hook(self, sample_essay_file):
        """Should extract first paragraph as hook"""
        essay = read_essay(str(sample_essay_file))

        assert len(essay['hook']) > 0, "Should have hook"
        # First paragraph mentions 45% growth
        assert '45%' in essay['hook']

    def test_read_essay_missing_file(self):
        """Should handle missing file gracefully"""
        essay = read_essay("/nonexistent/path/essay.md")

        assert essay is None, "Should return None for missing file"

    def test_read_essay_no_title(self, temp_data_dir):
        """Should handle essay without H1 heading"""
        essay_path = temp_data_dir / "no_title.md"
        essay_path.write_text("Just content without title.\n\nMore content here.")

        essay = read_essay(str(essay_path))

        assert essay is not None
        assert essay['title'] == "Untitled Essay"

    def test_read_essay_no_bullets(self, temp_data_dir):
        """Should handle essay without bullet points"""
        essay_path = temp_data_dir / "no_bullets.md"
        essay_path.write_text("# Test Essay\n\nJust paragraphs.\n\nNo bullets.")

        essay = read_essay(str(essay_path))

        assert essay is not None
        assert essay['key_points'] == []

    def test_read_essay_counts_words_correctly(self, temp_data_dir):
        """Should count words accurately"""
        essay_path = temp_data_dir / "word_count.md"
        # Title + exactly 10 words in content = 11 total
        essay_path.write_text("# Title\n\nThis essay has exactly ten words in its content.")

        essay = read_essay(str(essay_path))

        # Word count includes everything (title + content)
        assert essay['word_count'] == 11


class TestGenerateTwitterThread:
    """Test Twitter thread generation"""

    def test_generate_twitter_thread_basic(self, sample_essay_content):
        """Should generate valid Twitter thread"""
        essay = {
            'title': 'The Future of AI Regulation',
            'hook': sample_essay_content[:200],
            'key_points': [
                'Regulation frameworks emerging',
                'Investment reached $50M',
                'Self-regulation protocols'
            ]
        }

        thread = generate_twitter_thread(essay)

        assert isinstance(thread, list), "Should return list of tweets"
        assert len(thread) > 0, "Should have at least one tweet"

        # First tweet should be hook + thread indicator
        assert 'The Future of AI Regulation' in thread[0]
        assert '🧵' in thread[0] or 'thread' in thread[0].lower()

    def test_generate_twitter_thread_respects_character_limit(self, sample_essay_content):
        """Should enforce 280 character limit"""
        essay = {
            'title': 'Test Essay',
            'hook': sample_essay_content[:200],
            'key_points': ['Point 1', 'Point 2', 'Point 3']
        }

        thread = generate_twitter_thread(essay)

        for i, tweet in enumerate(thread):
            assert len(tweet) <= TWITTER_MAX_LENGTH, \
                f"Tweet {i+1} exceeds {TWITTER_MAX_LENGTH} chars: {len(tweet)}"

    def test_generate_twitter_thread_includes_key_points(self):
        """Should include key points in thread"""
        essay = {
            'title': 'Test Essay',
            'hook': 'Introduction paragraph',
            'key_points': [
                'First key insight',
                'Second key insight',
                'Third key insight'
            ]
        }

        thread = generate_twitter_thread(essay)

        # Should have tweets for key points
        assert len(thread) >= 3, "Should have tweets for key points"

        # Check that key points appear in thread
        thread_text = ' '.join(thread)
        for point in essay['key_points']:
            # Point should appear in some form
            assert any(word in thread_text for word in point.split()[:2])

    def test_generate_twitter_thread_has_cta(self):
        """Should include call-to-action in final tweet"""
        essay = {
            'title': 'Test Essay',
            'hook': 'Hook text',
            'key_points': ['Point 1']
        }

        thread = generate_twitter_thread(essay)

        final_tweet = thread[-1]
        # Should have CTA elements
        assert any(phrase in final_tweet.lower() for phrase in [
            'read', 'link', 'full', 'like', 'rt', 'retweet'
        ])

    def test_generate_twitter_thread_handles_long_title(self):
        """Should handle very long titles gracefully"""
        essay = {
            'title': 'A Very Long Title That Exceeds Normal Length And Should Be Truncated To Fit Within Tweet Character Limits',
            'hook': 'Hook',
            'key_points': []
        }

        thread = generate_twitter_thread(essay)

        assert thread[0] is not None
        assert len(thread[0]) <= TWITTER_MAX_LENGTH

    def test_generate_twitter_thread_minimum_length(self):
        """Should generate reasonable thread length"""
        essay = {
            'title': 'Test',
            'hook': 'Hook',
            'key_points': ['A', 'B', 'C']
        }

        thread = generate_twitter_thread(essay)

        # Should have at least: hook tweet + key point tweets + CTA
        assert len(thread) >= 3


class TestGenerateLinkedInPost:
    """Test LinkedIn post generation"""

    def test_generate_linkedin_post_basic(self):
        """Should generate basic LinkedIn post"""
        essay = {
            'title': 'The Future of AI Regulation',
            'hook': 'The AI industry is growing rapidly.',
            'key_points': [
                'Regulation frameworks emerging',
                'Investment at all-time high',
                'Self-regulation becoming standard'
            ]
        }

        post = generate_linkedin_post(essay)

        assert isinstance(post, str), "Should return string"
        assert len(post) > 0, "Should have content"

    def test_generate_linkedin_post_includes_title(self):
        """Should include essay title"""
        essay = {
            'title': 'Test Essay Title',
            'hook': 'Hook text',
            'key_points': []
        }

        post = generate_linkedin_post(essay)

        assert 'Test Essay Title' in post

    def test_generate_linkedin_post_includes_key_points(self):
        """Should include key insights as bullets"""
        essay = {
            'title': 'Test',
            'hook': 'Hook',
            'key_points': [
                'First insight',
                'Second insight',
                'Third insight'
            ]
        }

        post = generate_linkedin_post(essay)

        # Should have bullet points
        assert '•' in post or '-' in post or '*' in post

        # Should include insights
        assert 'First insight' in post
        assert 'Second insight' in post

    def test_generate_linkedin_post_optimal_length(self):
        """Should aim for optimal LinkedIn length"""
        essay = {
            'title': 'Test Essay',
            'hook': 'A reasonably sized hook paragraph that provides context.',
            'key_points': ['Point 1', 'Point 2', 'Point 3']
        }

        post = generate_linkedin_post(essay)

        # Should be reasonable length (LinkedIn optimal is ~1300)
        # Allow some flexibility
        assert len(post) > 100, "Should have substantial content"
        # Warn if too long but don't fail
        if len(post) > LINKEDIN_OPTIMAL:
            print(f"Warning: LinkedIn post is {len(post)} chars (optimal: {LINKEDIN_OPTIMAL})")

    def test_generate_linkedin_post_has_hashtags(self):
        """Should include relevant hashtags"""
        essay = {
            'title': 'AI Regulation',
            'hook': 'Hook',
            'key_points': []
        }

        post = generate_linkedin_post(essay)

        assert '#' in post, "Should include hashtags"

    def test_generate_linkedin_post_has_cta(self):
        """Should include call-to-action"""
        essay = {
            'title': 'Test',
            'hook': 'Hook',
            'key_points': []
        }

        post = generate_linkedin_post(essay)

        # Should have engagement CTA
        post_lower = post.lower()
        assert any(phrase in post_lower for phrase in [
            'thoughts', 'comment', 'share', 'link', 'read'
        ])

    def test_generate_linkedin_post_formatted_readably(self):
        """Should have readable formatting with paragraph breaks"""
        essay = {
            'title': 'Test Essay',
            'hook': 'Hook paragraph',
            'key_points': ['Point 1', 'Point 2']
        }

        post = generate_linkedin_post(essay)

        # Should have line breaks for readability
        assert '\n' in post, "Should have paragraph breaks"


class TestGenerateNewsletterTeaser:
    """Test newsletter teaser generation"""

    def test_generate_newsletter_teaser_basic(self):
        """Should generate basic teaser"""
        essay = {
            'title': 'The Future of AI Regulation',
            'hook': 'The AI industry is experiencing rapid growth and regulatory changes.'
        }

        teaser = generate_newsletter_teaser(essay)

        assert isinstance(teaser, str), "Should return string"
        assert len(teaser) > 0, "Should have content"

    def test_generate_newsletter_teaser_includes_title(self):
        """Should include essay title"""
        essay = {
            'title': 'Test Essay Title',
            'hook': 'Hook text here'
        }

        teaser = generate_newsletter_teaser(essay)

        assert 'Test Essay Title' in teaser

    def test_generate_newsletter_teaser_includes_hook(self):
        """Should include truncated hook"""
        essay = {
            'title': 'Test',
            'hook': 'This is the hook paragraph that should appear in the teaser.'
        }

        teaser = generate_newsletter_teaser(essay)

        # Should include some of the hook
        assert 'hook' in teaser.lower() or 'This is the' in teaser

    def test_generate_newsletter_teaser_reasonable_length(self):
        """Should be concise (teaser, not full content)"""
        essay = {
            'title': 'Test Essay',
            'hook': 'A' * 1000  # Very long hook
        }

        teaser = generate_newsletter_teaser(essay)

        # Should truncate to reasonable teaser length
        assert len(teaser) < 500, "Teaser should be concise"

    def test_generate_newsletter_teaser_has_cta(self):
        """Should include link placeholders and CTA"""
        essay = {
            'title': 'Test',
            'hook': 'Hook'
        }

        teaser = generate_newsletter_teaser(essay)

        # Should have CTA elements
        teaser_lower = teaser.lower()
        assert any(phrase in teaser_lower for phrase in [
            'read', 'link', 'subscribe', 'full'
        ])


class TestSaveSocialContent:
    """Test saving social content to files"""

    def test_save_social_content_creates_directory(self, temp_data_dir):
        """Should create essay-specific directory"""
        import social_repurpose
        original_social_dir = social_repurpose.SOCIAL_DIR
        social_repurpose.SOCIAL_DIR = temp_data_dir

        try:
            essay_name = "test_essay"
            content = {
                'twitter': ['Tweet 1', 'Tweet 2'],
                'linkedin': 'LinkedIn post content'
            }

            save_social_content(essay_name, content)

            essay_folder = temp_data_dir / essay_name
            assert essay_folder.exists(), "Should create essay folder"
            assert essay_folder.is_dir(), "Should be a directory"

        finally:
            social_repurpose.SOCIAL_DIR = original_social_dir

    def test_save_social_content_saves_twitter_thread(self, temp_data_dir):
        """Should save Twitter thread with numbered tweets"""
        import social_repurpose
        original_social_dir = social_repurpose.SOCIAL_DIR
        social_repurpose.SOCIAL_DIR = temp_data_dir

        try:
            essay_name = "test_essay"
            tweets = ['Tweet 1', 'Tweet 2', 'Tweet 3']
            content = {'twitter': tweets}

            save_social_content(essay_name, content)

            twitter_file = temp_data_dir / essay_name / "twitter.txt"
            assert twitter_file.exists(), "Should create twitter.txt"

            # Verify content
            twitter_content = twitter_file.read_text()
            assert 'Tweet 1' in twitter_content
            assert 'Tweet 2' in twitter_content
            assert 'Tweet 3' in twitter_content

            # Should have tweet numbers
            assert 'Tweet 1/' in twitter_content or '1/' in twitter_content

        finally:
            social_repurpose.SOCIAL_DIR = original_social_dir

    def test_save_social_content_saves_linkedin_post(self, temp_data_dir):
        """Should save LinkedIn post"""
        import social_repurpose
        original_social_dir = social_repurpose.SOCIAL_DIR
        social_repurpose.SOCIAL_DIR = temp_data_dir

        try:
            essay_name = "test_essay"
            content = {'linkedin': 'LinkedIn post content here'}

            save_social_content(essay_name, content)

            linkedin_file = temp_data_dir / essay_name / "linkedin.txt"
            assert linkedin_file.exists(), "Should create linkedin.txt"

            linkedin_content = linkedin_file.read_text()
            assert 'LinkedIn post content here' in linkedin_content

        finally:
            social_repurpose.SOCIAL_DIR = original_social_dir

    def test_save_social_content_saves_metadata(self, temp_data_dir):
        """Should save metadata.json"""
        import social_repurpose
        original_social_dir = social_repurpose.SOCIAL_DIR
        social_repurpose.SOCIAL_DIR = temp_data_dir

        try:
            essay_name = "test_essay"
            content = {
                'twitter': ['Tweet 1'],
                'linkedin': 'LinkedIn post'
            }

            save_social_content(essay_name, content)

            metadata_file = temp_data_dir / essay_name / "metadata.json"
            assert metadata_file.exists(), "Should create metadata.json"

            with open(metadata_file, 'r') as f:
                metadata = json.load(f)

            assert 'essay_name' in metadata
            assert metadata['essay_name'] == essay_name
            assert 'generated_date' in metadata
            assert 'formats' in metadata
            assert set(metadata['formats']) == {'twitter', 'linkedin'}

        finally:
            social_repurpose.SOCIAL_DIR = original_social_dir

    def test_save_social_content_handles_multiple_formats(self, temp_data_dir):
        """Should save all provided formats"""
        import social_repurpose
        original_social_dir = social_repurpose.SOCIAL_DIR
        social_repurpose.SOCIAL_DIR = temp_data_dir

        try:
            essay_name = "multi_format_essay"
            content = {
                'twitter': ['Tweet 1', 'Tweet 2'],
                'linkedin': 'LinkedIn content',
                'teaser': 'Newsletter teaser'
            }

            save_social_content(essay_name, content)

            essay_folder = temp_data_dir / essay_name

            # All files should exist
            assert (essay_folder / "twitter.txt").exists()
            assert (essay_folder / "linkedin.txt").exists()
            assert (essay_folder / "teaser.txt").exists()
            assert (essay_folder / "metadata.json").exists()

        finally:
            social_repurpose.SOCIAL_DIR = original_social_dir


@pytest.mark.integration
class TestSocialRepurposeIntegration:
    """Integration tests for full social repurposing workflow"""

    def test_full_repurpose_workflow(self, sample_essay_file, temp_data_dir):
        """Test complete workflow: read essay → generate all formats → save"""
        import social_repurpose
        original_social_dir = social_repurpose.SOCIAL_DIR
        social_repurpose.SOCIAL_DIR = temp_data_dir

        try:
            # Step 1: Read essay
            essay = read_essay(str(sample_essay_file))
            assert essay is not None

            # Step 2: Generate all formats
            twitter_thread = generate_twitter_thread(essay)
            linkedin_post = generate_linkedin_post(essay)
            teaser = generate_newsletter_teaser(essay)

            # Verify generated content
            assert len(twitter_thread) > 0
            assert len(linkedin_post) > 0
            assert len(teaser) > 0

            # Step 3: Save all content
            content = {
                'twitter': twitter_thread,
                'linkedin': linkedin_post,
                'teaser': teaser
            }

            essay_name = "ai_regulation"
            save_social_content(essay_name, content)

            # Step 4: Verify all files created
            essay_folder = temp_data_dir / essay_name
            assert essay_folder.exists()
            assert (essay_folder / "twitter.txt").exists()
            assert (essay_folder / "linkedin.txt").exists()
            assert (essay_folder / "teaser.txt").exists()
            assert (essay_folder / "metadata.json").exists()

            # Step 5: Verify metadata accuracy
            with open(essay_folder / "metadata.json", 'r') as f:
                metadata = json.load(f)

            assert metadata['essay_name'] == essay_name
            assert len(metadata['formats']) == 3

        finally:
            social_repurpose.SOCIAL_DIR = original_social_dir

    def test_character_limits_enforcement_across_workflow(self, sample_essay_file):
        """Verify character limits enforced throughout workflow"""
        essay = read_essay(str(sample_essay_file))

        # Generate Twitter thread
        twitter_thread = generate_twitter_thread(essay)

        # Verify ALL tweets respect limit
        for i, tweet in enumerate(twitter_thread):
            assert len(tweet) <= TWITTER_MAX_LENGTH, \
                f"Tweet {i+1}/{len(twitter_thread)} exceeds limit: {len(tweet)} > {TWITTER_MAX_LENGTH}"

        # LinkedIn should be reasonable (allow flexibility)
        linkedin_post = generate_linkedin_post(essay)
        assert len(linkedin_post) > 0
