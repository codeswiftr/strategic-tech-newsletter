# Social Repurpose Skill

## Purpose
Transform long-form newsletter essays into engaging social media content optimized for each platform. Generate multiple variations for A/B testing, maintain brand voice, and maximize distribution reach.

## When to Use
- **Friday afternoon** (after essay publication)
- **Social media scheduling** (planning week's content)
- **Engagement campaigns** (promoting specific essays)
- **Content recycling** (evergreen posts from archive)

## Capabilities

### 1. Platform-Specific Optimization
- **Twitter/X**: Thread format (10-15 tweets), 280 char limit
- **LinkedIn**: Long-form post (1300 chars optimal), professional tone
- **Substack Notes**: Teaser format, link to full essay
- **Newsletter Teaser**: Email subject line + preview

### 2. Multiple Format Variations
- Generate 7 LinkedIn post variations (for A/B testing)
- Create 3 Twitter thread styles (hook, narrative, bullet-point)
- Produce 5 Substack Note teasers (different angles)

### 3. Content Extraction
- Identify most compelling hook from essay
- Extract 3-5 key insights
- Pull quotable statistics
- Find controversial/discussion-worthy points

### 4. Call-to-Action Optimization
- Subscribe CTA (for new readers)
- Engagement CTA (comment, share, discuss)
- Link tracking (UTM parameters)

## Inputs

- **Published essay** (markdown file)
  ```
  content/essays/ai_regulation.md
  ```

- **Target platforms** (default: all)
  - Options: `twitter`, `linkedin`, `substack_notes`, `teaser`, `all`

- **Tone preference** (default: professional)
  - Options: `professional`, `casual`, `provocative`, `educational`

- **Variations count**
  - LinkedIn: 7 variations
  - Twitter threads: 3 variations
  - Substack Notes: 5 variations

## Outputs

### 1. LinkedIn Post Variations (7 formats)

**Variation 1: Hook-driven**
```
🚀 AI regulation is coming faster than most tech leaders expect.

Here's what you need to know:

→ 12 countries launching frameworks in 2025
→ EU's AI Act enforcement starts Q2
→ Compliance costs: $500K-$2M per company

The window to prepare is closing.

Read my deep-dive on strategic preparation 👇
[LINK]

#AIRegulation #TechStrategy #Leadership
```

**Variation 2: Question-led**
```
Is your organization ready for the AI regulation wave?

67% of enterprises haven't started compliance prep, according to Gartner's 2024 report.

That's a problem. Here's why:

• EU AI Act enforcement: Q2 2025
• Penalties: up to 6% of global revenue
• Implementation timeline: 6-18 months

I spent the week researching what strategic tech leaders are doing differently.

Key insight: It's not just legal compliance—it's competitive advantage.

Full analysis 👉 [LINK]

What's your organization's AI governance strategy? Share below.

#ArtificialIntelligence #Compliance #CTO
```

**[5 more variations in different styles]**

### 2. Twitter Thread Variations (3 styles)

**Style 1: Hook + Thread 🧵**
```
Tweet 1/12:
AI regulation isn't coming.

It's already here. And most tech companies aren't ready.

A thread on what's changing in 2025 🧵👇

---

Tweet 2/12:
The EU's AI Act officially takes effect in Q2 2025.

This isn't just European news—it impacts any company serving EU customers.

Think GDPR, but for AI systems.

---

Tweet 3/12:
What counts as "high-risk" AI under the Act?

→ Hiring/HR systems
→ Credit scoring
→ Law enforcement tools
→ Critical infrastructure management

If you use AI for these, you're in scope.

---

[Continue through 12 tweets]

Tweet 12/12:
Bottom line: Compliance isn't just legal—it's strategic.

Companies that get this right will have a moat.

Read my full analysis: [LINK]

Like/RT if you found this useful!
```

**Style 2: Bullet-Point Thread**
**Style 3: Narrative Thread**

### 3. Substack Notes (5 variations)

**Variation 1: Stat-led**
```
67% of enterprises haven't started AI compliance prep.

The EU AI Act enforcement begins in 4 months.

I spent the week researching what strategic leaders are doing differently.

Surprising finding: It's not about avoiding penalties—it's about building competitive moats.

Full analysis 👇
[LINK]
```

**[4 more variations with different hooks]**

### 4. Newsletter Teaser (Email/Preview)

**Subject Line Options:**
1. "AI regulation: 4 months until enforcement (are you ready?)"
2. "67% of companies unprepared for AI Act—here's the playbook"
3. "The strategic advantage hiding in AI compliance"

**Preview Text:**
```
The EU AI Act isn't just a legal issue—it's a strategic opportunity.
Companies that get compliance right will build competitive moats.
Here's how to prepare (6-minute read).
```

## Example Usage

### Generate All Platforms
```
Use social_repurpose skill on content/essays/ai_regulation.md with all formats.

Tone: professional
Generate: 7 LinkedIn variations, 3 Twitter threads, 5 Substack Notes
Include: UTM parameters for link tracking
Save to: content/social_posts/ai_regulation/
```

### Twitter Thread Only
```
Use social_repurpose skill:
- Essay: content/essays/platform_engineering.md
- Format: twitter
- Style: provocative
- Thread length: 12-15 tweets
- Include: engagement hooks, poll questions, RT requests
```

### A/B Test LinkedIn Posts
```
Use social_repurpose skill to generate 7 LinkedIn variations for:
Essay: content/essays/rust_adoption.md

Variations:
1. Hook-driven (starts with surprising stat)
2. Question-led (poses problem)
3. Story-led (personal anecdote)
4. List-based (3 key insights)
5. Contrarian (challenges common belief)
6. Data-heavy (multiple statistics)
7. Minimalist (1-2 sentences + link)

For each: estimate engagement potential (likes, comments, shares)
```

## Quality Standards

### Brand Voice Consistency
- **Strategic Tech Newsletter tone**: Authoritative yet accessible
- **Avoid**: Hype, clickbait, excessive emojis
- **Include**: Data-driven insights, actionable takeaways

### Platform Best Practices

**LinkedIn:**
- First line: Hook (8-12 words)
- Paragraph breaks: Every 2-3 lines for readability
- Length: 1000-1300 characters optimal
- Hashtags: 3-5 relevant tags at end
- CTA: Question to encourage comments

**Twitter/X:**
- Tweet 1: Hook + "A thread 🧵👇"
- Tweets 2-11: One insight per tweet, clear transitions
- Tweet 12: Summary + CTA + link
- Character count: Use full 280 when needed
- Avoid: Thread jail (keep tweets concise)

**Substack Notes:**
- Length: 200-400 characters
- Hook: First 50 characters critical (preview cutoff)
- Link: Always include at end
- Tone: Slightly more casual than essay

### Engagement Optimization

**Hooks that work:**
- Surprising statistics: "67% of..."
- Provocative questions: "Is X actually Y?"
- Contrarian takes: "Everyone says X. They're wrong."
- Timely warnings: "X is coming faster than you think"

**CTAs that convert:**
- Questions: "What's your experience with X?"
- Requests: "Share if you found this useful"
- Challenges: "Who else thinks X?"
- Direct asks: "Subscribe for weekly insights like this"

## Scripts Used Internally

1. `scripts/social_repurpose.py --essay=path/essay.md --formats=all`
   - Reads essay, extracts key points
   - Generates platform-specific content
   - Saves to `content/social_posts/{essay_name}/`

2. `scripts/social_repurpose.py --essay=path/essay.md --formats=linkedin --variations=7`
   - Focus on single platform
   - Generate multiple variations for A/B testing

## Workflow Integration

**Friday Afternoon Routine:**
1. Essay published on Substack/Ghost
2. Run social_repurpose skill (all formats)
3. Review generated content
4. Select best variation per platform
5. Schedule posts:
   - LinkedIn: Friday 4 PM
   - Twitter thread: Friday 6 PM
   - Substack Note: Saturday 10 AM
6. Track engagement in `data/social_performance.csv`

**Weekly A/B Testing:**
- Post 2 LinkedIn variations (Mon/Wed)
- Compare: likes, comments, shares, click-through
- Document winning formula
- Refine future templates

## Output Structure

```
content/social_posts/
└── ai_regulation/
    ├── linkedin/
    │   ├── variation_1_hook_driven.txt
    │   ├── variation_2_question_led.txt
    │   ├── variation_3_story_led.txt
    │   ├── variation_4_list_based.txt
    │   ├── variation_5_contrarian.txt
    │   ├── variation_6_data_heavy.txt
    │   └── variation_7_minimalist.txt
    ├── twitter/
    │   ├── thread_1_hook_style.txt
    │   ├── thread_2_bullet_style.txt
    │   └── thread_3_narrative_style.txt
    ├── substack_notes/
    │   ├── note_1_stat_led.txt
    │   ├── note_2_question_led.txt
    │   ├── note_3_insight_led.txt
    │   ├── note_4_quote_led.txt
    │   └── note_5_provocative.txt
    ├── teaser/
    │   └── email_preview.txt
    └── metadata.json
```

### metadata.json
```json
{
  "essay_title": "The Future of AI Regulation",
  "essay_url": "https://newsletter.com/ai-regulation",
  "generated_date": "2025-01-20",
  "formats_generated": ["linkedin", "twitter", "substack_notes", "teaser"],
  "variations": {
    "linkedin": 7,
    "twitter": 3,
    "substack_notes": 5
  },
  "utm_parameters": {
    "source": "social",
    "medium": "linkedin",
    "campaign": "ai_regulation_essay"
  },
  "tracking_links": {
    "linkedin": "https://newsletter.com/ai-regulation?utm_source=linkedin&utm_medium=social&utm_campaign=ai_regulation",
    "twitter": "https://newsletter.com/ai-regulation?utm_source=twitter&utm_medium=social&utm_campaign=ai_regulation"
  }
}
```

## Performance Metrics

- **Time savings**: 80% (3 hours → 30 minutes)
- **Output volume**: 3x increase (1 post → 15 variations)
- **Engagement**: Track per variation
- **Click-through rate**: Monitor UTM-tagged links

## Common Issues & Solutions

### Issue: "Content too similar across variations"
**Solution:**
- Adjust tone parameter
- Use different hooks (stat vs question vs story)
- Vary CTA approaches

### Issue: "Twitter thread too long"
**Solution:**
- Set max tweets: `--max-tweets=12`
- Focus on top 3 insights
- Link to essay for full details

### Issue: "LinkedIn posts too formal"
**Solution:**
- Use `tone: casual`
- Add personal anecdote
- Include rhetorical questions

## Tips for Best Results

1. **Review and edit**: Generated content is 80% ready, refine 20%
2. **Test hooks**: Try 3-5 different opening lines
3. **Track winners**: Document which variations perform best
4. **Update templates**: Refine prompts based on learnings
5. **Stay authentic**: Don't over-optimize into clickbait

## Limitations

- Cannot auto-post (requires manual scheduling)
- Emoji use may need adjustment per brand
- Platform changes (e.g., Twitter character limits) require updates
- Tone/voice accuracy improves with examples

## Future Enhancements

- [ ] Auto-posting integration (Buffer, Hootsuite)
- [ ] Image generation (key stat graphics)
- [ ] Video script generation (for LinkedIn/Twitter videos)
- [ ] Hashtag optimization (trending tags)
- [ ] Engagement prediction (ML-based scoring)
- [ ] Auto-response suggestions (for comments)
