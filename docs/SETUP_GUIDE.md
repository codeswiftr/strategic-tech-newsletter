# Strategic Tech Newsletter - Setup Guide

Complete guide to setting up your newsletter automation system in Claude Code on the Web.

## Prerequisites

- Python 3.11+ installed
- `uv` package manager ([installation guide](https://github.com/astral-sh/uv))
- GitHub account (repository already created)
- Newsletter platform account (Substack, Ghost, or Beehiiv)

## Quick Start (5 Minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/codeswiftr/strategic-tech-newsletter.git
cd strategic-tech-newsletter
```

### 2. Install Dependencies

```bash
# Create virtual environment and install all dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local with your API keys (see API Setup section below)
```

### 4. Validate Setup

```bash
# Run validation script
python scripts/validate_setup.py

# Run tests to verify everything works
pytest tests/ -v
```

### 5. Test Basic Functionality

```bash
# Fetch trending topics from Hacker News
python scripts/research_sources.py --mode=trending --days=7

# Check the output
cat data/topic_trends.csv
```

---

## API Key Setup

### Required APIs (Core Functionality)

#### 1. Hacker News API
**Cost:** Free
**Purpose:** Fetch trending tech topics

**Setup:**
- No API key required!
- API endpoint: `https://hacker-news.firebaseio.com/v0`
- Rate limit: Reasonable usage allowed
- Already integrated and working ✅

#### 2. Newsletter Platform API

Choose one based on your platform:

**Option A: Substack**
1. Go to https://substack.com/settings
2. Navigate to Settings → API
3. Click "Generate new API token"
4. Copy token to `.env.local`:
   ```
   SUBSTACK_API_TOKEN=your_token_here
   ```

**Option B: Ghost**
1. Go to your Ghost admin panel
2. Navigate to Settings → Integrations
3. Click "Add custom integration"
4. Name it "Newsletter Automation"
5. Copy the Admin API Key
6. Add to `.env.local`:
   ```
   GHOST_API_KEY=your_key_here
   GHOST_API_URL=https://yoursite.ghost.io
   ```

**Option C: Beehiiv**
1. Go to Beehiiv settings
2. Navigate to Integrations → API
3. Generate API key
4. Add to `.env.local`:
   ```
   BEEHIIV_API_KEY=your_key_here
   ```

### Optional APIs (Enhanced Features)

#### 3. Twitter/X API (for trend monitoring)
**Cost:** Free tier available
**Purpose:** Monitor Twitter discussions, find influencers

**Setup:**
1. Go to https://developer.twitter.com
2. Sign up for developer account
3. Create a new app
4. Generate Bearer Token and API keys
5. Add to `.env.local`:
   ```
   TWITTER_API_KEY=your_api_key
   TWITTER_API_SECRET=your_api_secret
   TWITTER_BEARER_TOKEN=your_bearer_token
   TWITTER_ACCESS_TOKEN=your_access_token
   TWITTER_ACCESS_SECRET=your_access_secret
   ```

**Rate Limits:**
- Free tier: 500,000 tweets/month
- Read rate: 450 requests/15 min

#### 4. SerpAPI (for Google Scholar search)
**Cost:** Free 100 searches/month, then $50/month
**Purpose:** Research academic papers, expert identification

**Setup:**
1. Go to https://serpapi.com
2. Sign up for free account
3. Copy API key from dashboard
4. Add to `.env.local`:
   ```
   SERPAPI_KEY=your_key_here
   ```

#### 5. Hunter.io (for email finding)
**Cost:** Free 50 searches/month, then $49/month
**Purpose:** Find company email addresses for sponsor outreach

**Setup:**
1. Go to https://hunter.io
2. Sign up for free account
3. Navigate to API → API Keys
4. Copy your API key
5. Add to `.env.local`:
   ```
   HUNTER_API_KEY=your_key_here
   ```

#### 6. OpenAI API (for content analysis)
**Cost:** Pay-as-you-go (~$0.10 per essay analysis)
**Purpose:** Content quality scoring, readability analysis

**Setup:**
1. Go to https://platform.openai.com
2. Sign up and add payment method
3. Navigate to API Keys
4. Create new secret key
5. Add to `.env.local`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

---

## Environment Variables Reference

Complete `.env.local` template:

```bash
# Newsletter Platform (choose one)
SUBSTACK_API_TOKEN=
GHOST_API_KEY=
GHOST_API_URL=
BEEHIIV_API_KEY=

# Social Media APIs (optional)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_BEARER_TOKEN=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_SECRET=

# Research APIs (optional)
SERPAPI_KEY=                  # Google Scholar search
HUNTER_API_KEY=               # Email finding
ARXIV_API_KEY=                # Academic papers (usually no key needed)

# AI APIs (optional)
OPENAI_API_KEY=              # Content analysis
ANTHROPIC_API_KEY=           # Alternative to OpenAI

# Development settings
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
```

---

## Directory Structure

Understanding the project layout:

```
strategic-tech-newsletter/
├── .claude/                    # Claude Code configuration
│   ├── settings.json          # Hooks and workflow automation
│   └── skills/                # Claude Code skills
│       ├── research/          # Research automation skill
│       ├── fact_checker/      # Fact-checking skill
│       └── social_repurpose/  # Social content generation skill
├── scripts/                    # Python automation scripts
│   ├── research_sources.py    # Trend discovery & expert sourcing
│   ├── fact_check.py          # Claim verification
│   ├── social_repurpose.py    # Social media content generation
│   ├── analytics_report.py    # Performance metrics
│   ├── sponsor_outreach.py    # Sponsor prospecting
│   └── validate_setup.py      # Environment validation
├── data/                       # Data files (gitignored)
│   ├── expert_database.json   # Expert CRM
│   ├── topic_trends.csv       # Trending topics history
│   ├── fact_check_library.json # Verified claims library
│   └── analytics_history.json # Metrics history
├── content/                    # Newsletter content
│   ├── essays/                # Published essays
│   ├── drafts/                # Work-in-progress
│   └── social_posts/          # Generated social content
├── tests/                      # Test suite (120 tests, 77% coverage)
├── docs/                       # Documentation
├── pyproject.toml             # Dependency management
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── CLAUDE.md                  # Claude Code guidelines
└── README.md                  # Project overview
```

---

## Verification Checklist

After setup, verify everything works:

### ✅ Basic Functionality
```bash
# 1. Dependencies installed
uv pip list | grep strategic-tech-newsletter

# 2. Environment variables loaded
python -c "from dotenv import load_dotenv; load_dotenv('.env.local'); import os; print('✓ Env vars loaded')"

# 3. Hacker News API works
python scripts/research_sources.py --mode=trending --days=7
# Should create data/topic_trends.csv with recent topics

# 4. Scripts executable
python scripts/fact_check.py --help
python scripts/social_repurpose.py --help
python scripts/analytics_report.py --help
```

### ✅ Tests Pass
```bash
# Run full test suite
pytest tests/ -v

# Expected: 120 passed, 77% coverage
```

### ✅ Data Files Created
```bash
# Check data directory
ls -la data/

# Should see:
# - expert_database.json
# - topic_trends.csv
# - fact_check_library.json
```

### ✅ Claude Code Skills Available
```bash
# Check skills exist
ls -la .claude/skills/

# Should see:
# - research/SKILL.md
# - fact_checker/SKILL.md
# - social_repurpose/SKILL.md
```

---

## Common Issues & Solutions

### Issue: `uv: command not found`
**Solution:**
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or via pip
pip install uv
```

### Issue: `ModuleNotFoundError: No module named 'requests'`
**Solution:**
```bash
# Reinstall dependencies
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### Issue: `Permission denied` when running scripts
**Solution:**
```bash
# Make scripts executable
chmod +x scripts/*.py

# Or run with python explicitly
python scripts/research_sources.py
```

### Issue: API rate limit exceeded
**Solution:**
- **Hacker News:** Wait 1 minute, reduce frequency
- **Twitter:** Free tier limit 450 requests/15 min
- **SerpAPI:** Free tier 100 searches/month
- **Hunter.io:** Free tier 50 searches/month

### Issue: Tests failing
**Solution:**
```bash
# Run tests with verbose output
pytest tests/ -v -s

# Run specific test file
pytest tests/unit/test_research_sources.py -v

# Check coverage
pytest tests/ --cov=scripts --cov-report=html
open htmlcov/index.html
```

---

## Next Steps

Once setup is complete:

1. **Read the workflows:** Check `docs/WORKFLOWS.md` for weekly routines
2. **Try research skill:** Use Claude Code on Web to run research automation
3. **Write first essay:** Follow the 5-day production cycle
4. **Generate social content:** Test the social_repurpose skill
5. **Review analytics:** Run weekly metrics reports

---

## Getting Help

- **Documentation:** Check `docs/` folder for detailed guides
- **Issues:** Report bugs at https://github.com/codeswiftr/strategic-tech-newsletter/issues
- **CLAUDE.md:** Read newsletter guidelines and SOPs
- **Test examples:** Review `tests/` for usage examples

---

## Security Best Practices

🔒 **Never commit API keys to git:**
- `.env.local` is gitignored
- Use `.env.example` as template only
- Rotate keys if accidentally exposed

🔒 **Restrict API key permissions:**
- Use read-only keys when possible
- Set up IP restrictions if available
- Monitor API usage regularly

🔒 **Backup your data:**
```bash
# Backup data directory
tar -czf backup-$(date +%Y%m%d).tar.gz data/

# Backup to cloud storage
# rclone copy data/ remote:newsletter-backup/
```

---

## Upgrade & Maintenance

Keep the system up to date:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
uv pip install -e ".[dev]" --upgrade

# Run tests after upgrade
pytest tests/ -v

# Check for security updates
uv pip list --outdated
```

---

**Setup complete! 🎉**

You're ready to use Strategic Tech Newsletter automation in Claude Code on the Web.

Next: Read `docs/WORKFLOWS.md` to learn the weekly production routine.
