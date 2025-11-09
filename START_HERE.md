# 🚀 Getting Started with Strategic Tech Newsletter

## Copy This Prompt into Claude Code on the Web

```
I'm ready to start using the Strategic Tech Newsletter automation system!

First, let's validate my environment setup:
1. Run the validation script to check everything is configured correctly
2. Show me the results and identify any issues

Then, let's do a test run of the research workflow:
1. Use the research skill to find 10 trending topics from the past 7 days
2. Focus on: AI/ML, DevOps, Cloud Infrastructure, and Developer Tools
3. Show me the top 5 topics by engagement score
4. For the #1 topic, run a deep research to find expert sources

Finally, prepare me for my first newsletter:
1. Explain the weekly workflow (Monday-Friday routine)
2. Show me what files I need to create/edit
3. Walk me through using the fact_checker and social_repurpose skills

Let's begin! 🎯
```

---

## Alternative: Quick Testing Prompt

If you just want to test the system quickly:

```
Let's test the Strategic Tech Newsletter automation system!

Step 1: Validate setup
Run: python scripts/validate_setup.py

Step 2: Test research functionality
Run: python scripts/research_sources.py --mode=trending --days=7

Step 3: Show me the results
Read: data/topic_trends.csv (show last 10 entries)

Step 4: Pick a topic and explain next steps
Based on the trending topics, recommend which one would make the best newsletter essay and explain why.
```

---

## Alternative: Full Production Workflow Prompt

If you're ready to create your first newsletter:

```
I want to produce my first Strategic Tech Newsletter essay this week. Guide me through the complete workflow using Claude Code skills.

**Monday - Research Phase:**
1. Use research skill to find trending topics (past 7 days)
2. Analyze the topics and help me select the best one for my audience (technical leaders, CTOs, senior engineers)
3. Run deep research on the selected topic to find 8+ expert sources
4. Generate email outreach templates for the top 5 experts

**Tuesday-Wednesday - Writing Phase:**
1. Help me structure the essay (Hook → Context → Analysis → Predictions → Takeaways)
2. Draft the essay outline based on research findings
3. Ensure we include 30%+ original insights

**Thursday - Fact-Checking Phase:**
1. Use fact_checker skill on my draft (I'll write it in content/drafts/)
2. Verify all statistical claims
3. Add proper citations with hyperlinks
4. Flag any unverifiable claims for manual review

**Friday - Distribution Phase:**
1. Use social_repurpose skill to generate all social content
2. Create 7 LinkedIn variations for A/B testing
3. Generate 3 Twitter thread styles
4. Produce 5 Substack Note teasers

Let's start with Monday's research! Use the research skill now.
```

---

## Alternative: Learn & Explore Prompt

If you want to understand the system first:

```
Help me understand the Strategic Tech Newsletter automation system.

1. **Overview:**
   - Explain the 3 Claude Code skills (research, fact_checker, social_repurpose)
   - Show me what each skill can do
   - Explain when to use each one

2. **Quick Demo:**
   - Run a simple research query to find 5 trending AI topics
   - Show me the output format
   - Explain how I'd use this in my workflow

3. **File Structure:**
   - Walk me through the key directories (scripts/, data/, content/)
   - Show me what's in the data files (expert_database.json, topic_trends.csv)
   - Explain the content workflow (drafts → essays → social_posts)

4. **Next Steps:**
   - What do I need to configure? (API keys, etc.)
   - What's the minimal setup to start producing content?
   - Recommend a learning path for me

Let's start with the overview!
```

---

## Recommended: First-Time User Prompt

**Best for first-time users - comprehensive but not overwhelming:**

```
Welcome! I'm new to the Strategic Tech Newsletter automation system.

**Immediate Goals:**
1. Validate my environment is set up correctly
2. Understand the 3 core skills (research, fact_checker, social_repurpose)
3. Run a test of the research workflow
4. See what a complete newsletter workflow looks like

**Let's Start:**

Step 1: Run validation
Execute: python scripts/validate_setup.py
Show me the results and explain any issues.

Step 2: Test basic research
Use the research skill to find 5 trending topics in AI/ML from the past week.
Show me the results and explain what I'm seeing.

Step 3: Explain the workflow
Walk me through the Monday-Friday production schedule.
Show me which skills I'd use on which days.

Step 4: Demo fact-checking
Show me how the fact_checker skill works by running it on the sample essay in tests/fixtures/sample_essay.md

I'm ready to learn! Let's begin with Step 1.
```

---

## 🎯 My Recommendation

**Use this prompt - it's comprehensive and actionable:**

```
I'm ready to use Strategic Tech Newsletter automation in Claude Code on the Web!

**Context:** This is a production-ready newsletter automation system with 3 Claude Code skills (research, fact_checker, social_repurpose) that reduces content production time by 80%.

**My immediate goals:**
1. Validate environment setup
2. Run a test research workflow
3. Understand the weekly production routine
4. Prepare for creating my first newsletter essay

**Let's start:**

STEP 1 - Validation:
Run the validation script and show me if everything is configured correctly:
```bash
python scripts/validate_setup.py
```

STEP 2 - Test Research:
Use the research skill to find 10 trending topics from the past week in these areas:
- AI/ML and LLMs
- DevOps and Platform Engineering
- Cloud Infrastructure
- Developer Tools and DX

Show me the top 5 by engagement score and recommend which would make the best newsletter topic for technical leaders and CTOs.

STEP 3 - Workflow Overview:
Explain the weekly workflow (Monday-Friday) and show me which Claude Code skills I'd use each day.

STEP 4 - Next Actions:
Based on the trending topics you found, prepare me to write my first essay:
- What should I research next?
- What files do I need to create?
- Which skill should I use next?

Let's begin! Run Step 1 now. 🚀
```

---

## 📋 Quick Reference Card

Save this for quick access:

| Day | Task | Command/Skill |
|-----|------|---------------|
| **Monday** | Research topics | `Use research skill to find trending topics` |
| **Monday** | Deep research | `Use research skill in expert mode on [topic]` |
| **Tue-Wed** | Write draft | Manual writing in `content/drafts/` |
| **Thursday** | Fact-check | `Use fact_checker skill on draft in strict mode` |
| **Friday** | Social content | `Use social_repurpose skill to generate all formats` |
| **Friday** | Analytics | `python scripts/analytics_report.py --period=week` |

---

## ✅ Pre-flight Checklist

Before using in Claude Code on the Web:

- [✅] Repository exists: https://github.com/codeswiftr/strategic-tech-newsletter
- [✅] All files committed and pushed
- [✅] 120 tests passing (77% coverage)
- [✅] 3 Claude Code skills ready
- [✅] Complete documentation available
- [✅] Validation script created
- [ ] API keys configured in .env.local (do this first!)
- [ ] Ran validation script
- [ ] Tested basic functionality

**Everything is committed and ready! Choose your starting prompt above and paste it into Claude Code on the Web.** 🎉
