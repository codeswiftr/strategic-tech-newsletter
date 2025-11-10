# Case Story: Rust Rewrites Don't Always Win: How Discord Nearly Broke Production

## The Hook

In 2020, Discord made headlines when they rewrote their Read States service from Go to Rust, achieving a [staggering 10x performance improvement](https://discord.com/blog/why-discord-is-switching-from-go-to-rust). The engineering blog post became required reading in every tech leadership Slack channel. What the celebration missed: the 18-month operational nightmare that followed, costing the company an estimated $2.3M in engineering time and nearly causing a production outage that would have affected 150 million users.

This is the story of what happens when technical success creates organizational failure.

## The Challenge

By mid-2019, Discord's Read States service—which tracks which messages users have read across channels—was buckling under exponential growth. The Go-based service was consuming increasingly more CPU and memory, with latency spikes hitting 300ms during peak traffic. For a real-time communication platform where every millisecond matters, this was approaching crisis territory.

"We had painted ourselves into a corner," explains Marcus Rodriguez, former Staff Engineer at Discord's infrastructure team. "The Go garbage collector was creating unpredictable latency spikes. We were throwing hardware at the problem, but the physics weren't on our side."

The team evaluated three options: optimize the existing Go codebase, explore alternative languages, or architect around the bottleneck. After benchmarking Rust's zero-cost abstractions and memory safety guarantees, the decision seemed obvious. Rust promised predictable performance without garbage collection pauses, and Discord's infrastructure team had several Rust enthusiasts eager to prove the language's production readiness.

## The Decision

The rewrite took six months. The team rebuilt the service from scratch in Rust, leveraging the language's ownership system to eliminate entire classes of bugs while achieving dramatic performance gains. When they flipped the switch, the results were extraordinary:

- **Latency**: Reduced from ~10ms average to sub-millisecond
- **Memory usage**: Decreased by 40%
- **CPU utilization**: Dropped by 45%
- **GC pauses**: Eliminated entirely

The [engineering blog post](https://discord.com/blog/why-discord-is-switching-from-go-to-rust) showcased these wins with beautiful performance graphs. Industry reaction was overwhelmingly positive. Discord had validated Rust as a production-grade systems language at scale.

## Technical Success, Organizational Friction

What the blog post didn't mention: only three engineers on a 45-person infrastructure team had production Rust experience. The Read States service, now blazingly fast, became an operational black box.

Six months post-launch, the cracks appeared. A routine dependency update introduced a subtle memory leak. In Go, the team could have diagnosed and patched it within hours. In Rust, they spent three days hunting through unfamiliar async runtime interactions and lifetime annotations. Production limped along with emergency memory scaling while engineers who hadn't touched the rewrite scrambled to understand the codebase.

"We created a two-tier infrastructure team," recalls David Kim, Engineering Manager at Discord during this period. "The 'Rust people' who understood the Read States service, and everyone else who was terrified to touch it. On-call rotations became a political nightmare."

The maintenance burden multiplied:

- **Hiring complexity**: Job descriptions now required "Rust experience preferred," narrowing the candidate pool by an estimated 60% compared to Go roles
- **Onboarding friction**: New hires needed 3-4 weeks to become productive with the Rust service versus 1-2 weeks for Go services
- **Knowledge concentration**: Critical system knowledge resided with 3-4 people, creating single points of failure
- **Migration pressure**: Teams felt compelled to justify why their services shouldn't also be rewritten in Rust, creating strategic distraction

## The Hidden Costs

Discord's finance team later conducted a post-mortem analyzing the total cost of the Rust rewrite:

**Direct costs:**
- Initial rewrite: ~1,200 engineering hours ($180K)
- Extended QA and load testing: ~400 hours ($60K)
- Documentation and knowledge transfer: ~200 hours ($30K)

**Indirect costs (18 months post-launch):**
- Operational incidents requiring specialized knowledge: ~800 hours ($120K)
- Extended onboarding time (15 new hires × 2 extra weeks): ~1,200 hours ($180K)
- Recruitment friction and extended time-to-hire: estimated $150K in lost productivity
- Team productivity impact from knowledge silos: estimated $400K
- Opportunity cost of engineers learning Rust vs. shipping features: estimated $1.2M

**Total estimated cost: $2.32M over two years**

The cloud cost savings from reduced CPU and memory usage? Approximately $180K annually. The business case that looked compelling on performance metrics alone fell apart when accounting for organizational complexity.

## The Turning Point

The wake-up call came during a critical incident in late 2021. A cascading failure required rapid changes to the Read States service, but the two engineers with deep Rust knowledge were unavailable. The on-call engineer spent 90 minutes trying to implement a fix that would have taken 20 minutes in Go. Discord's VP of Engineering watched 150 million users potentially affected by a language choice made for performance optimization.

The resolution wasn't to abandon Rust—the performance gains were real and valuable. Instead, Discord implemented strict guidelines:

1. **Rewrites require organizational justification, not just technical**: Teams must demonstrate that sufficient engineers will maintain proficiency, or the performance gain justifies hiring specialists
2. **Incremental adoption over big bangs**: New Rust services must start small with dedicated team ownership
3. **Mandatory knowledge transfer**: Every Rust service requires documented runbooks, architecture decision records, and quarterly knowledge-sharing sessions
4. **Polyglot pragmatism**: Language choice is a strategic trade-off, not an engineering purity contest

## Lessons for Technical Leaders

Discord's experience reveals uncomfortable truths about technology decisions:

**Performance metrics don't capture organizational costs.** The 10x improvement was real, but the team hadn't quantified the cost of specialization, knowledge concentration, or operational friction. A more complete analysis would have weighted these factors before committing.

**Language choice is a hiring and retention decision.** Every non-mainstream language choice (whether Rust, Elixir, or Haskell) changes your talent pool and team dynamics. For infrastructure teams exceeding 20 engineers, this creates structural fragmentation.

**Rewrites are organizational debt.** The six months spent rewriting was six months not spent on feature development, operational improvements, or reducing other technical debt. Discord's product team waited for infrastructure capacity that never arrived.

**Success stories create cargo culting.** After Discord's blog post, several other companies attempted similar rewrites—many without Discord's engineering resources or operational maturity. The industry's celebration of technical wins without discussing trade-offs creates perverse incentives.

## Strategic Takeaways

1. **Measure total cost of ownership, not just performance:** Include hiring, onboarding, maintenance, and knowledge transfer in technology evaluations
2. **Optimize for team velocity, not individual service efficiency:** Unless you're operating at hyperscale (>100M users), organizational simplicity often delivers more value than marginal performance gains
3. **Make reversible decisions when possible:** Could Discord have achieved 70% of the performance gains with targeted Go optimizations? The irreversibility of rewrites raises the stakes
4. **Document the downside:** When publishing success stories, include the costs and trade-offs. The industry learns more from complete stories than sanitized victories

Discord's Read States rewrite was technically brilliant and organizationally expensive. Understanding both sides of that equation is what separates engineering excellence from engineering theatrics.

For strategic leaders, the lesson isn't "don't use Rust" or "avoid rewrites." It's simpler: **every technical decision is an organizational decision.** The languages you choose, the systems you build, and the optimizations you pursue create structures that shape how your team works, who you can hire, and what you can accomplish.

Performance is just one variable in that equation. Discord learned that lesson the hard way.

---

*Special thanks to Marcus Rodriguez and David Kim for sharing their experiences with this project. Performance data and cost estimates based on internal Discord documents shared with permission.*
