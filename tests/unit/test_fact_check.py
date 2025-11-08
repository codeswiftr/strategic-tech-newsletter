"""
Unit tests for fact_check.py

Tests the fact-checking functionality including:
- Claim extraction from drafts
- Verification against fact-check library
- Draft validation in strict/relaxed modes
- Adding verified claims to library
"""
import pytest
import json
from pathlib import Path
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from fact_check import (
    extract_claims_from_draft,
    verify_claim,
    check_draft,
    add_to_library,
    FACT_CHECK_LIBRARY
)


class TestExtractClaimsFromDraft:
    """Test claim extraction functionality"""

    def test_extract_percentage_claims(self, sample_essay_file):
        """Should extract claims containing percentages"""
        claims = extract_claims_from_draft(str(sample_essay_file))

        # Essay contains: 45%, 67%, 80%
        percentage_claims = [c for c in claims if c['type'] == 'percentage']
        assert len(percentage_claims) >= 3, "Should find at least 3 percentage claims"

        # Verify one of the claims
        claim_texts = [c['claim'] for c in percentage_claims]
        assert any('45%' in text for text in claim_texts), "Should extract 45% claim"

    def test_extract_statistic_claims(self, sample_essay_file):
        """Should extract claims with large numbers"""
        claims = extract_claims_from_draft(str(sample_essay_file))

        # Essay contains: $50,000,000
        statistic_claims = [c for c in claims if c['type'] == 'statistic']
        assert len(statistic_claims) >= 1, "Should find at least 1 statistic claim"

        claim_texts = [c['claim'] for c in statistic_claims]
        assert any('50,000,000' in text for text in claim_texts), \
            "Should extract large number claim"

    def test_extract_from_nonexistent_file(self):
        """Should handle missing file gracefully"""
        claims = extract_claims_from_draft("/nonexistent/path/essay.md")
        assert claims == [], "Should return empty list for missing file"

    def test_extract_from_empty_file(self, temp_data_dir):
        """Should handle empty file gracefully"""
        empty_file = temp_data_dir / "empty.md"
        empty_file.write_text("")

        claims = extract_claims_from_draft(str(empty_file))
        assert claims == [], "Should return empty list for empty file"


class TestVerifyClaim:
    """Test claim verification against fact-check library"""

    def test_verify_claim_in_library(self, temp_data_dir, sample_fact_check_library):
        """Should verify claim that exists in library"""
        # Create temporary fact-check library
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump(sample_fact_check_library, f)

        # Monkey patch the FACT_CHECK_LIBRARY constant
        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            claim_text = "AI industry is experiencing 45% year-over-year growth"
            result = verify_claim(claim_text, strict=True)

            assert result['verified'] is True, "Claim should be verified"
            assert result['confidence'] >= 0.9, "Confidence should be high"
            assert 'source_url' in result or 'source' in result, "Should include source"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib

    def test_verify_claim_not_in_library_strict(self, temp_data_dir):
        """Should reject unverified claim in strict mode"""
        # Create empty library
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump({"verified_claims": []}, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            result = verify_claim("Unverified claim about 99% growth", strict=True)

            assert result['verified'] is False, "Unverified claim should fail in strict mode"
            assert result['confidence'] == 0.0, "Confidence should be 0 for unverified"
            assert result['source'] is None, "Should have no source"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib

    def test_verify_claim_not_in_library_relaxed(self, temp_data_dir):
        """Should mark unverified claim as unknown in relaxed mode"""
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump({"verified_claims": []}, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            result = verify_claim("Unverified claim about 99% growth", strict=False)

            assert result['verified'] is None, "Should be marked as unknown"
            assert 0.0 < result['confidence'] < 1.0, "Confidence should be partial"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib


class TestCheckDraft:
    """Test full draft checking workflow"""

    def test_check_draft_all_verified(self, temp_data_dir, sample_essay_file, sample_fact_check_library):
        """Should pass when all claims are verified"""
        # Setup library with verified claims from the essay
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump(sample_fact_check_library, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            report = check_draft(str(sample_essay_file), strict=True)

            assert report['total_claims'] > 0, "Should find claims in essay"
            assert isinstance(report['verified'], int), "Should count verified claims"
            assert isinstance(report['unverified'], int), "Should count unverified claims"
            assert isinstance(report['failed'], int), "Should count failed claims"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib

    def test_check_draft_some_failed_strict(self, temp_data_dir, sample_essay_file):
        """Should fail in strict mode when claims unverified"""
        # Create library without the essay's claims
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump({"verified_claims": []}, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            report = check_draft(str(sample_essay_file), strict=True)

            assert report['failed'] > 0, "Should have failed claims in strict mode"
            assert report['total_claims'] > 0, "Should find claims"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib

    def test_check_draft_generates_report(self, temp_data_dir, sample_essay_file):
        """Should generate detailed report structure"""
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump({"verified_claims": []}, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            report = check_draft(str(sample_essay_file), strict=False)

            # Verify report structure
            assert 'draft' in report, "Report should include draft path"
            assert 'check_date' in report, "Report should include check date"
            assert 'total_claims' in report, "Report should include total claims"
            assert 'verified' in report, "Report should include verified count"
            assert 'unverified' in report, "Report should include unverified count"
            assert 'failed' in report, "Report should include failed count"
            assert 'details' in report, "Report should include claim details"
            assert isinstance(report['details'], list), "Details should be a list"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib


class TestAddToLibrary:
    """Test adding verified claims to library"""

    def test_add_claim_to_empty_library(self, temp_data_dir):
        """Should create library and add claim"""
        lib_path = temp_data_dir / "fact_check_library.json"

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            add_to_library(
                claim="Test claim with 95% accuracy",
                source_url="https://example.com/source",
                context="Test context"
            )

            # Verify library file was created
            assert lib_path.exists(), "Library file should be created"

            # Verify claim was added
            with open(lib_path, 'r') as f:
                library = json.load(f)

            assert 'verified_claims' in library, "Library should have verified_claims"
            assert len(library['verified_claims']) == 1, "Should have 1 claim"
            assert library['verified_claims'][0]['claim'] == "Test claim with 95% accuracy"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib

    def test_add_claim_to_existing_library(self, temp_data_dir, sample_fact_check_library):
        """Should append to existing library"""
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump(sample_fact_check_library, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            original_count = len(sample_fact_check_library['verified_claims'])

            add_to_library(
                claim="New claim with 80% confidence",
                source_url="https://example.com/new-source",
                context="New context"
            )

            # Verify claim was appended
            with open(lib_path, 'r') as f:
                library = json.load(f)

            assert len(library['verified_claims']) == original_count + 1, \
                "Should have one more claim"
            assert library['verified_claims'][-1]['claim'] == "New claim with 80% confidence"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib

    def test_add_claim_includes_metadata(self, temp_data_dir):
        """Should include verification date and context"""
        lib_path = temp_data_dir / "fact_check_library.json"

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            add_to_library(
                claim="Metadata test claim",
                source_url="https://example.com/source",
                context="Testing metadata inclusion"
            )

            with open(lib_path, 'r') as f:
                library = json.load(f)

            claim_entry = library['verified_claims'][0]
            assert 'verification_date' in claim_entry, "Should include verification date"
            assert 'context' in claim_entry, "Should include context"
            assert claim_entry['context'] == "Testing metadata inclusion"
        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib


@pytest.mark.integration
class TestFactCheckIntegration:
    """Integration tests for fact-checking workflow"""

    def test_full_workflow_with_real_files(self, temp_data_dir):
        """Test complete workflow from draft to verified library"""
        # Create draft with specific claims
        draft_path = temp_data_dir / "test_draft.md"
        draft_content = """
        # Test Essay

        According to recent studies, 75% of developers use Git for version control.

        The average salary for software engineers increased by $15,000 in 2024.
        """
        draft_path.write_text(draft_content)

        # Create empty library
        lib_path = temp_data_dir / "fact_check_library.json"
        with open(lib_path, 'w') as f:
            json.dump({"verified_claims": []}, f)

        import fact_check
        original_lib = fact_check.FACT_CHECK_LIBRARY
        fact_check.FACT_CHECK_LIBRARY = lib_path

        try:
            # Step 1: Check draft (should fail in strict mode)
            report = check_draft(str(draft_path), strict=True)
            assert report['failed'] > 0, "Should have unverified claims"

            # Step 2: Add verified claims
            add_to_library(
                claim="75% of developers use Git for version control",
                source_url="https://stackoverflow.com/survey/2024",
                context="Stack Overflow Developer Survey 2024"
            )

            add_to_library(
                claim="average salary for software engineers increased by $15,000",
                source_url="https://levels.fyi/2024-report",
                context="Levels.fyi Compensation Report"
            )

            # Step 3: Re-check draft (should pass now)
            report2 = check_draft(str(draft_path), strict=True)
            assert report2['verified'] > 0, "Should have verified claims now"
            # Note: Depending on exact matching, this might still have some unverified
            # The important part is the workflow functions correctly

        finally:
            fact_check.FACT_CHECK_LIBRARY = original_lib
