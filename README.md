# Strategic Tech Newsletter

A premium weekly newsletter delivering actionable insights on emerging technologies, strategic trends, and industry analysis for technical leaders and decision-makers.

**🎯 Automated with Claude Code:**  80% time reduction (15 hrs → 3 hrs/week)

## 🚀 Quick Start (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/codeswiftr/strategic-tech-newsletter.git
cd strategic-tech-newsletter

# 2. Install dependencies (using uv per project standards)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# 3. Configure environment variables
cp .env.example .env.local
# Edit .env.local with your API keys (see docs/SETUP_GUIDE.md)

# 4. Validate setup
python scripts/validate_setup.py

# 5. Test basic functionality
python scripts/research_sources.py --mode=trending --days=7
cat data/topic_trends.csv | tail -10
```

**📚 Full Documentation:**
- **Setup Guide:** [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) - Detailed API key setup
- **Workflows:** [docs/WORKFLOWS.md](docs/WORKFLOWS.md) - Weekly production routines
- **Guidelines:** [CLAUDE.md](CLAUDE.md) - Editorial standards and SOPs

## ✨ Features

- **Automated Research:** Discover trending topics from HN, Twitter, Reddit
- **Expert Sourcing:** Find and score credible sources (1-100 scale)
- **Fact-Checking:** Verify every claim before publication (100% accuracy)
- **Social Repurposing:** Generate LinkedIn, Twitter, Substack content
- **Analytics Tracking:** Monitor open rates, CTR, subscriber growth
- **Sponsor Management:** Prospect generation and pitch templates

## 📊 Test Suite

**120 tests, 77% coverage**
```bash
pytest tests/ -v
# ✅ 120 passed, 77% coverage
```

Coverage by script:
- analytics_report.py: 82%
- research_sources.py: 80%
- fact_check.py: 79%
- social_repurpose.py: 75%
- sponsor_outreach.py: 65%

## 🤖 Claude Code Skills

Three automated skills for Claude Code on the Web:

### 1. **Research Skill** (`.claude/skills/research/`)
- Find trending topics across platforms
- Identify expert sources with credibility scoring
- Generate outreach email templates

**Usage:**
```
Use research skill to find 10 trending AI topics from the past week.
Focus on enterprise applications and regulatory frameworks.
```

### 2. **Fact-Checker Skill** (`.claude/skills/fact_checker/`)
- Extract factual claims from drafts
- Cross-verify against trusted sources
- Add hyperlinked citations
- Flag unverifiable statements

**Usage:**
```
Use fact_checker skill on content/drafts/ai_regulation.md in strict mode.
Verify all claims and add citations.
```

### 3. **Social Repurpose Skill** (`.claude/skills/social_repurpose/`)
- Generate 7 LinkedIn variations for A/B testing
- Create Twitter threads (280 char limit enforced)
- Produce Substack Note teasers

**Usage:**
```
Use social_repurpose skill on content/essays/my_essay.md.
Generate all formats with professional tone.
```

## Project Structure

```
strategic-tech-newsletter/
├── .claude/
│   └── settings.json          # Claude Code automation hooks
├── CLAUDE.md                  # Newsletter guidelines + SOPs
├── scripts/
│   ├── research_sources.py    # Find trending topics & expert sources
│   ├── fact_check.py          # Validate claims against sources
│   ├── social_repurpose.py    # Generate social posts from essays
│   ├── analytics_report.py    # Weekly metrics + insights
│   └── sponsor_outreach.py    # Prospect generation + pitch templates
├── data/
│   ├── expert_database.json   # CRM of expert sources
│   ├── topic_trends.csv       # Trending topics across platforms
│   └── fact_check_library.json # Verified claims + citations
├── content/
│   ├── essays/                # Published essays
│   ├── drafts/                # Work-in-progress essays
│   └── social_posts/          # Generated social content
└── README.md                  # This file
```

## Weekly Workflow

### Monday: Topic Selection
1. Run trending topics analysis:
   ```bash
   python scripts/research_sources.py --mode=trending --days=7
   ```
2. Review `data/topic_trends.csv` for emerging patterns
3. Select topic with highest strategic value + novelty
4. Run deep research on selected topic:
   ```bash
   python scripts/research_sources.py --topic="Your Selected Topic" --depth=expert
   ```

### Tuesday-Wednesday: Research & Drafting
1. Compile sources from `data/expert_database.json`
2. Write first draft in `content/drafts/`
3. Structure: Hook → Context → Analysis → Predictions → Takeaways
4. Include inline citations: `[source_name](url)`

### Thursday: Fact-Checking
1. Run comprehensive fact-check:
   ```bash
   python scripts/fact_check.py --draft=content/drafts/your_essay.md --strict
   ```
2. Review flagged claims
3. Add missing citations or remove unverifiable claims
4. Re-run until passing

### Friday: Publication & Distribution
1. Move polished essay to `content/essays/`
2. Generate social content:
   ```bash
   python scripts/social_repurpose.py --essay=content/essays/your_essay.md --formats=all
   ```
3. Review generated content in `content/social_posts/your_essay/`
4. Publish via newsletter platform
5. Post social content

### Weekly Analytics Review
Every Monday, review performance:
```bash
python scripts/analytics_report.py --period=week --compare=true
```

## Script Reference

### research_sources.py

Find trending topics and research expert sources.

**Modes:**
- `--mode=trending`: Find hot topics across HN, Twitter, tech blogs
- `--topic="Topic Name"`: Deep-dive on specific topic

**Examples:**
```bash
# Find trending topics from last 7 days
python scripts/research_sources.py --mode=trending --days=7

# Deep research on specific topic
python scripts/research_sources.py --topic="AI regulation" --depth=expert
```

### fact_check.py

Validate claims against verified sources.

**Options:**
- `--draft=path`: Fact-check entire draft
- `--claim="claim"`: Verify single claim
- `--strict`: Fail on any unverified claims
- `--add --source=url`: Add verified claim to library

**Examples:**
```bash
# Validate all claims in draft (strict mode)
python scripts/fact_check.py --draft=content/drafts/essay.md --strict

# Verify single claim
python scripts/fact_check.py --claim="GPT-4 has 1.7T parameters"

# Add verified claim to library
python scripts/fact_check.py --claim="..." --source="https://..." --add
```

### social_repurpose.py

Generate social media content from published essays.

**Formats:**
- `twitter`: Thread optimized for Twitter (up to 10 tweets)
- `linkedin`: Long-form post with bullets
- `teaser`: Short newsletter teaser
- `all`: Generate all formats

**Examples:**
```bash
# Generate all social formats
python scripts/social_repurpose.py --essay=content/essays/ai_regulation.md --formats=all

# Twitter thread only
python scripts/social_repurpose.py --essay=content/essays/ai_regulation.md --formats=twitter
```

Output saved to: `content/social_posts/{essay_name}/`

### analytics_report.py

Track newsletter performance and subscriber metrics.

**Periods:**
- `--period=week`: Weekly performance
- `--period=month`: Monthly summary

**Output:**
- `--output=markdown`: Human-readable report
- `--output=json`: Structured data

**Examples:**
```bash
# Weekly report with week-over-week comparison
python scripts/analytics_report.py --period=week --compare=true

# Monthly summary
python scripts/analytics_report.py --period=month --output=markdown
```

### sponsor_outreach.py

Manage sponsor prospecting and pitch generation.

**Commands:**
- `--generate-prospects`: Create list of potential sponsors
- `--pitch --company="Name"`: Generate personalized pitch

**Templates:**
- `standard`: Comprehensive overview + metrics
- `data-driven`: Performance-focused, concise
- `value-first`: Thought leadership approach

**Examples:**
```bash
# Generate 20 sponsor prospects
python scripts/sponsor_outreach.py --generate-prospects --niche="developer-tools"

# Create pitch for specific company
python scripts/sponsor_outreach.py --pitch --company="Acme Corp" --template=data-driven

# Update prospect status
python scripts/sponsor_outreach.py --update-status=contacted --prospect-id=PROSPECT_20250120_001
```

## Quality Standards

Before publishing any essay, ensure:
- [ ] Minimum 5 credible sources cited
- [ ] All statistics verified via `fact_check.py`
- [ ] Original insights/predictions included
- [ ] Clear actionable takeaways
- [ ] Readability score 10-12 grade level
- [ ] Social posts generated and reviewed
- [ ] SEO keywords identified
- [ ] Internal links to previous essays (if relevant)

## Target Metrics

### Content Quality
- **Source credibility score**: >85/100
- **Fact-check pass rate**: 100%
- **Reading time**: 6-9 minutes
- **Original research**: 30%+ unique insights

### Engagement
- **Open rate**: >40%
- **Click-through rate**: >8%
- **Social shares**: >50 per essay
- **Average read time**: 6-9 minutes

### Growth
- **Subscriber growth**: >5% MoM
- **Retention rate**: >92%
- **Referral rate**: >10%

## Data Files

### expert_database.json
Expert sources CRM with contact info, expertise, and credibility scores.

**Update after each essay**: Add new experts discovered during research.

**Fields:**
- `name`: Expert's full name
- `expertise`: Array of expertise areas
- `twitter_handle`: Twitter username
- `email`: Contact email
- `affiliation`: Company/institution
- `credibility_score`: 0-100 based on publications, citations, experience

### topic_trends.csv
Trending topics scraped from HN, Twitter, tech blogs.

**Auto-updated** by `research_sources.py --mode=trending`

**Columns:**
- `date`: Trend discovery date
- `topic`: Topic description
- `source_platform`: Where it's trending
- `engagement_score`: Relative popularity
- `url`: Source URL

### fact_check_library.json
Verified claims with source citations for reuse.

**Updated** after each fact-checking session.

**Use cases:**
- Quick validation of recurring claims
- Source reference for new essays
- Building authority through citation consistency

## Monthly Sponsor Workflow

**First Monday of Month:**
```bash
# Generate new prospects based on newsletter niche
python scripts/sponsor_outreach.py --generate-prospects --niche="developer-tools"

# Review generated prospects in data/sponsor_pipeline.json
# Select top 5 prospects by fit score

# Generate personalized pitches
python scripts/sponsor_outreach.py --pitch --company="Prospect 1" --template=data-driven
python scripts/sponsor_outreach.py --pitch --company="Prospect 2" --template=value-first

# Track outreach in sponsor_pipeline.json
```

## Troubleshooting

### Fact-check failing?
- Review flagged claims in detail
- Find alternative sources or remove claim
- Add verified claims to `fact_check_library.json` for future use
- Re-run until passing

### Low engagement?
- Review `analytics_report.py` output for patterns
- Analyze top-performing essays for common elements
- A/B test subject lines and hooks
- Adjust content strategy based on data

### Need more sources?
- Expand `expert_database.json` with new experts
- Run `research_sources.py` with different niches
- Follow Twitter lists of industry leaders
- Monitor academic paper releases (arXiv, Google Scholar)

## Git Workflow

### Branch Strategy
- `main`: Published essays only
- `draft/{topic-slug}`: Work-in-progress essays

### Commit After:
- Publishing each essay
- Weekly analytics run
- Significant data updates
- Script improvements

### Never Commit:
- Incomplete drafts to main
- Unverified claims
- API keys or credentials

## Dependencies

Install via `uv` (per project standards):

```bash
# Core dependencies
uv pip install requests beautifulsoup4 feedparser pandas

# Optional (for advanced features)
uv pip install tweepy openai anthropic
```

### API Keys Required (Optional)

For full functionality, configure:
- **OpenAI API**: Content analysis and repurposing
- **Twitter API**: Trend monitoring
- **Newsletter Platform API**: Substack/Ghost/Beehiiv analytics

## Support & Contribution

### For Questions:
- Review `CLAUDE.md` for detailed guidelines
- Check script docstrings: `python scripts/script_name.py --help`

### For Improvements:
- Add new pitch templates to `sponsor_outreach.py`
- Expand fact-check patterns in `fact_check.py`
- Improve social content generation in `social_repurpose.py`

## Next Steps

1. **First-Time Setup:**
   ```bash
   # Install dependencies
   uv pip install requests beautifulsoup4 feedparser pandas

   # Test scripts
   python scripts/research_sources.py --mode=trending --days=7
   ```

2. **Write Your First Essay:**
   - Select topic from trends
   - Research experts
   - Draft in `content/drafts/`
   - Fact-check thoroughly
   - Publish and promote

3. **Build Your Routine:**
   - Follow weekly workflow
   - Track metrics religiously
   - Refine based on data
   - Grow strategically

Happy writing! 📝
