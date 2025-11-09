"""
Unit tests for sponsor_outreach.py

Tests sponsor management including:
- Prospect generation and scoring
- Pitch template creation
- Pipeline management and status updates
- Contact information handling
"""
import pytest
import json
from pathlib import Path
from datetime import datetime
import sys

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from sponsor_outreach import (
    load_sponsor_pipeline,
    save_sponsor_pipeline,
    generate_prospects,
    create_pitch,
    update_prospect_status,
    SPONSOR_PIPELINE
)


class TestLoadSponsorPipeline:
    """Test loading sponsor pipeline data"""

    def test_load_sponsor_pipeline_existing_file(self, temp_data_dir):
        """Should load existing pipeline data"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        sample_pipeline = {
            "prospects": [
                {
                    "id": "PROSPECT_001",
                    "company_name": "Test Company",
                    "status": "prospect"
                }
            ],
            "active": [],
            "closed": [],
            "last_updated": "2025-01-20"
        }

        with open(pipeline_file, 'w') as f:
            json.dump(sample_pipeline, f)

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            pipeline = load_sponsor_pipeline()

            assert 'prospects' in pipeline
            assert 'active' in pipeline
            assert 'closed' in pipeline
            assert len(pipeline['prospects']) == 1
            assert pipeline['prospects'][0]['company_name'] == "Test Company"

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_load_sponsor_pipeline_missing_file(self, temp_data_dir):
        """Should return default structure for missing file"""
        pipeline_file = temp_data_dir / "nonexistent.json"

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            pipeline = load_sponsor_pipeline()

            # Should return default structure
            assert 'prospects' in pipeline
            assert 'active' in pipeline
            assert 'closed' in pipeline
            assert pipeline['prospects'] == []
            assert pipeline['active'] == []
            assert pipeline['closed'] == []

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_load_sponsor_pipeline_structure(self):
        """Should have correct data structure"""
        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        temp_file = Path("/tmp/test_pipeline.json")
        sponsor_outreach.SPONSOR_PIPELINE = temp_file

        try:
            pipeline = load_sponsor_pipeline()

            assert isinstance(pipeline, dict)
            assert isinstance(pipeline['prospects'], list)
            assert isinstance(pipeline['active'], list)
            assert isinstance(pipeline['closed'], list)

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline
            if temp_file.exists():
                temp_file.unlink()


class TestSaveSponsorPipeline:
    """Test saving sponsor pipeline data"""

    def test_save_sponsor_pipeline_creates_file(self, temp_data_dir):
        """Should create pipeline file"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            pipeline_data = {
                "prospects": [],
                "active": [],
                "closed": [],
                "last_updated": None
            }

            save_sponsor_pipeline(pipeline_data)

            assert pipeline_file.exists(), "Should create file"

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_save_sponsor_pipeline_updates_timestamp(self, temp_data_dir):
        """Should update last_updated timestamp"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            pipeline_data = {
                "prospects": [],
                "active": [],
                "closed": [],
                "last_updated": None
            }

            save_sponsor_pipeline(pipeline_data)

            with open(pipeline_file, 'r') as f:
                saved_data = json.load(f)

            assert saved_data['last_updated'] is not None
            # Should be ISO format
            datetime.fromisoformat(saved_data['last_updated'])

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_save_sponsor_pipeline_preserves_data(self, temp_data_dir):
        """Should preserve all pipeline data"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            pipeline_data = {
                "prospects": [
                    {"id": "001", "company_name": "Company A"},
                    {"id": "002", "company_name": "Company B"}
                ],
                "active": [
                    {"id": "003", "company_name": "Company C"}
                ],
                "closed": [],
                "last_updated": None
            }

            save_sponsor_pipeline(pipeline_data)

            with open(pipeline_file, 'r') as f:
                saved_data = json.load(f)

            assert len(saved_data['prospects']) == 2
            assert len(saved_data['active']) == 1
            assert saved_data['prospects'][0]['company_name'] == "Company A"

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline


class TestGenerateProspects:
    """Test prospect generation"""

    def test_generate_prospects_basic(self):
        """Should generate prospects with correct structure"""
        prospects = generate_prospects("developer-tools", count=5)

        assert isinstance(prospects, list)
        assert len(prospects) > 0
        assert len(prospects) <= 5

    def test_generate_prospects_structure(self):
        """Should generate properly structured prospects"""
        prospects = generate_prospects("developer-tools", count=1)

        prospect = prospects[0]
        required_fields = [
            'id', 'company_name', 'category', 'website',
            'estimated_budget', 'fit_score', 'contact_info', 'status', 'added_date'
        ]

        for field in required_fields:
            assert field in prospect, f"Should have {field} field"

    def test_generate_prospects_unique_ids(self):
        """Should generate unique IDs for prospects"""
        prospects = generate_prospects("ai-ml", count=10)

        ids = [p['id'] for p in prospects]
        assert len(ids) == len(set(ids)), "All IDs should be unique"

    def test_generate_prospects_fit_scores(self):
        """Should assign fit scores within valid range"""
        prospects = generate_prospects("devops", count=10)

        for prospect in prospects:
            assert 'fit_score' in prospect
            assert 0 <= prospect['fit_score'] <= 100

    def test_generate_prospects_status_is_prospect(self):
        """Should set initial status to 'prospect'"""
        prospects = generate_prospects("web3", count=5)

        for prospect in prospects:
            assert prospect['status'] == 'prospect'

    def test_generate_prospects_has_contact_info(self):
        """Should include contact information"""
        prospects = generate_prospects("developer-tools", count=1)

        prospect = prospects[0]
        assert 'contact_info' in prospect
        assert 'marketing_email' in prospect['contact_info']
        assert 'linkedin' in prospect['contact_info']

    def test_generate_prospects_respects_count(self):
        """Should respect requested count parameter"""
        for count in [1, 5, 10, 20]:
            prospects = generate_prospects("developer-tools", count=count)
            assert len(prospects) <= count

    def test_generate_prospects_different_niches(self):
        """Should handle different niche categories"""
        niches = ['developer-tools', 'ai-ml', 'devops', 'web3']

        for niche in niches:
            prospects = generate_prospects(niche, count=3)
            assert len(prospects) > 0


class TestCreatePitch:
    """Test pitch creation"""

    def test_create_pitch_standard_template(self):
        """Should create pitch using standard template"""
        pitch = create_pitch("Test Company", template='standard')

        assert isinstance(pitch, str)
        assert len(pitch) > 0
        assert "Test Company" in pitch

    def test_create_pitch_data_driven_template(self):
        """Should create data-driven pitch"""
        pitch = create_pitch("Acme Corp", template='data-driven')

        assert isinstance(pitch, str)
        assert "Acme Corp" in pitch
        # Data-driven should mention metrics
        assert any(metric in pitch for metric in ['%', 'subscribers', 'engagement'])

    def test_create_pitch_value_first_template(self):
        """Should create value-first pitch"""
        pitch = create_pitch("Example Inc", template='value-first')

        assert isinstance(pitch, str)
        assert "Example Inc" in pitch

    def test_create_pitch_includes_newsletter_metrics(self):
        """Should include newsletter metrics in pitch"""
        pitch = create_pitch("Test Co", template='standard')

        # Should mention subscriber count, open rate, CTR
        assert any(metric in pitch.lower() for metric in [
            'subscribers', 'open rate', 'click', 'engagement'
        ])

    def test_create_pitch_has_cta(self):
        """Should include call-to-action"""
        pitch = create_pitch("Test Company", template='standard')

        # Should have next steps or CTA
        pitch_lower = pitch.lower()
        assert any(cta in pitch_lower for cta in [
            'call', 'discuss', 'next steps', 'schedule', 'questions'
        ])

    def test_create_pitch_subject_line(self):
        """Should include subject line"""
        pitch = create_pitch("Test Co", template='standard')

        assert 'Subject:' in pitch or 'subject:' in pitch.lower()

    def test_create_pitch_custom_data(self):
        """Should allow custom data insertion"""
        custom_data = {
            'COMPANY_CATEGORY': 'Developer Tools',
            'UPCOMING_TOPIC': 'AI in Software Development'
        }

        pitch = create_pitch("Test Co", template='value-first', custom_data=custom_data)

        # Custom data might be inserted
        assert isinstance(pitch, str)


class TestUpdateProspectStatus:
    """Test prospect status updates"""

    def test_update_prospect_status_basic(self, temp_data_dir):
        """Should update prospect status"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        # Create initial pipeline
        initial_pipeline = {
            "prospects": [
                {
                    "id": "PROSPECT_001",
                    "company_name": "Test Co",
                    "status": "prospect"
                }
            ],
            "active": [],
            "closed": [],
            "last_updated": None
        }

        with open(pipeline_file, 'w') as f:
            json.dump(initial_pipeline, f)

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            update_prospect_status("PROSPECT_001", "contacted", notes="Initial outreach")

            # Verify status updated
            with open(pipeline_file, 'r') as f:
                updated_pipeline = json.load(f)

            # Find the prospect
            all_prospects = (
                updated_pipeline['prospects'] +
                updated_pipeline['active'] +
                updated_pipeline['closed']
            )

            prospect = next((p for p in all_prospects if p['id'] == "PROSPECT_001"), None)
            assert prospect is not None
            assert prospect['status'] == 'contacted'

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_update_prospect_status_moves_to_active(self, temp_data_dir):
        """Should move prospect to active list when status is active"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        initial_pipeline = {
            "prospects": [
                {"id": "PROSPECT_001", "company_name": "Test Co", "status": "prospect"}
            ],
            "active": [],
            "closed": []
        }

        with open(pipeline_file, 'w') as f:
            json.dump(initial_pipeline, f)

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            update_prospect_status("PROSPECT_001", "active")

            with open(pipeline_file, 'r') as f:
                updated_pipeline = json.load(f)

            # Should be in active list
            assert len(updated_pipeline['active']) == 1
            assert updated_pipeline['active'][0]['id'] == "PROSPECT_001"
            # Should be removed from prospects
            assert len(updated_pipeline['prospects']) == 0

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_update_prospect_status_adds_notes(self, temp_data_dir):
        """Should add notes to prospect"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        initial_pipeline = {
            "prospects": [
                {"id": "PROSPECT_001", "company_name": "Test Co", "status": "prospect"}
            ],
            "active": [],
            "closed": []
        }

        with open(pipeline_file, 'w') as f:
            json.dump(initial_pipeline, f)

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            update_prospect_status("PROSPECT_001", "contacted", notes="Sent initial email")

            with open(pipeline_file, 'r') as f:
                updated_pipeline = json.load(f)

            prospect = updated_pipeline['prospects'][0]
            assert 'notes' in prospect
            assert len(prospect['notes']) > 0
            assert prospect['notes'][0]['note'] == "Sent initial email"
            assert 'date' in prospect['notes'][0]

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_update_prospect_status_nonexistent_id(self, temp_data_dir, capsys):
        """Should handle nonexistent prospect ID gracefully"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        initial_pipeline = {
            "prospects": [],
            "active": [],
            "closed": []
        }

        with open(pipeline_file, 'w') as f:
            json.dump(initial_pipeline, f)

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            update_prospect_status("NONEXISTENT_ID", "active")

            captured = capsys.readouterr()
            assert "not found" in captured.out.lower()

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_update_prospect_status_updates_timestamp(self, temp_data_dir):
        """Should update last_updated timestamp"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        initial_pipeline = {
            "prospects": [
                {"id": "PROSPECT_001", "company_name": "Test Co", "status": "prospect"}
            ],
            "active": [],
            "closed": []
        }

        with open(pipeline_file, 'w') as f:
            json.dump(initial_pipeline, f)

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            update_prospect_status("PROSPECT_001", "contacted")

            with open(pipeline_file, 'r') as f:
                updated_pipeline = json.load(f)

            prospect = updated_pipeline['prospects'][0]
            assert 'last_updated' in prospect
            # Should be ISO format timestamp
            datetime.fromisoformat(prospect['last_updated'])

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline


@pytest.mark.integration
class TestSponsorOutreachIntegration:
    """Integration tests for sponsor outreach workflow"""

    def test_full_sponsor_workflow(self, temp_data_dir):
        """Test complete workflow: generate → pitch → update status"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            # Step 1: Generate prospects
            prospects = generate_prospects("developer-tools", count=5)
            assert len(prospects) == 5

            # Step 2: Save to pipeline
            pipeline = load_sponsor_pipeline()
            pipeline['prospects'].extend(prospects)
            save_sponsor_pipeline(pipeline)

            # Step 3: Create pitch for top prospect
            top_prospect = sorted(prospects, key=lambda x: x['fit_score'], reverse=True)[0]
            pitch = create_pitch(top_prospect['company_name'], template='data-driven')
            assert len(pitch) > 0

            # Step 4: Update status to contacted
            update_prospect_status(top_prospect['id'], 'contacted', notes="Sent pitch email")

            # Step 5: Verify pipeline updated
            updated_pipeline = load_sponsor_pipeline()
            contacted_prospect = next(
                (p for p in updated_pipeline['prospects'] if p['id'] == top_prospect['id']),
                None
            )
            assert contacted_prospect is not None
            assert contacted_prospect['status'] == 'contacted'

            # Step 6: Move to active
            update_prospect_status(top_prospect['id'], 'active')

            # Verify moved to active list
            final_pipeline = load_sponsor_pipeline()
            assert len(final_pipeline['active']) == 1
            assert final_pipeline['active'][0]['id'] == top_prospect['id']

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline

    def test_prospect_lifecycle(self, temp_data_dir):
        """Test prospect moving through pipeline stages"""
        pipeline_file = temp_data_dir / "sponsor_pipeline.json"

        import sponsor_outreach
        original_pipeline = sponsor_outreach.SPONSOR_PIPELINE
        sponsor_outreach.SPONSOR_PIPELINE = pipeline_file

        try:
            # Create prospect
            prospects = generate_prospects("ai-ml", count=1)
            prospect = prospects[0]

            # Save to pipeline
            pipeline = load_sponsor_pipeline()
            pipeline['prospects'].append(prospect)
            save_sponsor_pipeline(pipeline)

            # Lifecycle: prospect → contacted → negotiating → active → closed
            statuses = ['contacted', 'negotiating', 'active', 'closed']

            for status in statuses:
                update_prospect_status(prospect['id'], status, notes=f"Moving to {status}")

                # Verify status
                updated_pipeline = load_sponsor_pipeline()
                all_prospects = (
                    updated_pipeline['prospects'] +
                    updated_pipeline['active'] +
                    updated_pipeline['closed']
                )
                current_prospect = next((p for p in all_prospects if p['id'] == prospect['id']), None)
                assert current_prospect is not None
                assert current_prospect['status'] == status

        finally:
            sponsor_outreach.SPONSOR_PIPELINE = original_pipeline
