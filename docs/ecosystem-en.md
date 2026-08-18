# Three-Skill Ecosystem

[RU version](ecosystem-ru.md)

## Why Three Skills, Not One?

AI-assisted development breaks in three different places:

1. **The agent solves the wrong problem** — doesn't understand what matters in the domain
2. **Both sides make structural errors** — architect and Claude Code alike, each in its own way
3. **The result looks correct but isn't** — pseudo-rigor, beautiful but wrong output

One skill can't cover all three because these are **different types of knowledge**:

```mermaid
graph TB
    subgraph "project-dna"
        DNA_Q["WHAT?<br/><i>What can never be violated?<br/>Why is the world structured this way?</i>"]
    end

    subgraph "architect-cc-workflow"
        ARCH_Q["HOW?<br/><i>How do both sides catch<br/>each other's errors?</i>"]
    end

    subgraph "research-with-ai"
        RES_Q["TRUE?<br/><i>How do we know this is correct?<br/>Is this an illusion?</i>"]
    end

    DNA_Q -->|"invariants define<br/>what to check"| ARCH_Q
    ARCH_Q -->|"error patterns show<br/>what needs verification"| RES_Q
    RES_Q -->|"truth criteria<br/>refine invariants"| DNA_Q

    style DNA_Q fill:#2d6a4f,stroke:#1b4332,color:#fff
    style ARCH_Q fill:#e76f51,stroke:#c1440e,color:#fff
    style RES_Q fill:#264653,stroke:#1a323d,color:#fff
```

## Activation Order

The skills don't fire simultaneously — each owns a phase:

```mermaid
flowchart LR
    S8["research-with-ai<br/>Mode 8<br/><i>domain scouting</i>"]
    PD["project-dna<br/>Modes 1-6<br/><i>invariants</i>"]
    ACC["architect-cc-workflow<br/><i>execution</i>"]
    RES["research-with-ai<br/>Modes 1-7<br/><i>result epistemics</i>"]

    S8 -->|"domain_scouting.md"| PD
    PD -->|"DNA.md + RNA"| ACC
    ACC -->|"results"| RES
    RES -.->|"invariant mutation"| PD

    style S8 fill:#264653,stroke:#1a323d,color:#fff
    style PD fill:#2d6a4f,stroke:#1b4332,color:#fff
    style ACC fill:#e76f51,stroke:#c1440e,color:#fff
    style RES fill:#264653,stroke:#1a323d,color:#fff
```

**Key point:** `project-dna` Mode 1 begins with a **scouting readiness check**. If the domain hasn't been scouted, the skill refuses to formulate DNA and routes you to `research-with-ai` Mode 8. This is a gate, not a suggestion.

## Each Skill in Detail

### project-dna — Invariants

**Domain:** What can never be violated and why.

**Six modes:** create DNA, DNA audit, extract, mutate, create RNA, subtraction audit.

**Three key mechanisms:**

| Mechanism | What it solves |
|-----------|---------------|
| **Violation indicator** | An invariant with no observable violation indicator is a slogan. Every invariant must name a concrete code/data state that shows it's broken |
| **ASSUMPTIONS.md** | Separating invariants from hypotheses. Without it, DNA either fossilizes or becomes worthless |
| **Negative invariants** | What must never appear. Protection against accretion drift, which is invisible at the level of any single change |

**Example invariant with violation indicator:**

> "No conclusion is published without a source reference."
> **Violation indicator:** the output artifact contains a record with a non-empty value and an empty provenance field.

True for PostgreSQL, MongoDB, and flat files alike. This is DNA.

---

### architect-cc-workflow — Execution Discipline

**Domain:** How both sides catch each other's structural errors.

**Fundamental change:** the protocol is **bidirectional**. In the architect + Claude Code pair, both sides are LLMs with structural failure modes. The defenses must be symmetric.

#### Architect-side errors (~10% rate)

| Cause | Manifestation |
|-------|--------------|
| No persistent state | Every message is a fresh context; repo state reconstructed from memory |
| Pattern matching from training | Confidently generates plausible-but-wrong assertions |
| Confabulation | Claims knowledge of literature/code without actual verification |

#### Claude Code-side errors — four root causes

| Cause | Manifestation |
|-------|--------------|
| **Likely-not-true generation** | The model generates the statistically probable, not the true. Hence sycophancy, hallucination, and **self-certification of completion** ("task complete" as format continuation, not as fact) |
| **Attention degradation** | Tunnel vision (a rule mid-prompt is ignored) + context drift (by turn 30, rules from the session start are forgotten). Degradation is abrupt, not gradual |
| **Numeric/temporal blindness** | Numbers tokenize as text; there's no symbolic arithmetic. A date is a probability, not a fact |
| **No trust boundary** | The model doesn't distinguish instruction from data. Prompt injection via a poisoned document |

**Core principle:** "there will be no healthy agent." The goal isn't to eliminate errors but to build a **closed loop** (task → action → external check → correction) where errors stay under control.

#### Key Defenses

| Defense | What it prevents |
|---------|-----------------|
| Verification protocol (§3) | Architect issues a spec with unverified constants and assumptions |
| Assumptions section (§4) | Implicit assumptions unwritten; the agent fills gaps |
| Session-start refresh (§5.1) | Agent "remembers" repo state from a prior session — but it's stale |
| Critical rules placement (§5.3) | A rule in the middle of a long context is ignored |
| Probe-first (§8) | Numeric constraints without empirical pre-flight verification |
| **No self-certification (§11)** | Agent declares "done, tests pass" — and the tests never ran |
| **Confidence markers (§12)** | Unclear what was verified programmatically vs pulled from training data |
| **Raw artifact review (§13)** | Architect trusts the summary instead of reading raw output |
| **Numeric hard rule (§14)** | Arithmetic and dates via model reasoning instead of code |
| **BLOCK/NOTE/SILENCE (§15)** | Agent either narrates every step or vanishes for 40 minutes |
| **Regression suite (§16)** | A skill without tests is a set of beliefs about what works |

#### Communication Decision Function (§15)

Not a list of occasions, but a rule derived from cost asymmetry — comparing the cost of the architect learning about it **later** against the cost of interrupting **now**:

|  | On DevPrompt plan | Diverges from plan |
|---|---|---|
| **Reversible** | SILENCE | NOTE |
| **Irreversible, in mandate** | NOTE **before** acting | BLOCK |
| **Irreversible, outside mandate** | BLOCK | BLOCK |

**Signal budget:** ≤1 BLOCK, ≤3-5 NOTE per phase. Exceeding it signals not an agent problem but a **DevPrompt quality** problem: the mandate was underspecified. The architect fixes the DevPrompt, not the agent.

Why this isn't bureaucracy: each unnecessary interruption trains reflexive approval. After a few trivial BLOCKs, a real BLOCK goes unread. Over-asking isn't noise — it's **disarming the mechanism**.

---

### research-with-ai — Epistemics

**Domain:** What counts as truth when working with AI.

**What it does:**
- Establishes an epistemic framework: AI produces work, the human bears responsibility for truth
- Seven anchors of truth — mechanisms compensating specific defects of AI as a research assistant
- Mode 8 — domain scouting, the **mandatory entry point** into project-dna

**Core principle:**
> AI can produce a beautiful, detailed, confident result that is completely wrong. The human's job is not to believe, but to verify.

**Seven anchors:** pre-registration, generator/critic separation, external reproducibility, reality cross-check, adversarial verification, significance calibration, epistemic journal.

---

## How They Interlock

The skills don't merely complement each other — their mechanisms form **pairs**:

```mermaid
graph LR
    subgraph "project-dna"
        P1["Violation indicator"]
        P2["Pre-action protocol"]
        P3["Numeric invariants<br/>(section 7)"]
    end

    subgraph "architect-cc-workflow"
        A1["Regression suite<br/>(§16)"]
        A2["Phase-end report"]
        A3["Verification anchors<br/>(§14.1)"]
    end

    P1 <-->|"every rule<br/>has a test"| A1
    P2 <-->|"before change ↔<br/>after phase"| A2
    P3 <-->|"WHY the value ↔<br/>WHAT it is"| A3

    style P1 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style P2 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style P3 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style A1 fill:#e76f51,stroke:#c1440e,color:#fff
    style A2 fill:#e76f51,stroke:#c1440e,color:#fff
    style A3 fill:#e76f51,stroke:#c1440e,color:#fff
```

| Pair | Shared principle |
|------|-----------------|
| Violation indicator ↔ Regression suite | A rule you can't check observably isn't a rule. In DNA that's the violation indicator; in the skill, the anti-pattern test |
| Pre-action protocol ↔ Phase-end report | Recording decisions on both sides of a change: before (which invariant does this serve) and after (what wasn't verified, which decisions went unapproved) |
| Numeric invariants ↔ Verification anchors | DNA says **why** a quantity is what it is; ANCHORS.md says **what** it concretely is |

## Scenario: New Project from Scratch

```mermaid
sequenceDiagram
    participant E as Expert
    participant RES as research-with-ai
    participant DNA as project-dna
    participant ARCH as architect-cc-workflow
    participant CC as Claude Code

    E->>RES: "Starting a project on topic X"
    RES->>RES: Mode 8: five scouting questions
    RES-->>E: domain_scouting.md

    E->>DNA: "Create DNA"
    DNA->>DNA: Step 0: scouting readiness check ✓
    DNA->>E: Crystallization dialogue
    DNA->>E: "What's the violation indicator?"
    DNA-->>E: DNA.md + ASSUMPTIONS.md

    E->>DNA: "Create RNA for Python/PostgreSQL"
    DNA-->>E: RNA.md + CLAUDE.md + ANCHORS.md

    E->>ARCH: Formulates DevPrompt
    ARCH->>ARCH: Assumptions section + signal budget
    ARCH-->>CC: Verified DevPrompt

    CC->>CC: Session-start refresh (§5.1)
    CC->>ARCH: Verification report (§3)
    ARCH-->>CC: Confirmation

    CC->>CC: Implementation
    CC->>E: NOTE (divergence from plan)
    CC-->>E: PHASE_REPORT.md with confidence markers

    E->>E: Raw artifact review (§13)
    E->>DNA: "Run DNA audit"
    DNA-->>E: Compliance / violations / gaps

    E->>RES: "Are the results valid?"
    RES->>RES: Adversarial check (Anchor 5)
    RES-->>E: Verification or red flags
```

## Scenario: Problem Discovered

```mermaid
flowchart TD
    BUG["Problem discovered"]

    BUG --> Q1{"Does code violate<br/>a DNA invariant?"}
    Q1 -->|Yes| DNA_AUDIT["project-dna:<br/>DNA audit"]
    Q1 -->|No| Q2{"Agent reported 'done'<br/>when it wasn't?"}

    Q2 -->|Yes| SELF["architect-cc-workflow:<br/>§11 + §13<br/>raw artifact review"]
    Q2 -->|No| Q3{"Did architect give<br/>a poor instruction?"}

    Q3 -->|Yes| ARCH_FIX["architect-cc-workflow:<br/>§3 verification<br/>§4 assumptions"]
    Q3 -->|No| Q4{"Result looked correct<br/>but was wrong?"}

    Q4 -->|Yes| RES_CHECK["research-with-ai:<br/>Anchor 5"]
    Q4 -->|No| Q5{"Project accumulated<br/>cruft?"}

    Q5 -->|Yes| SUB["project-dna:<br/>Mode 6<br/>subtraction audit"]
    Q5 -->|No| REGULAR["Standard bugfix"]

    style DNA_AUDIT fill:#2d6a4f,stroke:#1b4332,color:#fff
    style SELF fill:#c1440e,stroke:#8b0000,color:#fff
    style ARCH_FIX fill:#e76f51,stroke:#c1440e,color:#fff
    style RES_CHECK fill:#264653,stroke:#1a323d,color:#fff
    style SUB fill:#f4a261,stroke:#e76f51,color:#000
```

## When to Use Which Skill

| Situation | Skill | Why |
|-----------|-------|-----|
| Starting a project, domain unfamiliar | **research-with-ai** Mode 8 | DNA without scouting is a declaration |
| Domain scouted, need invariants | **project-dna** Mode 1 | Fix them before coding begins |
| Writing a DevPrompt | **architect-cc-workflow** | Assumptions section + signal budget |
| Agent said "done" | **architect-cc-workflow** §11, §13 | Self-reporting is structurally unreliable |
| Numbers in the report look off | **architect-cc-workflow** §14 | The model treats numbers as text |
| Agent interrupts over trivia | **architect-cc-workflow** §15 | Over-asking disarms BLOCK |
| Code drifted from intent | **project-dna** Mode 2 | DNA audit |
| Project has sprawled | **project-dna** Mode 6 | Subtraction audit |
| Changing stack | **project-dna** Mode 5 | DNA stays, RNA is rewritten |
| "Too good" results | **research-with-ai** Anchor 5 | Sign of pseudo-rigor |
| Changed a skill | **architect-cc-workflow** §16 | A change without a test is incomplete |

## Boundaries: What These Skills Don't Do

- **project-dna** doesn't write code or manage the development process
- **architect-cc-workflow** doesn't define the domain — it takes invariants from DNA
- **research-with-ai** doesn't replace peer review — it strengthens it
- None of these skills replace human domain expertise — they **amplify** it

## Origin

Extracted from the practice of developing SciProof and sat-revisit-tool (2025-2026). Key patterns emerged across 50+ Claude Code sessions: unit tests passed but integration broke; the architect made ~10% errors due to LLM structural limits; the agent reported completion by format rather than by fact; results looked rigorous but were incorrect.
