# DNA/RNA: Development Methodology with AI Agents
## Separating Domain Knowledge from Technical Implementation

**Version:** 2.0
**Date:** 2026-03-17
**Origin:** Derived empirically during SciProof development (2025–2026)

---

## Manifesto

Code is an intermediate representation between human intent and machine execution. With the advent of LLMs capable of understanding intent directly, code becomes a transitional artifact — like assembly became invisible behind C. What disappears is not computation, but human-readable code as an intermediary between intent and computation.

But intent, constraints, and quality criteria do not disappear. They are the true product of development. A human with domain expertise and systems thinking is the only irreplaceable element. They carry in their head the domain model, reality constraints, quality criteria, and purpose.

The DNA/RNA methodology separates **what the system must do and why** (the immutable core) from **how it is implemented under specific conditions** (the adaptive harness). The former belongs to the human expert. The latter — to the agent and environment.

---

## The Biological Metaphor

**DNA** — the genetic code of the system. Contains the domain model, invariants, constraints, and quality criteria. Independent of technologies, models, or frameworks. Written for humans. The same DNA can spawn different implementations (web platform, CLI, bot, plugin) — all of the same "species".

**RNA (Harness)** — expression of DNA for specific conditions. Translates domain invariants into agent rules, linters, CI checks, code patterns. Tied to a specific stack, agent, and environment. Changes when conditions change — DNA stays the same.

**DNA Mutation** — a revision of fundamental domain understanding. A rare event, initiated only by the domain expert.

**RNA Adaptation** — changing the stack, model, agent, or infrastructure. A routine event. Same species, different habitat.

---

## Philosophical Framework of DNA

DNA is not just ontology. Ontology describes "what exists". DNA is broader by three layers:

### Formula

```
DNA = Ontology (what exists and how it's connected)
    + Deontology (what is permitted and what is forbidden)
    + Axiology (what is valuable and what is not)
    + Praxeology (how to act in this world)
```

### Four Layers

**Ontology** — the core. What entities exist in the domain, how they're related, what categories are valid. A domain expert reads it and says: "yes, the world is structured this way."

Examples: Fact ≠ Claim. Measurement ≠ Calibration ≠ Interpretation. Term ≠ Concept (same term — different meanings in different schools).

**Deontology** — what is permitted and what is forbidden. Constraints dictated not by the structure of the world, but by practice of working within it.

Examples: Originals are immutable. Without a link to evidence, an assertion does not enter the system. Do not split within borehole descriptions.

**Axiology** — what is valuable and what is not. Ontology does not evaluate. DNA evaluates, because the system is built for a specific purpose.

Examples: Completeness over speed. Distillation quality over throughput. Deep analysis of hundreds of documents, not shallow indexing of millions.

**Praxeology** — how to act. Not a description of the world nor prohibitions, but principles of action.

Examples: Triage is built into the process. Derived layers are regenerable. Infrastructure is temporary, knowledge is permanent. Simplicity over architectural perfection.

### Why Not Formal Ontology

DNA is a natural language document, not an OWL file or RDF graph. Deontology, axiology, and praxeology can be formalized into machine ontology, but there's no need. The audience is a human (for review) and an LLM (for context understanding). Both read natural language better than OWL.

### LLM as a Thinking Amplifier: Formalization Through Dialogue

The traditional approach to formalizing intent is external: a person forces their thoughts into a formal language (DSL, UML, specification). This works but creates additional cognitive load — the "free energy" of translation from natural language to formalism.

LLM does the opposite — crystallization from within. Chaos in the expert's mind is high free energy: many possible states, uncertainty, contradictions, implicit assumptions. Dialogue with an LLM is a crystallization process: from a cloud of possibilities, a stable structure precipitates.

DNA is the result of this crystallization. Not a formalism for machines, but a precise record of the domain expert's knowledge after going through a process of clarification.

---

## DNA vs Requirements

DNA says **why the world is structured this way**. Requirements say **what the system must do in this world**.

DNA: "Fact ≠ Claim, because different authors draw different conclusions from the same measurements."
Requirements: "The system allows browsing all claims for a given fact, filtering by author and year."

**Separation test:** if a statement holds for any interface (web, CLI, bot, API) — it's DNA. If it describes specific behavior — it's Requirements.

---

## Documentation Architecture

```
DNA.md — invariants, for humans
  ↓ translates into
RNA / Harness.md — enforcement, for the agent
  ├── CLAUDE.md / AGENTS.md (contract with a specific agent)
  ├── Skills (codified experience)
  └── Plugins / MCP (agent tooling)
  ↓ concretized into
Requirements — what the system does
  ↓
TechnicalDesign — how it's implemented
  ↓
DevPrompts — instructions to the agent per step
  ↓
Code + Tests ←── DNA audit (feedback to DNA)
  ↓
Development Log — what was done, what decisions were made
```

### Stability Scale

| Layer | Lifespan | Who changes it |
|-------|----------|----------------|
| DNA | Years | Expert |
| RNA / Harness | Months | Expert |
| Skills | Months | Both |
| Requirements | Months | Both |
| TechnicalDesign | Weeks | Agent |
| DevPrompts | One-time | Both |
| Code | Days | Agent |

---

## DNA Audit — The Third Quality Control Loop

### Three Loops

1. **Unit tests** — does the code work?
2. **Integration tests** — do the components work together?
3. **DNA audit** — was the right code written in the first place?

### What It Checks

For each DNA section:
- **Compliance** — is the decision implemented?
- **Violations** — are there contradictions?
- **Gaps** — what's in DNA but not in code?
- **Divergences** — what's in code but not documented in DNA?

---

## Lifecycle

### Project Creation

1. Domain expert formulates DNA (2–5 pages)
2. DNA is reviewed by a domain peer
3. RNA is derived from DNA for the specific stack/agent
4. From DNA + RNA — Requirements → TechnicalDesign → DevPrompts
5. Agent begins work with DNA + RNA as context

### Stack / Agent Change

DNA stays → RNA is rewritten → TechnicalDesign is rewritten → DevPrompts from scratch → DNA audit

### DNA Mutation

Expert realizes a change → DNA is updated with justification → RNA is updated → DNA audit identifies divergences → tasks to bring code into compliance

---

## Roles

**Domain Expert (DNA owner)** — formulates invariants, criteria, model. Not required to write code. The only one who can mutate DNA.

**AI Agent (executor)** — reads DNA as invariants, RNA as rules. Translates into implementation. Does not silently violate DNA. May propose mutations.

**CI / Automation (enforcement)** — checks RNA compliance (and through RNA — DNA). Runs DNA audits.

---

## Anti-patterns

**DNA drift** — invariants are outdated, code lives its own life. Treatment: regular DNA audits.

**DNA bloat** — implementation leaked into DNA, 10+ pages. Treatment: "remove all technologies — does it still make sense?" test.

**Phantom DNA** — DNA exists only in someone's head, never written down. The agent makes arbitrary decisions. Treatment: write it down.

**RNA without DNA** — CLAUDE.md exists but there's no root. When switching agents — start from scratch. Treatment: extract DNA.

**Overspecification** — DNA dictates implementation. The agent cannot optimize. Treatment: "what" and "why", not "how".

---

## Applicability

### Works well

- Solo developer + AI agent
- Domain expert (non-programmer) + AI agent
- Small team with a shared domain
- Long-lifecycle projects

### Does not work

- Projects without domain complexity (generic CRUD — ADR is sufficient)
- Projects where implementation IS the domain (compiler, game engine — DNA and RNA merge)

---

## Versioning

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-16 | Initial formalization |
| 2.0 | 2026-03-17 | Added philosophical framework, DNA vs Requirements, role of skills and plugins |
| 2.1 | 2026-03-17 | LLM as thinking amplifier, DNA as attractor |

---

## Acknowledgments

This methodology was derived from the practice of developing SciProof — a scientific verification platform for geomorphological and paleogeographical publications. Key ideas were formulated in dialogue between a domain expert and an AI assistant, drawing from CodeSpeak (Andrey Breslav), Harness Engineering (OpenAI), and Spec-Driven Development. The biological DNA/RNA metaphor was proposed by the domain expert.
