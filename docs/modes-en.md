# Five Operating Modes

[RU version](modes-ru.md)

Project DNA has five modes. Each handles a different task in the project lifecycle.

```mermaid
flowchart LR
    subgraph "Lifecycle"
        M1["1. Create<br/>DNA"]
        M5["5. Create<br/>RNA"]
        WORK["Development"]
        M2["2. DNA<br/>Audit"]
        M3["3. Extract<br/>DNA"]
        M4["4. Mutate<br/>DNA"]
    end

    M1 -->|"New project"| M5
    M5 --> WORK
    WORK --> M2
    M2 -->|"DNA outdated"| M4
    M4 --> M5
    M3 -->|"Existing<br/>project"| M5

    style M1 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style M2 fill:#264653,stroke:#1a323d,color:#fff
    style M3 fill:#40916c,stroke:#2d6a4f,color:#fff
    style M4 fill:#e76f51,stroke:#c1440e,color:#fff
    style M5 fill:#52b788,stroke:#40916c,color:#000
```

---

## Mode 1: Create DNA

**When:** Starting a new project.

**Triggers:** *"create DNA"*, *"start project"*, *"let's begin"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Create DNA'"]
    
    START --> GATHER["Gather context<br/><i>Mission, entities, constraints,<br/>values, principles, specifics</i>"]
    
    GATHER --> CRYSTAL["Crystallization<br/><i>Not formalization (recording what you know),<br/>but discovery (finding what you know implicitly)</i>"]
    
    CRYSTAL --> DRAFT["Draft DNA<br/><i>Using template: 4 layers</i>"]
    
    DRAFT --> TEST["Technology test<br/><i>Remove all names —<br/>does meaning remain?</i>"]
    
    TEST --> Q{"Pass?"}
    Q -->|Yes| SAVE["DNA.md in project root"]
    Q -->|No| CRYSTAL
    
    SAVE --> OFFER["Offer to create<br/>RNA and first DevPrompt"]

    style CRYSTAL fill:#2d6a4f,stroke:#1b4332,color:#fff
    style TEST fill:#264653,stroke:#1a323d,color:#fff
```

### Example Dialogue

```
You: Create DNA for a sedimentary rock analysis project.

AI: Let's start with the mission. Why does this system exist?

You: We analyze grains in thin sections — their size, shape, 
     roundness. We need to automate what geologists do 
     manually under a microscope.

AI: Got it. A few clarifications:
    1. Roundness and Circularity — are these different 
       parameters or synonyms?
    2. Training dataset — is this a one-time resource 
       or a permanent asset?
    3. What's more important — processing speed or 
       classification accuracy?

You: Roundness and Circularity are strictly different things! 
     You must never confuse them...
```

**Key moment:** The Roundness/Circularity question is crystallization. The expert knew they were different but hadn't formulated it as an invariant until the AI asked.

---

## Mode 2: DNA Audit

**When:** You want to check whether code has drifted from invariants.

**Triggers:** *"DNA audit"*, *"check compliance"*, *"what are our invariants"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Run DNA audit'"]
    
    START --> READ_DNA["Read DNA.md"]
    READ_DNA --> STUDY["Study code, schemas,<br/>prompts, tests, configs"]
    
    STUDY --> CHECK["For each DNA section<br/>assess compliance"]
    
    CHECK --> REPORT["Report"]
    
    REPORT --> OK["✅ Compliant"]
    REPORT --> VIOL["❌ Violation"]
    REPORT --> NOTIMPL["⚠️ Not implemented"]
    REPORT --> UNDOC["🔍 In code but<br/>not documented in DNA"]

    style REPORT fill:#264653,stroke:#1a323d,color:#fff
    style VIOL fill:#e76f51,stroke:#c1440e,color:#fff
    style UNDOC fill:#e9c46a,stroke:#f4a261,color:#000
```

### What the Audit Produces

Diagnostics only, **no fix proposals**:

```
## DNA Audit: SciProof

### Ontology
✅ Fact ≠ Claim — implemented (tables facts, claims)
❌ Measurement ≠ Interpretation — merged in one model
⚠️ Fact type classification — not implemented

### Deontology  
✅ Originals immutable — immutable flag
🔍 "Chunks don't split well descriptions" — implemented 
   but invariant not recorded in DNA

### Axiology
✅ Completeness > speed — timeout 60 sec
❌ Distillation quality — no metrics in CI

### Require Manual Verification
- Correctness of ontological distinctions
  (only expert can confirm)
```

---

## Mode 3: Extract DNA

**When:** You have a project but no DNA. You want to extract invariants from what's already written.

**Triggers:** *"extract DNA"*, *"what are our invariants"*, *"let's start fresh"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Extract DNA'"]
    
    START --> STUDY["Study ALL project documents:<br/>code, README, CLAUDE.md, tests,<br/>DB schemas, prompts, comments"]
    
    STUDY --> FILTER["For each decision:<br/>'Is this true for PostgreSQL,<br/>flat files, AND an LLM with<br/>10M context alike?'"]
    
    FILTER --> Q{"Yes?"}
    Q -->|Yes| DNA_CANDIDATE["DNA candidate"]
    Q -->|No| IMPL["Implementation — not DNA"]
    
    DNA_CANDIDATE --> GROUP["Group by<br/>four layers"]
    
    GROUP --> FORMULATE["Formulate<br/>without technologies"]
    
    FORMULATE --> REVIEW["Propose to<br/>expert for review"]

    style FILTER fill:#264653,stroke:#1a323d,color:#fff
    style DNA_CANDIDATE fill:#2d6a4f,stroke:#1b4332,color:#fff
    style IMPL fill:#95d5b2,stroke:#52b788,color:#000
```

---

## Mode 4: Mutate DNA

**When:** Domain understanding has changed. Not the code, not the stack — the knowledge about the world itself.

**Triggers:** *"update DNA"*, *"this decision changed"*, *"why is it structured this way"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Update DNA —<br/>Roundness now includes<br/>multiple measurement methods'"]
    
    START --> SHOW["Show current<br/>DNA wording"]
    
    SHOW --> PROPOSE["Propose new<br/>wording"]
    
    PROPOSE --> JUSTIFY["Justify: why is this<br/>a DNA mutation, not just<br/>an implementation change?"]
    
    JUSTIFY --> Q{"Expert<br/>agrees?"}
    Q -->|Yes| UPDATE["Update DNA.md<br/>+ version table entry"]
    Q -->|No| REVISE["Revise wording"]
    REVISE --> PROPOSE
    
    UPDATE --> AUDIT["Suggest<br/>DNA audit"]

    style JUSTIFY fill:#e76f51,stroke:#c1440e,color:#fff
    style UPDATE fill:#2d6a4f,stroke:#1b4332,color:#fff
```

### Important Rule

The agent **proposes** a mutation but **does not commit** without the expert's consent. DNA is updated only by the project owner.

---

## Mode 5: Create RNA

**When:** DNA is ready, you need enforcement rules for a specific stack.

**Triggers:** *"create RNA"*, *"create harness"*, *"translate invariants into rules"*

### How It Works

```mermaid
flowchart TD
    START["Expert: 'Create RNA<br/>for Python/PostgreSQL/Claude Code'"]
    
    START --> READ_DNA["Read DNA.md"]
    
    READ_DNA --> STACK["Determine stack:<br/>language, DB, agent, CI"]
    
    STACK --> TRANSLATE["For each invariant:<br/>→ Stack-specific check<br/>→ Test / CI rule<br/>→ CLAUDE.md rule"]
    
    TRANSLATE --> GENERATE["Generate:<br/>RNA.md + Harness.md"]

    style TRANSLATE fill:#52b788,stroke:#40916c,color:#000
```

### Translation Example

| DNA (invariant) | RNA (Python/PostgreSQL) |
|-----------------|------------------------|
| "Fact ≠ Claim" | Models `Fact` and `Claim` are separate classes. Test: `test_fact_claim_separation()` |
| "Originals immutable" | `UPDATE originals SET ...` forbidden. SQL constraint: `BEFORE UPDATE RAISE EXCEPTION` |
| "Traceability" | `source_ref` NOT NULL in migration. CI: `SELECT count(*) WHERE source_ref IS NULL = 0` |
| "Completeness > speed" | Timeout 60 sec. No `LIMIT` without explicit justification in comments |

---

## Which Mode Do I Need?

```mermaid
flowchart TD
    START["What do you need?"]
    
    START --> Q1{"Have a project?"}
    Q1 -->|"No, starting"| M1["Mode 1:<br/>Create DNA"]
    Q1 -->|"Yes"| Q2{"Have DNA?"}
    
    Q2 -->|"No"| M3["Mode 3:<br/>Extract DNA"]
    Q2 -->|"Yes"| Q3{"What do you want?"}
    
    Q3 -->|"Check code"| M2["Mode 2:<br/>DNA Audit"]
    Q3 -->|"DNA outdated"| M4["Mode 4:<br/>Mutate DNA"]
    Q3 -->|"New stack/agent"| M5["Mode 5:<br/>Create RNA"]

    style M1 fill:#2d6a4f,stroke:#1b4332,color:#fff
    style M2 fill:#264653,stroke:#1a323d,color:#fff
    style M3 fill:#40916c,stroke:#2d6a4f,color:#fff
    style M4 fill:#e76f51,stroke:#c1440e,color:#fff
    style M5 fill:#52b788,stroke:#40916c,color:#000
```
