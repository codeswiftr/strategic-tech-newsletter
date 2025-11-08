# Newsletter Research Skill

## Purpose
Automate weekly research: find trending topics, identify expert sources, validate credibility, and prepare outreach materials for the Strategic Tech Newsletter.

## When to Use
- **Weekly content planning** (Monday mornings)
- **Topic trend analysis** (identifying emerging themes)
- **Expert outreach preparation** (finding and vetting sources)
- **Competitive analysis** (what other newsletters are covering)

## Capabilities
1. **Trend Discovery**
   - Scrape Hacker News top stories (last 7-30 days)
   - Monitor Twitter/X for tech discussions
   - Track Reddit r/programming, r/technology trends
   - Identify patterns across platforms

2. **Expert Identification**
   - Find thought leaders on LinkedIn
   - Identify active Twitter/X voices
   - Discover GitHub project maintainers
   - Locate academic researchers (Google Scholar)

3. **Source Credibility Scoring**
   - Publication history (journals, blogs, talks)
   - Citation count and h-index
   - Social media engagement metrics
   - Professional affiliations
   - Score: 1-100 (100 = Nobel Prize winner, 1 = anonymous blogger)

4. **Outreach Template Generation**
   - Personalized email templates
   - Twitter DM drafts
   - LinkedIn connection messages
   - Interview question suggestions

## Inputs
- **Topic area** (e.g., "AI agents in backend development", "Rust adoption trends")
- **Time window** (default: 7 days, options: 3/7/14/30 days)
- **Target audience** (default: "senior engineers, CTOs", options: "startup founders", "enterprise architects")
- **Depth** (default: "expert", options: "basic", "expert", "comprehensive")
- **Minimum credibility score** (default: 75/100)

## Outputs

### 1. `research_report.json`
```json
{
  "topic": "AI agents in backend development",
  "research_date": "2025-01-20",
  "trending_topics": [
    {
      "title": "LangChain Agents Hit Production",
      "source": "Hacker News",
      "engagement_score": 450,
      "url": "https://...",
      "relevance_score": 92
    }
  ],
  "expert_sources": [
    {
      "name": "Dr. Jane Smith",
      "credibility_score": 95,
      "expertise": ["AI Agents", "Backend Systems"],
      "contact": {
        "email": "jane@university.edu",
        "twitter": "@janesmith",
        "linkedin": "https://linkedin.com/in/janesmith"
      },
      "recent_work": [
        "Published: 'Agent Architectures for Production' (2024)",
        "Spoke at: AI Engineering Summit 2024"
      ]
    }
  ],
  "outreach_angles": [
    "Impact of AI agents on database performance",
    "Security considerations for autonomous agents",
    "Cost-benefit analysis of agent vs traditional APIs"
  ]
}
```

### 2. `expert_database_update.csv`
```csv
name,expertise,twitter_handle,email,linkedin,credibility_score,last_updated
Dr. Jane Smith,"AI Agents|Backend Systems",@janesmith,jane@university.edu,https://...,95,2025-01-20
```

### 3. `outreach_templates/`
- `email_expert_interview.txt` - Personalized interview request
- `twitter_dm.txt` - Concise DM for Twitter outreach
- `linkedin_connection.txt` - LinkedIn connection message

## Example Usage

### Basic Trend Discovery
```
Use the research skill to find 5 emerging trends in AI regulation (past week).
Focus on topics relevant to technical leaders and CTOs.
```

### Expert Sourcing
```
Use research skill to identify 8 expert sources on "Rust in production systems".
Minimum credibility score: 85/100.
Include contact information and recent publications.
Generate personalized email templates for each expert.
```

### Comprehensive Research
```
Use research skill in comprehensive mode:
- Topic: "Platform engineering vs traditional DevOps"
- Time window: 30 days
- Find: 10 trending articles, 5 expert sources, 3 case studies
- Generate: outreach materials, interview questions, essay outline
```

## Scripts Used Internally

1. `scripts/research_sources.py --mode=trending --days=7`
   - Fetches Hacker News top stories
   - Saves to `data/topic_trends.csv`

2. `scripts/research_sources.py --topic="..." --depth=expert`
   - Deep-dive on specific topic
   - Searches academic papers, blogs, social media
   - Updates `data/expert_database.json`

## Quality Standards

- **Minimum 5 credible sources** per research request
- **Credibility score >75** for featured experts
- **Diversity**: sources from academia, industry, independent researchers
- **Recency**: prioritize sources active in last 6 months
- **Verification**: cross-check credentials via LinkedIn, Google Scholar

## Workflow Integration

**Monday Morning Routine:**
1. Run research skill for trending topics
2. Select 2-3 high-potential topics
3. Run research skill in expert mode for selected topics
4. Review expert list, select 3-5 for outreach
5. Send personalized outreach emails (use generated templates)
6. Track responses in `data/expert_database.json`

## Tips for Best Results

1. **Be specific with topic descriptions**
   - Good: "AI regulation frameworks in the EU vs US"
   - Bad: "AI stuff"

2. **Adjust time window based on topic velocity**
   - Fast-moving (e.g., AI): 7 days
   - Slower (e.g., database theory): 30 days

3. **Review and filter results**
   - Skill provides raw research, you curate final selection
   - Check credibility scores against your standards

4. **Update templates**
   - Customize generated outreach templates with your voice
   - Save successful templates for future use

## Limitations

- Cannot access paywalled content (journals, premium newsletters)
- Twitter API rate limits: 450 requests/15 min
- LinkedIn scraping may require manual verification
- Academic paper full-text may not be available

## Future Enhancements

- [ ] Integration with Google Scholar API
- [ ] Automated email sending (with approval)
- [ ] Response tracking and follow-up reminders
- [ ] Topic clustering (find related trends)
- [ ] Sentiment analysis of discussions
