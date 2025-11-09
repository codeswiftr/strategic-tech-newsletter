# Strategic Tech Newsletter - Weekly Workflows

Step-by-step workflows for producing weekly newsletter content using Claude Code on the Web.

---

## 📅 Weekly Production Schedule

### Monday: Research & Topic Selection (2 hours → 30 min with automation)

**Morning Routine:**

```bash
# 1. Fetch trending topics
python scripts/research_sources.py --mode=trending --days=7
```

**Or use Claude Code skill:**
```
Use research skill to find 10 trending topics from the past week.
Focus on: AI, DevOps, Cloud Infrastructure, Developer Tools
```

**Review Results:**
```bash
# Check trending topics
cat data/topic_trends.csv | tail -20

# Sort by engagement score
cat data/topic_trends.csv | sort -t, -k4 -rn | head -10
```

**Select Topic:** Choose topic with:
- High engagement score (>300)
- Strategic relevance to audience
- Novelty (not heavily covered)

**Deep Research:**
```bash
# Option 1: Manual command
python scripts/research_sources.py --topic="Your Selected Topic" --depth=expert

# Option 2: Use Claude Code skill
```

Claude Code on Web:
```
Use research skill in expert mode for topic: "AI regulation frameworks"

Requirements:
- Find 8+ expert sources
- Minimum credibility score: 85/100
- Include: academics, industry leaders, practitioners
- Generate email outreach templates
```

**Output:**
- `data/expert_database.json` updated with new experts
- `research_report.json` with sources and key insights

---

### Tuesday-Wednesday: Expert Outreach & Writing (6 hours → 4 hours)

#### Tuesday: Expert Outreach

**Review Expert List:**
```bash
# View experts by credibility score
python -c "
import json
with open('data/expert_database.json') as f:
    db = json.load(f)
experts = sorted(db['experts'], key=lambda x: x['credibility_score'], reverse=True)
for e in experts[:10]:
    print(f\"{e['name']} ({e['credibility_score']}): {e['email']}\")
"
```

**Send Outreach Emails:**
1. Use generated email templates from research skill
2. Personalize each email
3. Track responses in expert_database.json

#### Wednesday: Draft Writing

**Structure (follow CLAUDE.md guidelines):**
1. **Hook** (50-100 words): Compelling opening with key statistic
2. **Context** (200-300 words): Background and why this matters now
3. **Analysis** (600-800 words): Deep dive with expert insights
4. **Predictions** (200-300 words): Future implications
5. **Takeaways** (100-200 words): Actionable insights for readers

**Save draft:**
```bash
# Create draft file
touch content/drafts/your_topic_slug.md

# Write essay (1200-1800 words)
# Include inline citations: [source](url)
```

**Quality Checklist While Writing:**
- [ ] Every claim has a source
- [ ] Minimum 5 expert sources cited
- [ ] 30%+ original insights (not just synthesis)
- [ ] Clear actionable takeaways
- [ ] Grade 10-12 reading level

---

### Thursday: Fact-Checking & Editing (4 hours → 1.5 hours with automation)

#### Morning: Automated Fact-Check

```bash
# Run fact-checker in strict mode
python scripts/fact_check.py --draft=content/drafts/your_topic_slug.md --strict
```

**Or use Claude Code skill:**
```
Use fact_checker skill on content/drafts/ai_regulation.md in strict mode.

Requirements:
- Verify ALL statistical claims
- Require 2+ sources per claim
- Add hyperlink citations
- Flag any unverifiable claims
```

**Review Results:**
```bash
# Check fact-check report
cat content/drafts/your_topic_slug_factcheck.json

# Count claims by status
python -c "
import json
with open('content/drafts/your_topic_slug_factcheck.json') as f:
    report = json.load(f)
print(f\"Verified: {report['verified']}\")
print(f\"Unverified: {report['unverified']}\")
print(f\"Failed: {report['failed']}\")
"
```

#### Afternoon: Fix Unverified Claims

**For each unverified claim:**

1. **Find credible source:**
   - Google Scholar for academic claims
   - Official reports for statistics
   - Expert quotes from interviews

2. **Add to fact-check library:**
```bash
python scripts/fact_check.py \
  --claim="67% of enterprises use Kubernetes" \
  --source="https://cncf.io/survey-2024" \
  --add
```

3. **Update draft with citation:**
```markdown
According to [CNCF Survey 2024](https://cncf.io/survey-2024), 67% of enterprises now use Kubernetes in production.
```

4. **Re-run fact-check:**
```bash
python scripts/fact_check.py --draft=content/drafts/your_topic_slug.md --strict
```

**Repeat until:** `report['failed'] == 0`

#### Final Polish

- [ ] All claims verified ✅
- [ ] Readability checked (Hemingway app, grade 10-12)
- [ ] Internal links to previous essays added
- [ ] SEO keywords identified and included naturally
- [ ] Title is compelling (8-12 words)

**Move to essays folder:**
```bash
mv content/drafts/your_topic_slug.md content/essays/your_topic_slug.md
```

---

### Friday: Publication & Social Distribution (3 hours → 45 min with automation)

#### Morning: Social Content Generation

```bash
# Generate all social formats
python scripts/social_repurpose.py \
  --essay=content/essays/your_topic_slug.md \
  --formats=all
```

**Or use Claude Code skill:**
```
Use social_repurpose skill on content/essays/ai_regulation.md

Generate:
- 7 LinkedIn post variations (test different hooks)
- 3 Twitter thread styles
- 5 Substack Note teasers
- Email preview text

Tone: professional, data-driven
```

**Review Generated Content:**
```bash
# Check output directory
ls -la content/social_posts/your_topic_slug/

# Review LinkedIn variations
cat content/social_posts/your_topic_slug/linkedin/variation_1_hook_driven.txt
cat content/social_posts/your_topic_slug/linkedin/variation_2_question_led.txt

# Review Twitter thread
cat content/social_posts/your_topic_slug/twitter/thread_1_hook_style.txt
```

**Select Best Variations:**
- LinkedIn: Pick 2-3 variations for A/B testing
- Twitter: Select thread style based on topic (narrative vs bullet-point)
- Substack Notes: Choose most compelling teaser

#### Midday: Publish Newsletter

**Publish to platform:**
```bash
# If using Substack/Ghost API (future enhancement)
# python scripts/publish.py --essay=content/essays/your_topic_slug.md

# Manual for now:
# 1. Copy essay content
# 2. Paste into Substack/Ghost editor
# 3. Add featured image
# 4. Preview and publish
```

**Generate UTM-tracked links:**
```bash
# For LinkedIn
https://yoursite.com/essay-slug?utm_source=linkedin&utm_medium=social&utm_campaign=essay_name

# For Twitter
https://yoursite.com/essay-slug?utm_source=twitter&utm_medium=social&utm_campaign=essay_name
```

#### Afternoon: Social Media Distribution

**LinkedIn (Friday 4 PM optimal):**
1. Copy variation_1_hook_driven.txt
2. Replace [LINK] with UTM-tracked URL
3. Post to LinkedIn
4. Pin for first 24 hours

**Twitter Thread (Friday 6 PM optimal):**
1. Copy thread_1_hook_style.txt
2. Schedule tweets using TweetDeck or Buffer
3. Tweet 1 → wait 2 min → Tweet 2 → etc.

**Substack Notes (Saturday 10 AM):**
1. Copy note_1_stat_led.txt
2. Post to Substack Notes
3. Include link to full essay

**Track Performance:**
```bash
# Create tracking file
echo "Essay: your_topic_slug
Published: $(date)
LinkedIn: variation_1
Twitter: thread_1
Substack: note_1" > content/social_posts/your_topic_slug/distribution_log.txt
```

---

## 📊 Weekly Analytics Review

### Every Monday Morning (Before Research)

```bash
# Generate weekly report
python scripts/analytics_report.py --period=week --compare=true
```

**Review metrics:**
```bash
# View markdown report
cat data/analytics_report_week_$(date +%Y%m%d).md
```

**Key Metrics to Track:**
- **Open rate:** Target >40%
- **Click-through rate:** Target >8%
- **Subscriber growth:** Target >5% MoM
- **Top performing essay:** What worked?

**Action Items Based on Data:**
- Low open rate → Test new subject line styles
- Low CTR → Improve hooks and CTAs
- High engagement → Identify topic patterns
- Unsubscribes → Review content quality

---

## 🎯 Monthly Sponsor Outreach

### First Monday of Month

**Generate Prospects:**
```bash
python scripts/sponsor_outreach.py \
  --generate-prospects \
  --niche="developer-tools" \
  --count=20
```

**Review Prospects:**
```bash
# View by fit score
python -c "
import json
with open('data/sponsor_pipeline.json') as f:
    pipeline = json.load(f)
prospects = sorted(pipeline['prospects'], key=lambda x: x['fit_score'], reverse=True)
for p in prospects[:10]:
    print(f\"{p['company_name']} (Fit: {p['fit_score']}): {p['category']}\")
"
```

**Create Personalized Pitches:**
```bash
# Generate pitch for top prospect
python scripts/sponsor_outreach.py \
  --pitch \
  --company="Top Prospect Inc" \
  --template=data-driven

# Review pitch
cat data/pitch_Top_Prospect_Inc_*.txt
```

**Send Outreach:**
1. Personalize generated pitch
2. Send to marketing contact
3. Track in sponsor_pipeline.json

**Update Status:**
```bash
python scripts/sponsor_outreach.py \
  --update-status=contacted \
  --prospect-id=PROSPECT_20250120_001
```

---

## 🔄 Workflow Optimization Tips

### Time-Saving Shortcuts

**1. Create Aliases:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias research='python scripts/research_sources.py'
alias factcheck='python scripts/fact_check.py'
alias social='python scripts/social_repurpose.py'
alias analytics='python scripts/analytics_report.py'
alias sponsors='python scripts/sponsor_outreach.py'
```

**2. Use Claude Code Skills:**
- Skills auto-load in Claude Code on Web
- Natural language interface
- No need to remember exact commands
- Example: "Use research skill to find AI trends"

**3. Batch Processing:**
```bash
# Generate social content for multiple essays
for essay in content/essays/*.md; do
  python scripts/social_repurpose.py --essay="$essay" --formats=all
done
```

### Quality Gates

**Before Publication Checklist:**
```bash
#!/bin/bash
# Save as scripts/pre_publish_check.sh

echo "🔍 Running pre-publication checks..."

# 1. Fact-check passes
python scripts/fact_check.py --draft=content/drafts/$1.md --strict
if [ $? -ne 0 ]; then
  echo "❌ Fact-check failed!"
  exit 1
fi

# 2. Word count in range (1200-1800)
word_count=$(wc -w < content/drafts/$1.md)
if [ $word_count -lt 1200 ] || [ $word_count -gt 1800 ]; then
  echo "⚠️ Word count: $word_count (target: 1200-1800)"
fi

# 3. Minimum sources cited
source_count=$(grep -o '\[.*\](http' content/drafts/$1.md | wc -l)
if [ $source_count -lt 5 ]; then
  echo "❌ Only $source_count sources (minimum: 5)"
  exit 1
fi

echo "✅ All checks passed! Ready to publish."
```

---

## 🚀 Automation Level Selection

Choose your automation level:

### Level 1: Manual (Beginner)
- Run each script manually
- Review all outputs before proceeding
- Learn the workflow step-by-step
- **Time:** ~15 hours/week

### Level 2: Semi-Automated (Recommended)
- Use Claude Code skills for complex tasks
- Automate fact-checking and social generation
- Manual review and editing
- **Time:** ~6 hours/week (60% reduction)

### Level 3: Fully Automated (Advanced)
- Claude Code on Web orchestrates entire workflow
- Minimal manual intervention
- Focus on strategy and quality review
- **Time:** ~2 hours/week (87% reduction)

---

## 📝 Example Session (Claude Code on Web)

**Monday Morning:**
```
Me: Use research skill to find 10 trending topics in AI and DevOps from the past week.

Claude: [Executes research_sources.py, analyzes results]
I found 10 trending topics. Top 3 by engagement:
1. "AI Agents in Production" (score: 450)
2. "Kubernetes 2.0 Announced" (score: 380)
3. "Platform Engineering vs DevOps" (score: 320)

Which topic interests you for this week's essay?

Me: Let's go with AI Agents in Production.

Claude: [Executes deep research]
I've researched "AI Agents in Production" and found 12 expert sources...
[Shows research summary]
Ready to start writing?
```

**Thursday Afternoon:**
```
Me: Use fact_checker skill on my draft in strict mode.

Claude: [Executes fact_check.py]
Fact-check complete:
✅ 18 claims verified
❌ 2 claims failed verification:
1. "80% of companies use AI agents" - No credible source found
2. "Agent response times under 100ms" - Conflicting data

Recommendations:
- Claim 1: Soften to "Many companies are experimenting..."
- Claim 2: Cite specific benchmark: "OpenAI reports 120ms average"

Should I update the draft?
```

---

**Ready to start? Begin with Monday's research workflow!**

For detailed API setup, see `docs/SETUP_GUIDE.md`
For API integration details, see `docs/API_INTEGRATIONS.md`
