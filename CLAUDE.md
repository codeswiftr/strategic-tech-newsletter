# CLAUDE.md

This file provides guidance to Claude Code when working with the Strategic Tech Newsletter project.

## Newsletter Overview
Strategic Tech Newsletter is a premium weekly publication delivering actionable insights on emerging technologies, strategic trends, and industry analysis for decision-makers.

## Editorial Guidelines

### Voice & Style
- **Tone**: Authoritative yet accessible, data-driven but conversational
- **Audience**: Technical leaders, CTOs, strategic thinkers, tech investors
- **Length**: 1200-1800 words per essay
- **Format**: Deep-dive analysis with clear takeaways
- **Citation Standard**: All claims must link to primary sources

### Quality Standards
- **Fact-checking**: Every statistical claim verified via `fact_check.py`
- **Source diversity**: Minimum 5 expert sources per essay
- **Original research**: 30%+ unique insights (not just synthesis)
- **Timeliness**: Published within 72 hours of trend emergence
- **Readability**: Grade 10-12 reading level (Flesch-Kincaid)

## Standard Operating Procedures (SOPs)

### Essay Production Workflow
1. **Topic Selection** (Monday)
   - Run `scripts/research_sources.py --mode=trending` to identify hot topics
   - Review `data/topic_trends.csv` for emerging patterns
   - Select topic with highest strategic value + novelty score

2. **Research Phase** (Monday-Tuesday)
   - Scrape expert opinions via `research_sources.py --topic="selected_topic"`
   - Update `data/expert_database.json` with new sources
   - Compile preliminary bibliography (minimum 10 sources)

3. **Draft Creation** (Wednesday)
   - Write first draft in `content/drafts/`
   - Structure: Hook → Context → Analysis → Predictions → Takeaways
   - Include inline citations with `[source_name](url)` format

4. **Fact-Checking** (Thursday)
   - Run `scripts/fact_check.py --draft=filename.md`
   - Verify all statistics against `data/fact_check_library.json`
   - Add missing citations or remove unverifiable claims

5. **Finalization** (Friday)
   - Move polished essay to `content/essays/`
   - Run `scripts/social_repurpose.py --essay=filename.md`
   - Generate Twitter thread, LinkedIn post, and newsletter teaser
   - Output saved to `content/social_posts/`

6. **Distribution** (Friday afternoon)
   - Publish via newsletter platform (Substack/Ghost/Beehiiv)
   - Post social content from `content/social_posts/`
   - Schedule follow-up engagement posts

### Monthly Sponsor Outreach
- **First Monday of month**: Run `scripts/sponsor_outreach.py --generate-prospects`
- **Target criteria**: B2B SaaS, developer tools, cloud infrastructure companies
- **Pitch template**: Data-driven with subscriber demographics + engagement metrics
- **Track in**: `data/sponsor_pipeline.json` (create if needed)

### Analytics Review
- **Every Monday**: Run `scripts/analytics_report.py --period=week`
- **Track metrics**: Open rate, click-through rate, subscriber growth, top-performing topics
- **Action items**: Adjust content strategy based on engagement patterns

## Python Script Usage

### research_sources.py
```bash
# Find trending topics across HN, Twitter, tech blogs
python scripts/research_sources.py --mode=trending --days=7

# Deep-dive on specific topic
python scripts/research_sources.py --topic="AI regulation" --depth=expert
```

### fact_check.py
```bash
# Validate all claims in draft
python scripts/fact_check.py --draft=content/drafts/essay_draft.md --strict

# Check specific claim
python scripts/fact_check.py --claim="GPT-4 has 1.7T parameters"
```

### social_repurpose.py
```bash
# Generate all social formats from essay
python scripts/social_repurpose.py --essay=content/essays/ai_regulation.md --formats=all

# Twitter thread only
python scripts/social_repurpose.py --essay=content/essays/ai_regulation.md --formats=twitter
```

### analytics_report.py
```bash
# Weekly performance report
python scripts/analytics_report.py --period=week --output=markdown

# Compare to previous month
python scripts/analytics_report.py --period=month --compare=true
```

### sponsor_outreach.py
```bash
# Generate prospect list based on newsletter niche
python scripts/sponsor_outreach.py --generate-prospects --niche="developer-tools"

# Create personalized pitch for prospect
python scripts/sponsor_outreach.py --pitch --company="Acme Corp" --template=standard
```

## Content Quality Checklist

Before publishing any essay, verify:
- [ ] Minimum 5 credible sources cited
- [ ] All statistics verified via fact_check.py
- [ ] Original insights/predictions included
- [ ] Clear actionable takeaways
- [ ] Readability score 10-12 grade level
- [ ] Social posts generated and reviewed
- [ ] SEO keywords identified
- [ ] Internal links to previous essays (if relevant)

## Data Management

### expert_database.json
- **Purpose**: CRM of expert sources, journalists, researchers
- **Fields**: name, expertise, twitter_handle, email, last_contacted, topics
- **Update frequency**: After each essay (add new sources)

### topic_trends.csv
- **Purpose**: Track emerging topics and their trajectory
- **Fields**: date, topic, source_platform, engagement_score, relevance_score
- **Update frequency**: Daily automated scraping

### fact_check_library.json
- **Purpose**: Verified claims with citations for reuse
- **Fields**: claim, source_url, verification_date, context
- **Update frequency**: After each fact-checking session

## Autonomous Operation Guidelines

### Automated Tasks (No Human Gate Required)
- Running research scripts for topic discovery
- Fact-checking against established sources
- Generating social media content from approved essays
- Weekly analytics reporting
- Updating expert database with new sources

### Human Review Required
- Final essay approval before publication
- Sponsor outreach pitch customization
- Editorial calendar adjustments
- New source vetting (first-time citations)
- Controversial claims or predictions

## Common Commands

```bash
# Full essay production workflow
python scripts/research_sources.py --mode=trending
# [Select topic manually]
python scripts/research_sources.py --topic="selected_topic" --depth=expert
# [Write draft in content/drafts/]
python scripts/fact_check.py --draft=content/drafts/essay.md --strict
# [Revise based on fact-check results]
python scripts/social_repurpose.py --essay=content/essays/essay.md --formats=all

# Weekly maintenance
python scripts/analytics_report.py --period=week
# Review data/topic_trends.csv for patterns

# Monthly sponsor pipeline
python scripts/sponsor_outreach.py --generate-prospects --niche="devtools"
```

## Git Workflow

### Branch Strategy
- `main`: Published essays only
- `draft/{topic-slug}`: Work-in-progress essays
- `feature/{script-name}`: Script improvements

### Commit Conventions
- `essay: Title of essay` - New published essay
- `draft: Working on {topic}` - Draft updates
- `data: Update expert database` - Data file updates
- `script: Improve fact-checking logic` - Script enhancements

### Auto-Commit Rules
- Commit after each essay publication
- Commit after weekly analytics run
- Commit after significant data updates
- Never commit incomplete drafts to main

## Performance Metrics

### Newsletter KPIs
- **Target open rate**: >40%
- **Target click-through rate**: >8%
- **Subscriber growth**: >5% MoM
- **Engagement score**: Comments + shares per issue

### Content Quality Metrics
- **Source credibility score**: >85/100
- **Fact-check pass rate**: 100%
- **Reading time**: 6-9 minutes
- **Social amplification**: >50 shares per essay

## Tool Integration

### Required Python Dependencies
```bash
# Install via uv (per user's global CLAUDE.md preference)
uv pip install requests beautifulsoup4 feedparser tweepy pandas openai
```

### API Keys Required
- OpenAI API (for content analysis and repurposing)
- Twitter API (for trend monitoring)
- Newsletter platform API (Substack/Ghost/Beehiiv)
- Analytics API (if using third-party analytics)

## Emergency Protocols

### If Fact-Check Fails Pre-Publication
1. **STOP publication immediately**
2. Review flagged claims in detail
3. Find alternative sources or remove claim
4. Re-run fact_check.py until pass
5. Only then proceed to publication

### If Sponsor Pitch Goes Wrong
1. Document issue in sponsor_pipeline.json
2. Escalate to human for damage control
3. Review pitch template for improvements
4. Update outreach.py logic if systematic issue

## Continuous Improvement

### Weekly Retrospective Questions
1. Which essay had highest engagement? Why?
2. Which sources provided most valuable insights?
3. Were there any fact-check failures? Root cause?
4. How can research process be optimized?
5. What topics are trending that we haven't covered?

### Monthly Strategy Review
1. Analyze analytics_report.py output for patterns
2. Adjust editorial calendar based on engagement
3. Refresh expert_database.json (remove stale sources)
4. Update social_repurpose.py templates based on performance
5. Review sponsor pipeline and optimize targeting
