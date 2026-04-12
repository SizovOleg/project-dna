---
name: project-dna
description: "Create, maintain, and audit Project DNA — a root project document containing implementation-independent invariants. Use when: starting a new project from scratch, formulating architectural decisions, auditing existing code against invariants, updating a domain model, or reconsidering project priorities. Triggers: 'create DNA', 'start project', 'check compliance', 'DNA audit', 'what are our invariants', 'update DNA', 'why is it structured this way', 'what must not be broken', 'let's start from scratch'. Also when launching a new project, reviewing architecture, refactoring, or changing tech stack."
license: MIT
---

# Project DNA — Skill for Creating and Auditing Root Project Documents

## What is DNA

DNA (Decision Nucleic Acid) — a compact document (2–5 pages) containing only decisions that hold true **regardless of implementation**. No technology names, models, or frameworks — only "what" and "why".

DNA is the root of project documentation. All other documents (Requirements, TechnicalDesign, DevPrompts, CLAUDE.md) are derived from it.

## Philosophical Framework

DNA consists of four layers:

```
DNA = Ontology (what exists and how it's connected)
    + Deontology (what is permitted and what is forbidden)
    + Axiology (what is valuable and what is not)
    + Praxeology (how to act)
```

**Ontology** — what entities exist, how they're related, what categories are valid.
**Deontology** — what is permitted, what is forbidden. Constraints from practice.
**Axiology** — what is valuable, what is not. Priorities and quality criteria.
**Praxeology** — how to act. Principles of evolution and work.

## Documentation Hierarchy

```
DNA.md — invariants, for humans
  ↓
RNA / Harness — enforcement, for the agent
  ├── CLAUDE.md / AGENTS.md (contract with the agent)
  ├── Skills (codified experience)
  └── Plugins / MCP (tooling)
  ↓
Requirements → TechnicalDesign → DevPrompts → Code
  ↑
DNA audit (feedback loop)
```

## Mode 1: Creating DNA for a New Project

### When to use
The user is starting a new project or says "start with DNA".

### Process

1. **Gather context.** Ask the user (or extract from prompts/documents):
   - Why does the system exist? (mission — 1-2 sentences)
   - What entities exist in the domain? (ontology)
   - What must not be violated? (deontology)
   - What matters more than what? (axiology)
   - What are the working principles? (praxeology)
   - Domain specifics (terminology, sources, pitfalls)

2. **Crystallize, don't just formalize.** Your role is not to record what the user already knows, but to help them discover what they know implicitly. Ask questions that turn intuition into precise statements. "You said 'measure correctly' — what exactly does 'correctly' mean? What result would you reject?" Users often don't know their own decisions until they hear the wrong version.

3. **Draft the DNA** using the template below.

4. **Verify:** mentally remove all technology names. If DNA loses its meaning — it contains implementation details, clean them out.

5. **Place** `DNA.md` in the project root.

6. **Offer** to create RNA/Harness and the first DevPrompt based on the DNA.

### DNA Template

```markdown
# [Project Name] — Project DNA

**Version:** 1.0
**Date:** [date]

---

## Purpose of This Document

Root project document. Contains decisions, constraints, and quality criteria
independent of implementation. All other documents are derived from DNA.

### Rules for the AI Agent
1. Read the DNA before starting work.
2. Every decision must be compatible with the invariants.
3. On conflict — report, do not silently violate.
4. DNA is updated only by the project owner.

---

## 1. Mission

[Why the system exists. 1-2 sentences.]

---

## 2. Domain Model (Ontology)

### 2.1. Entities
[What entities exist and why they are separated.]

### 2.2. Fundamental Distinctions
[X ≠ Y, because…]

### 2.3. Typologies
[Initial types/categories, if applicable.]

---

## 3. Constraints (Deontology)

### 3.1. [Invariant 1]
[Description and justification.]

### 3.2. [Invariant 2]
...

---

## 4. Quality Criteria (Axiology)

### 4.1. [Stage/Component]
[What "works correctly" means.]

### 4.2. Priorities
[What matters more than what.]

---

## 5. Principles (Praxeology)

### 5.1. Economic Model
[What is free, what costs money, where is the boundary.]

### 5.2. Scale
[What volume is it designed for.]

### 5.3. Evolution
[How the system should develop.]

---

## 6. Domain Specifics

[What makes this task unlike a generic solution.]

---

## 7. Typical Queries / Scenarios

[What questions/tasks is the system designed for.]

---

## Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | [date] | Initial formalization |
```

## Mode 2: DNA Audit of an Existing Project

### When to use
The user says "check DNA compliance" / "DNA audit" / after a major development stage.

### Process

1. **Read DNA.md** in the project root.

2. **Study the code, DB schemas, prompts, tests, configuration.**

3. **For each DNA section** output:

```
### [DNA Section]

✅ Compliant:
- [what is implemented correctly]

❌ Violations:
- [what contradicts DNA, file/line]

⚠️ Not implemented:
- [what is in DNA but not in code]

🔍 Not documented in DNA:
- [what is in code but not in DNA]
```

4. **Do not propose fixes** in this pass. Diagnostics only.

5. **Note** what requires manual verification (OCR quality, domain-specific correctness).

## Mode 3: Extracting DNA from an Existing Project

### When to use
The project already exists, DNA is not formalized. The user says "extract DNA" / "what are our invariants".

### Process

1. **Study** all project documents (Requirements, TechnicalDesign, CLAUDE.md, prompts, code).

2. **For each decision ask:** "Is this true for PostgreSQL, flat files, and an LLM with 10M context alike?"
   - Yes → DNA
   - No → implementation (TechnicalDesign)

3. **Group** by the four layers (ontology, deontology, axiology, praxeology).

4. **Formulate** without technologies.

5. **Propose** to the user for review.

## Mode 4: DNA Mutation

### When to use
The user says "update DNA" / "this decision is outdated" / "add to DNA".

### Process

1. **Show** the current version of the affected section.
2. **Propose** the wording of the change.
3. **Justify** — why this is a DNA mutation, not an implementation change.
4. **After approval** — update DNA.md with the new version and a versioning table entry.
5. **Offer** to run a DNA audit to identify divergences between code and the new DNA.

## Mode 5: Creating RNA from DNA

### When to use
DNA is ready, RNA / Harness is needed for a specific stack and agent.

### Process

1. **Read DNA.md.**
2. **Determine the stack:** language, DB, agent, CI.
3. **For each DNA invariant** formulate:
   - A specific check in terms of the current stack
   - A test or CI rule
   - A rule for CLAUDE.md / AGENTS.md
4. **Generate** RNA.md / Harness.md.

## Key Rules

- DNA **never** contains names of technologies, models, or frameworks
- DNA is **always** compact (2–5 pages)
- DNA is updated **only** by the project owner; the agent proposes — does not commit
- On conflict between a task and DNA — the agent **reports**, does not silently violate
- Quality test: "remove all technologies — does it still make sense?"
- The agent's role in DNA creation is **crystallization**, not formalization. Help discover the implicit, don't just record the explicit

## Additional Resources

For the complete DNA/RNA methodology with philosophy, anti-patterns, lifecycle, and roles, see [references/methodology-en.md](../../references/methodology-en.md).

Original methodology in Russian: [references/methodology-ru.md](../../references/methodology-ru.md).
