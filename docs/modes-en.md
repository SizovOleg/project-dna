# Six Operating Modes

[RU version](modes-ru.md)

Project DNA has six modes. Each handles a different task in the project lifecycle.

```mermaid
flowchart LR
    SCOUT["research-with-ai<br/>Mode 8:<br/>domain scouting"]

    subgraph "DNA Lifecycle"
        M1["1. Create<br/>DNA"]
        M5["5. Create<br/>RNA"]
        WORK["Development"]
        M2["2. DNA<br/>Audit"]
        M3["3. Extract<br/>DNA"]
        M4["4. Mutate<br/>DNA"]
        M6["6. Subtraction<br/>Audit"]
    end

    SCOUT -->|"domain_scouting.md"| M1
    M1 --> M5
    M5 --> WORK
    WORK --> M2
    M2 -->|"DNA outdated"| M4
    M4 --> M5
    M3 -->|"existing<br/>project"| M5
    WORK -->|"every 2-3 months"| M6
    M6 -->|"rejected →<br/>section 6"| M4

    style SCOUT fill:#264653,stroke:#1a323d,color:#fff
    style M1 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style M2 fill:#264653,stroke:#1a323d,color:#fff
    style M3 fill:#40916c,stroke:#2d6a4f,color:#fff
    style M4 fill:#e76f51,stroke:#c1440e,color:#fff
    style M5 fill:#52b788,stroke:#40916c,color:#000
    style M6 fill:#f4a261,stroke:#e76f51,color:#000
```

---

## Mode 1: Create DNA

**When:** Starting a new project.

**Triggers:** *"create DNA"*, *"start project"*, *"let's begin"*

### Step 0: Domain Scouting Readiness Check (mandatory)

DNA without domain scouting is a declarative document resting on the plausibility of AI phrasing or the authority of someone else's sources — not on justified premises.

Before formulating DNA — five control questions:

| Question | Readiness criterion |
|----------|--------------------|
| **Ontological** | Can you map the domain entities against 3+ independent precedents? |
| **Precedent** | Do you know 3-5 analogous projects, including at least one failed, and their actual failure modes? |
| **Categorical** | Have you identified where AI will wrongly transfer categories from training data? |
| **Conflict** | Do you know the real axiological dilemmas in this area and how they were resolved? |
| **Boundary** | Can you separate the project's object from adjacent ones with concrete criteria? |

Any answer of "not sure" → **do not proceed to step 1**. Go to `research-with-ai`, Mode 8.

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Create DNA'"]

    START --> GATE{"Scouting<br/>done?"}
    GATE -->|"No"| SCOUT["research-with-ai<br/>Mode 8"]
    SCOUT --> GATE
    GATE -->|"Yes"| GATHER["Gather context<br/><i>Mission, entities, constraints, values,<br/>principles, NEGATIVE invariants,<br/>numeric bounds</i>"]

    GATHER --> CRYSTAL["Crystallization<br/><i>Not formalization (recording what you know),<br/>but discovery (finding what you know implicitly)</i>"]

    CRYSTAL --> SIGN{"For each invariant:<br/>is there a violation<br/>indicator?"}
    SIGN -->|"No"| SPLIT["Split into:<br/>value → axiology<br/>hypothesis → ASSUMPTIONS.md<br/>too broad → narrow it"]
    SPLIT --> CRYSTAL
    SIGN -->|"Yes"| DRAFT["Draft DNA"]

    DRAFT --> TEST["Technology test<br/><i>Remove all names —<br/>does meaning remain?</i>"]

    TEST --> Q{"Pass?"}
    Q -->|"Yes"| PLACE["Key invariants —<br/>at the start AND end of document"]
    Q -->|"No"| CRYSTAL

    PLACE --> SAVE["DNA.md + ASSUMPTIONS.md<br/>in project root"]

    style CRYSTAL fill:#2d6a4f,stroke:#1b4332,color:#fff
    style SIGN fill:#264653,stroke:#1a323d,color:#fff
    style SPLIT fill:#e76f51,stroke:#c1440e,color:#fff
    style PLACE fill:#f4a261,stroke:#e76f51,color:#000
```

### Why Key Invariants Are Duplicated

A rule sitting in the middle of a long context is statistically ignored by the agent. This is a property of attention architecture, not model laziness. So key invariants go at the **start** of the document and are duplicated at the **end**.

Details: `architect-cc-workflow` §5.3.

### Example Dialogue

```
You: Create DNA for a sedimentary rock analysis project.

AI: First let's check scouting readiness. Can you map the domain
    entities against 3+ independent precedents?

You: Yes — three papers on grain morphometry, two of them with
    different classification approaches.

AI: [...four remaining questions...]
    Good, scouting is sufficient. Let's start with the mission.

You: We analyze grains in thin sections — size, shape, roundness.
    Automating what geologists do manually.

AI: Clarifications:
    1. Roundness and Circularity — different parameters or synonyms?
    2. Training dataset — one-time resource or permanent asset?

You: Roundness and Circularity are strictly different!

AI: That's an invariant. What's the violation indicator? What would
    I see in code or data if it were broken?

You: If one column holds values of both parameters, or if one is
    computed from the other.
```

**Two key moments:** the Roundness/Circularity question is crystallization (the expert knew but hadn't articulated). The violation indicator question turns a phrase into a checkable condition.

---

## Mode 2: DNA Audit

**When:** Checking whether code has drifted from invariants.

**Triggers:** *"DNA audit"*, *"check compliance"*

**Regular triggers** (not only on request): phase completion, stack change, returning after a pause > 1 month, before publication or handoff.

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Run DNA audit'"]

    START --> READ["Read DNA.md<br/>+ ASSUMPTIONS.md"]

    READ --> SELFCHECK["Check DNA itself<br/>for soundness"]

    SELFCHECK --> DIAG1["🩺 Invariant without violation indicator → slogan<br/>🩺 Invariant that is a hypothesis → to ASSUMPTIONS<br/>🩺 Axiology without dilemmas → a list, not a rule"]

    DIAG1 --> STUDY["Study code, schemas,<br/>prompts, tests, configs"]

    STUDY --> CHECK["For each DNA section<br/>assess compliance"]

    CHECK --> REPORT["Report"]

    REPORT --> OK["✅ Compliant"]
    REPORT --> VIOL["❌ Violation<br/><i>citing the indicator</i>"]
    REPORT --> NOTIMPL["⚠️ Not implemented"]
    REPORT --> UNDOC["🔍 In code,<br/>not in DNA"]
    REPORT --> NEGVIOL["🚫 Negative invariant<br/>violated"]

    style SELFCHECK fill:#f4a261,stroke:#e76f51,color:#000
    style REPORT fill:#264653,stroke:#1a323d,color:#fff
    style VIOL fill:#e76f51,stroke:#c1440e,color:#fff
    style NEGVIOL fill:#c1440e,stroke:#8b0000,color:#fff
```

### Checking DNA Itself — Before Checking Code

New compared to earlier versions: the audit starts by diagnosing the **quality of the DNA itself**, not the code. There's no point checking code against slogans.

```
🩺 Invariant quality:
- "The system must be reliable" — slogan with no violation
  indicator, needs reformulation
- "Library X doesn't support Y" — hypothesis,
  move to ASSUMPTIONS.md
- Section 4 lists values without resolved dilemmas —
  an agent cannot apply a list
```

### What the Audit Produces

Diagnostics only, **no fix proposals**:

```
## DNA Audit: SciProof

### Ontology
✅ Fact ≠ Claim — implemented (tables facts, claims)
❌ Measurement ≠ Interpretation — merged into one model
   Violation indicator (DNA §3.2): one table holds both measured
   and interpreted values → confirmed

### Negative Invariants
🚫 DNA §6.3 forbids ORM abstractions over SQL —
   core/repository.py grew an ORM-like layer

### Require Manual Verification
- Correctness of ontological distinctions
```

---

## Mode 3: Extract DNA

**When:** The project exists, DNA doesn't.

**Triggers:** *"extract DNA"*, *"what are our invariants"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Extract DNA'"]

    START --> STUDY["Study ALL documents:<br/>code, README, CLAUDE.md, tests,<br/>DB schemas, prompts, comments"]

    STUDY --> F1{"True for another DB,<br/>for flat files AND for<br/>a model with 10M context?"}
    F1 -->|"No"| IMPL["Implementation —<br/>TechnicalDesign"]
    F1 -->|"Yes"| F2{"What would have to happen<br/>for this to stop<br/>being true?"}

    F2 -->|"We might find<br/>we were wrong"| HYP["Hypothesis →<br/>ASSUMPTIONS.md"]
    F2 -->|"Nothing, it's a<br/>property of the domain"| F3{"Can a violation<br/>indicator be<br/>formulated?"}

    F3 -->|"No"| BACK["Back to step 2<br/>or into axiology"]
    F3 -->|"Yes"| DNA_C["DNA invariant"]

    DNA_C --> NEG["Separately hunt negatives:<br/>'What did you decide NOT to do, and why?'"]

    NEG --> GROUP["Group by<br/>four layers"]
    GROUP --> REVIEW["Propose<br/>for review"]

    style F1 fill:#264653,stroke:#1a323d,color:#fff
    style F2 fill:#264653,stroke:#1a323d,color:#fff
    style F3 fill:#264653,stroke:#1a323d,color:#fff
    style DNA_C fill:#2d6a4f,stroke:#1b4332,color:#fff
    style HYP fill:#e9c46a,stroke:#f4a261,color:#000
    style NEG fill:#e76f51,stroke:#c1440e,color:#fff
    style IMPL fill:#95d5b2,stroke:#52b788,color:#000
```

### Negative Invariants Are Almost Never Written Down

But they live in the decisions: what the team rejected, why something isn't automated, which dependencies are banned. You have to ask directly: **"What did you decide NOT to do, and why?"**

---

## Mode 4: Mutate DNA

**When:** Domain understanding has changed.

**Triggers:** *"update DNA"*, *"this decision is outdated"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Update DNA'"]

    START --> SHOW["Show current<br/>wording"]

    SHOW --> CAT{"Invariant<br/>or hypothesis?"}
    CAT -->|"Hypothesis"| ASSUM["Edit ASSUMPTIONS.md<br/>DNA untouched"]
    CAT -->|"Invariant"| PROPOSE["Propose wording<br/>+ violation indicator"]

    PROPOSE --> JUSTIFY["Justify: why is this a DNA<br/>mutation and not an<br/>implementation change?"]

    JUSTIFY --> Q{"Expert<br/>agrees?"}
    Q -->|"No"| PROPOSE
    Q -->|"Yes"| UPDATE["Update DNA.md<br/>+ version table"]

    UPDATE --> AUDIT["Run DNA audit<br/>to surface divergences"]

    style CAT fill:#264653,stroke:#1a323d,color:#fff
    style ASSUM fill:#e9c46a,stroke:#f4a261,color:#000
    style JUSTIFY fill:#e76f51,stroke:#c1440e,color:#fff
    style UPDATE fill:#2d6a4f,stroke:#1b4332,color:#fff
```

### Important Rule

The agent **proposes** a mutation but **does not commit** without expert consent. DNA is updated only by the project owner.

The first branch is new: a significant share of "update DNA" requests actually concern hypotheses. Those are edited in `ASSUMPTIONS.md`, leaving DNA untouched.

---

## Mode 5: Create RNA

**When:** DNA is ready, you need enforcement rules for the stack.

**Triggers:** *"create RNA"*, *"create harness"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Create RNA<br/>for Python/PostgreSQL/Claude Code'"]

    START --> READ["Read DNA.md"]
    READ --> STACK["Determine stack:<br/>language, DB, agent, CI"]

    STACK --> T1["Violation indicator →<br/>check in stack terms"]
    STACK --> T2["Section 7 (numeric) →<br/>ANCHORS.md"]
    STACK --> T3["Section 6 (negative) →<br/>bans in CLAUDE.md + lint"]

    T1 --> GEN["RNA.md / Harness.md"]
    T2 --> GEN
    T3 --> GEN

    style T1 fill:#52b788,stroke:#40916c,color:#000
    style T2 fill:#e9c46a,stroke:#f4a261,color:#000
    style T3 fill:#e76f51,stroke:#c1440e,color:#fff
```

### The Violation Indicator *Is* the Check Specification

An invariant without a violation indicator is **untranslatable into RNA**. That's another reason to demand one at DNA creation time.

| DNA | Violation indicator | RNA (Python/PostgreSQL) |
|-----|--------------------|------------------------|
| "Fact ≠ Claim" | One table holds both types | Models `Fact` and `Claim` separate. Test: `test_fact_claim_separation()` |
| "Originals immutable" | An UPDATE path to originals exists | SQL trigger `BEFORE UPDATE RAISE EXCEPTION` |
| "Traceability" | Record with non-empty value and empty provenance | `source_ref NOT NULL`. CI: `SELECT count(*) WHERE source_ref IS NULL = 0` |

### Numeric Invariants → ANCHORS.md

DNA section 7 (numeric domain invariants) generates `ANCHORS.md` — a set of self-check anchors for the agent.

**Division of responsibility:** DNA says **why** a quantity is what it is; `ANCHORS.md` and the constants file say **what** it concretely is.

Details: `architect-cc-workflow` §14.1.

---

## Mode 6: Subtraction Audit

**When:** Regularly (every 2-3 months) for active projects.

**Triggers:** *"what to remove"*, *"the project has sprawled"*, *"let's clean up"*

### Why

Projects sprawl through **accretion**: each addition looks reasonable, the sum destroys coherence. The default working mode is to add. The subtraction audit is deliberate counter-pressure.

Adding features can turn a tool into the very thing it was built against. Deleting half the roadmap is sometimes the best product decision available.

### How It Works

```mermaid
flowchart TD
    START["Expert: 'What should we remove?'"]

    START --> READ["Read DNA.md:<br/>section 1 (mission)<br/>section 6 (negative invariants)"]

    READ --> LOOP["For each component/feature"]

    LOOP --> Q1{"Does it serve the<br/>mission directly?"}
    LOOP --> Q2{"If removed —<br/>what actually breaks,<br/>not hypothetically?"}
    LOOP --> Q3{"Does it contradict<br/>negative invariants?"}
    LOOP --> Q4{"Would we make this<br/>decision again today?"}

    Q1 --> LISTS["Three lists"]
    Q2 --> LISTS
    Q3 --> LISTS
    Q4 --> LISTS

    LISTS --> L1["Deletion<br/>candidates"]
    LISTS --> L2["Candidates for<br/>negative invariants"]
    LISTS --> L3["Keep, despite<br/>doubts"]

    L1 --> OWNER["Propose to owner<br/><i>the agent does not delete</i>"]
    L2 --> OWNER
    L3 --> OWNER

    OWNER --> SECTION6["Rejected → DNA section 6<br/>with reason, so it stays gone"]

    style LISTS fill:#f4a261,stroke:#e76f51,color:#000
    style L1 fill:#e76f51,stroke:#c1440e,color:#fff
    style L2 fill:#264653,stroke:#1a323d,color:#fff
    style SECTION6 fill:#2d6a4f,stroke:#1b4332,color:#fff
```

### What the Audit Produces

```
### Deletion Candidates
- XML export — doesn't serve the mission, added for a single
  one-off request. Frees 340 LOC + the lxml dependency

### Candidates for Negative Invariants
- Automatic interpretation of results — rejected twice this
  year. Record in section 6 so it stops coming back

### Keep, Despite Doubts
- CLI interface — looks like duplication of the web UI, but it's
  the only path for batch processing
```

**Important:** the agent does not delete. Deletion is the owner's decision, like DNA mutation.

---

## Which Mode Do I Need?

```mermaid
flowchart TD
    START["What do you need?"]

    START --> Q1{"Have a project?"}
    Q1 -->|"No, starting"| Q0{"Domain<br/>scouted?"}
    Q0 -->|"No"| SCOUT["research-with-ai<br/>Mode 8"]
    Q0 -->|"Yes"| M1["Mode 1:<br/>Create DNA"]
    SCOUT --> M1

    Q1 -->|"Yes"| Q2{"Have DNA?"}
    Q2 -->|"No"| M3["Mode 3:<br/>Extract DNA"]
    Q2 -->|"Yes"| Q3{"What do you want?"}

    Q3 -->|"Check code"| M2["Mode 2:<br/>DNA Audit"]
    Q3 -->|"DNA outdated"| M4["Mode 4:<br/>Mutate DNA"]
    Q3 -->|"New stack/agent"| M5["Mode 5:<br/>Create RNA"]
    Q3 -->|"Project sprawled"| M6["Mode 6:<br/>Subtraction Audit"]

    style SCOUT fill:#264653,stroke:#1a323d,color:#fff
    style M1 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style M2 fill:#264653,stroke:#1a323d,color:#fff
    style M3 fill:#40916c,stroke:#2d6a4f,color:#fff
    style M4 fill:#e76f51,stroke:#c1440e,color:#fff
    style M5 fill:#52b788,stroke:#40916c,color:#000
    style M6 fill:#f4a261,stroke:#e76f51,color:#000
```
