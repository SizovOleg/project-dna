# DNA: SciProof

> Real-world example from the SciProof project — a scientific verification platform for geomorphological and paleogeographical publications. Comments in `<!-- -->` explain the reasoning behind each section.

**Version:** 3.0 | **Date:** 2026-08-18

---

## Purpose of This Document

Root project document. Contains decisions, constraints, and quality criteria independent of implementation. All other documents derive from DNA.

### Rules for the AI Agent

1. Read DNA before starting work.
2. Every decision must be compatible with the invariants.
3. On conflict — report it, don't violate silently.
4. DNA is updated only by the project owner.
5. Hypotheses live in `ASSUMPTIONS.md`, not here.

---

## Key Invariants (read first)

<!-- Duplicated at the end of the document. A rule sitting only in the middle
     of a long context is statistically ignored by the agent — this is attention
     architecture, not laziness. See architect-cc-workflow §5.3. -->

1. **Fact ≠ Claim.** One fact can carry multiple contradictory claims.
2. **Originals are immutable.** No UPDATE path may exist to source text.
3. **No assertion without evidence linkage.** Every claim traces to a specific page.
4. **Roundness ≠ Circularity.** Never aliased, never derived from one another.
5. **We do not interpret results automatically.** Interpretation is the geologist's job.

---

## 1. Mission

<!-- One or two sentences. No technologies. -->

Automated extraction, verification, and systematization of factual claims from scientific publications on geomorphology and paleogeography. The system replaces manual literature review, not scientific judgment.

---

## 2. Domain Model (ontology)

### 2.1. Entities

Publication, Fact, Claim, Author, Measurement, Source Reference, Training Sample.

### 2.2. Fundamental Distinctions

**Fact ≠ Claim.** A Fact is an observed measurement or phenomenon recorded in a publication. A Claim is an interpretation drawn from facts. One fact can have multiple contradictory claims from different authors. Conflating them loses the ability to trace scientific disagreement.

**Measurement ≠ Calibration ≠ Interpretation.** Three distinct operations. A grain size measurement (0.25 mm) is not its calibration against a standard, which is not the interpretation ("fine sand indicates low-energy depositional environment").

**Roundness ≠ Circularity.** Two different morphometric parameters. Roundness measures edge smoothness. Circularity measures how close the shape is to a circle. Confusing them produces incorrect sedimentological conclusions.

**Term ≠ Concept.** The same term carries different meanings across scientific schools. "Loess" in Russian and Western geomorphology refers to overlapping but non-identical categories. The system tracks terms-in-context, not bare terms.

### 2.3. Typologies

- Publications: monograph, article, dissertation, report, map description
- Facts: measured, observed, calculated, inferred
- Sources: primary (original publication) vs. secondary (citing another)

---

## 3. Constraints (deontology)

<!-- Each invariant carries a violation indicator. An invariant you cannot
     observably violate is a slogan, not an invariant. -->

### 3.1. Originals are immutable

**Statement:** Source text, once ingested, cannot be modified. All transformations produce derived artifacts.
**Rationale:** Loss of the original means loss of traceability. Precedent: two of the three analogous projects surveyed lost source fidelity through in-place "cleanup" and could not reconstruct provenance.
**Violation indicator:** An UPDATE or DELETE path to the originals store exists and is reachable from application code.

### 3.2. Measurement and interpretation are stored separately

**Statement:** A measured value and its interpretation never share a storage location or a model field.
**Rationale:** Once merged, the two cannot be untangled; downstream consumers cannot tell which values are observations and which are inferences.
**Violation indicator:** A single record or table column holds both measured values and interpreted values.

### 3.3. No assertion without evidence linkage

**Statement:** Every claim traces back to a specific page, paragraph, or figure in the source publication.
**Rationale:** Unlinked claims are noise — indistinguishable from fabrication at review time.
**Violation indicator:** An output artifact contains a record with a non-empty value and an empty provenance field.

### 3.4. Geological unit descriptions are atomic

**Statement:** When chunking text, descriptions of individual wells and outcrops are atomic units and are never split.
**Rationale:** Splitting produces incoherent fragments that mislead analysis — the depth sequence loses meaning without its header.
**Violation indicator:** A chunk begins mid-description — its first line lacks a unit header and the preceding chunk ends without a terminator.

### 3.5. Training samples are permanent assets

**Statement:** Expert-annotated samples are never held in temporary or regenerable storage.
**Rationale:** Each sample costs hours of geologist time. Loss is irreversible.
**Violation indicator:** The training data path resolves under a temp directory, or lacks a backup mechanism, or is deletable without explicit confirmation.

---

## 4. Quality Criteria (axiology)

### 4.1. What "works correctly" means

Extraction is correct when a domain expert reviewing a random sample of 20 extracted facts finds zero misattributions of source and zero conflations of fact with claim.

### 4.2. Resolved dilemmas

<!-- A list of values is not axiology — it's decoration. An agent cannot apply
     a list of good things; it can only apply a rule of choice. -->

- **When we cannot both process all documents and stay within a fast response budget → choose completeness**, because a missed publication costs more than a slow answer.
- **When we cannot both extract more facts and maintain attribution accuracy → choose accuracy**, because one correctly attributed fact is worth more than a hundred unverifiable claims.
- **When we cannot both preserve full provenance and simplify the data model → choose provenance**, because the model can be refactored and provenance cannot be reconstructed.
- **When the review interface cannot both show full context and stay responsive → choose responsiveness**, because an expert who stops reviewing produces no data at all.

---

## 5. Principles (praxeology)

### 5.1. Economic model

Deep analysis of hundreds of documents, not surface indexing of millions. Per-document processing cost may be high; corpus size is deliberately bounded.

### 5.2. Scale

Designed for a corpus of 10²–10⁴ publications, single-institution use, tens of concurrent reviewers.

### 5.3. Evolution

Triage is built into the process — the system prioritizes by relevance before deep processing. Derived layers (indexes, summaries, cached views) are designed for regeneration, not permanence. Infrastructure is temporary, knowledge is permanent.

---

## 6. Negative Invariants (what must never appear)

<!-- Most DNA documents record only the positive side. Without explicit negative
     invariants a project sprawls through accretion — each addition looks
     reasonable, and the sum destroys coherence. -->

### 6.1. Deliberately not built

- **Automatic interpretation of results.** The system extracts and organizes; it does not conclude. Interpretation is where the geologist's judgment is irreplaceable, and an automated guess presented alongside verified facts would contaminate the whole output.
- **Cross-publication synthesis.** The system does not merge claims from different authors into a single "consensus" view. Disagreement is signal, not noise to be averaged away.

### 6.2. Rejected approaches

- **Full-text search as the primary interface** — rejected twice. It returns passages, not facts, and pushes the extraction work back onto the user.
- **Crowd-sourced annotation** — rejected. Annotation quality depends on domain expertise that cannot be crowd-sourced in this field.

### 6.3. Forbidden patterns

- **ORM abstraction over the query layer.** Queries here encode domain logic that must remain readable to a reviewing geologist.
- **Silent schema migration on startup.** Schema changes are reviewed events, not side effects of deployment.

Any proposal to add something from this list requires formal DNA mutation (Mode 4), not silent addition.

---

## 7. Numeric Domain Invariants

<!-- These generate ANCHORS.md — the agent's self-check anchors.
     DNA says WHY a quantity is what it is; ANCHORS.md says WHAT it is. -->

- Grain size ∈ (0, 2000] μm — beyond this the object is not a grain in this domain's sense
- `roundness` ∈ [0, 1] and `circularity` ∈ [0, 1], independently — neither derived from the other
- Publication year ∈ [1850, current] — the field's literature does not predate systematic geological survey
- A measurement has exactly one source reference; a fact may have many claims
- Depth values in a well description increase monotonically — a decrease indicates a parsing error, not a geological feature

---

## 8. Pre-action Protocol

Before any change touching a DNA invariant, record in DEVLOG:

**Always:**
1. **What changes?** (one phrase)
2. **Why?** (concrete goal or problem, not "improvement in general")
3. **Which DNA invariant does this serve?** If none — STOP: either update DNA (Mode 4) or cancel the change.

**On triggers:**
4. Persistent state or irreversible operation (DB, filesystem, deploy, release) → **How to roll back?**
5. Handoff or publication → **Who maintains it and how?**
6. Diff > 100 lines OR > 3 modules touched → **Which components?**

---

## 9. Domain Specifics

- Russian-language publications dominate the field. OCR quality for Russian geological texts is a critical bottleneck.
- Geological terminology has regional variants (Soviet/Russian school vs. Western nomenclature).
- Publications may use historical coordinate systems; transformation requires metadata about the source CRS.
- Scale matters: thin section analysis (micrometers) vs. outcrop description (meters) vs. regional mapping (kilometers) — different analytical approaches at each scale.

---

## 10. Typical Scenarios

- "Which publications report grain roundness measurements for aeolian deposits in Western Siberia?"
- "Show all claims derived from this specific measurement, grouped by author and year."
- "Where do these two authors disagree about the same outcrop?"

---

## Key Invariants (repeated for the agent)

<!-- Deliberate duplication of the block at the top. -->

1. **Fact ≠ Claim.** One fact can carry multiple contradictory claims.
2. **Originals are immutable.** No UPDATE path may exist to source text.
3. **No assertion without evidence linkage.** Every claim traces to a specific page.
4. **Roundness ≠ Circularity.** Never aliased, never derived from one another.
5. **We do not interpret results automatically.** Interpretation is the geologist's job.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-15 | Initial DNA at project start |
| 2.0 | 2026-02-20 | Added Roundness ≠ Circularity distinction |
| 2.1 | 2026-03-17 | Philosophical framework alignment, Term ≠ Concept added |
| 3.0 | 2026-08-18 | Violation indicators for every invariant; negative invariants (§6); numeric invariants (§7); pre-action protocol (§8); key invariants duplicated for agent placement; hypotheses moved to `ASSUMPTIONS.md` |
