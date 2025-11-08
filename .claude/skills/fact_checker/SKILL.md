# Fact-Checking Skill

## Purpose
Validate every factual claim before publication to ensure 100% accuracy and maintain the newsletter's credibility. Automatically extract claims, verify against trusted sources, add citations, and flag questionable statements.

## When to Use
- **Thursday fact-checking session** (before Friday publication)
- **Draft review** (after initial essay writing)
- **Pre-publication quality gate** (mandatory before going live)
- **Claim verification** (when adding statistics or data)

## Process

### 1. Claim Extraction (NLP-based)
- Scan draft for factual assertions
- Identify: statistics, percentages, dates, quotes, causal claims
- Extract: "According to X, Y% of Z..." patterns
- Flag: unsourced claims, vague assertions

### 2. Source Verification
- For each claim: search `data/fact_check_library.json`
- If not found: query external sources (Google Scholar, official reports)
- Requirement: **2+ credible sources** for each claim
- Cross-reference: ensure sources agree

### 3. Citation Addition
- Add hyperlinks: `[source_name](url)` format
- Prefer primary sources over secondary
- Use APA citation format for academic papers
- Include access date for web sources

### 4. Quality Flagging
- ✅ **Verified**: 2+ credible sources, high confidence
- ❌ **Needs Review**: conflicting sources, low credibility
- ⚠️ **Flagged for Editor**: cannot verify, requires expert input

## Inputs

- **Draft essay** (markdown file path)
  ```
  content/drafts/ai_regulation.md
  ```

- **Fact-check library** (citation database)
  ```json
  data/fact_check_library.json
  ```

- **Strictness mode**
  - `strict`: Block publication if any claim unverified
  - `relaxed`: Allow with warnings for manual review

- **Verification threshold** (default: 0.90)
  - Confidence score required to pass (0.0-1.0)

## Outputs

### 1. `essay_with_citations.md`
Updated essay with inline hyperlinks:

**Before:**
```markdown
AI investment grew by 45% in 2024.
```

**After:**
```markdown
AI investment grew by [45% in 2024](https://mckinsey.com/ai-report-2024).
```

### 2. `fact_check_report.json`
```json
{
  "draft": "content/drafts/ai_regulation.md",
  "check_date": "2025-01-20T10:30:00",
  "total_claims": 12,
  "verified": 10,
  "unverified": 1,
  "failed": 1,
  "pass": false,
  "details": [
    {
      "claim": "AI investment grew by 45% in 2024",
      "type": "percentage",
      "status": "verified",
      "confidence": 0.95,
      "sources": [
        "https://mckinsey.com/ai-report-2024",
        "https://gartner.com/ai-spending-2024"
      ]
    },
    {
      "claim": "Most developers prefer Python",
      "type": "vague",
      "status": "needs_review",
      "confidence": 0.50,
      "issue": "Define 'most' - provide specific percentage",
      "suggestion": "Replace with: '67% of developers use Python regularly' [Stack Overflow Survey 2024]"
    },
    {
      "claim": "AI will replace 50% of jobs by 2030",
      "type": "prediction",
      "status": "failed",
      "confidence": 0.20,
      "issue": "Highly speculative, conflicting expert opinions",
      "sources_found": [
        "https://optimistic-source.com (70% replacement)",
        "https://conservative-source.com (10% replacement)"
      ],
      "recommendation": "Remove or soften claim: 'Estimates vary widely, from 10-70%'"
    }
  ]
}
```

### 3. `unverified_claims.txt`
Plain text list for manual review:
```
UNVERIFIED CLAIMS REQUIRING MANUAL REVIEW:

1. "Most developers prefer Python" (Line 45)
   Issue: Vague quantifier
   Suggested Fix: Use specific percentage from Stack Overflow Survey

2. "AI will replace 50% of jobs by 2030" (Line 78)
   Issue: Highly speculative, conflicting sources
   Recommendation: Remove or provide range of estimates
```

## Example Usage

### Basic Fact-Check
```
Use fact_checker skill on content/drafts/ai_regulation.md in strict mode.
Add citations as hyperlinks. Flag anything questionable.
```

### Comprehensive Review
```
Use fact_checker skill with these settings:
- Draft: content/drafts/platform_engineering.md
- Mode: strict
- Threshold: 0.95 (very high confidence required)
- Output: essay_with_citations.md + detailed report

For each unverified claim, suggest:
1. Alternative phrasing
2. Potential sources to check
3. Whether to keep, modify, or remove
```

### Quick Claim Verification
```
Use fact_checker skill to verify this single claim:
"Kubernetes adoption reached 96% among enterprises in 2024"

Provide:
- Confidence score
- Primary sources (minimum 2)
- Alternative statistics if available
```

## Quality Standards

### Citation Requirements
- **Primary sources preferred**: Original research, official reports
- **Secondary sources acceptable**: Reputable tech media (TechCrunch, Ars Technica)
- **Avoid**: Blog posts (unless from recognized experts), unverified social media

### Source Credibility Scoring
- **High (0.90-1.00)**: Academic journals, government reports, S&P 500 company filings
- **Medium (0.70-0.89)**: Tech media (TechCrunch, The Verge), industry reports (Gartner, Forrester)
- **Low (0.50-0.69)**: Personal blogs (verified experts), podcasts, conference talks
- **Unacceptable (<0.50)**: Anonymous sources, unverified social media, clickbait sites

### Verification Process
1. **Check fact-check library first** (instant if previously verified)
2. **Google Scholar search** for academic backing
3. **Official source verification** (company press releases, government data)
4. **Expert corroboration** (quotes from named experts)
5. **Cross-reference** (ensure 2+ sources agree)

### Edge Cases

**Predictions/Opinions:**
- Clearly label as predictions or opinions
- Attribute to specific expert: "According to [Expert], ..."
- Include confidence level: "Some analysts predict...", "Widely expected..."

**Statistics:**
- Always provide source and date
- Specify methodology if available
- Note margin of error when relevant

**Quotes:**
- Verify exact wording (use quotation marks)
- Link to original source
- Provide context (when/where said)

## Scripts Used Internally

1. `scripts/fact_check.py --draft=path/to/draft.md --strict`
   - Extracts claims using regex patterns
   - Verifies against `data/fact_check_library.json`
   - Generates detailed report

2. `scripts/fact_check.py --claim="..." --source="..."`  --add`
   - Manually add verified claim to library
   - Useful after validating new sources

## Workflow Integration

**Thursday Fact-Check Routine:**
1. Run fact_checker skill on draft
2. Review `fact_check_report.json`
3. For each unverified claim:
   - Research proper source
   - Add to fact-check library: `fact_check.py --add`
   - Update draft with citation
4. Re-run fact_checker until `pass: true`
5. Save report with essay for future reference

**Pre-Publication Checklist:**
- [ ] Fact-check report shows `pass: true`
- [ ] All statistics have hyperlinked sources
- [ ] No claims flagged as "needs review"
- [ ] Vague terms replaced with specific data
- [ ] Predictions clearly labeled as such

## Common Issues & Solutions

### Issue: "Too many unverified claims"
**Solution:**
- Use relaxed mode for first pass
- Identify patterns (e.g., all stats from one source)
- Batch-add verified claims to library
- Re-run in strict mode

### Issue: "Conflicting sources"
**Solution:**
- Present range of estimates
- Note disagreement in essay
- Cite both sources
- Example: "Estimates range from 40% [Source A] to 60% [Source B]"

### Issue: "Cannot find credible source"
**Solution:**
- Soften claim ("may", "some experts believe")
- Remove claim entirely
- Reach out to expert for clarification
- Flag for manual research

## Performance Metrics

- **Target**: 100% fact-check pass rate before publication
- **Average time**: 15-30 minutes per essay (with library)
- **Reduction vs manual**: 60-75% time savings
- **Accuracy improvement**: 40% fewer post-publication corrections

## Limitations

- Cannot verify behind paywalls (some academic journals)
- Predictions/forecasts inherently uncertain
- Emerging topics may lack credible sources (flag for manual review)
- Sarcasm/humor may be misidentified as factual claims

## Future Enhancements

- [ ] LLM-powered claim extraction (beyond regex)
- [ ] Automatic Google Scholar querying
- [ ] Integration with fact-checking APIs (Snopes, PolitiFact)
- [ ] Citation format variations (APA, MLA, Chicago)
- [ ] Plagiarism detection
- [ ] Source freshness checking (warn if source >2 years old)
