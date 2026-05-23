# DNA: SciProof

> This is a real-world example extracted from the SciProof project — a scientific verification platform for geomorphological and paleogeographical publications. Comments in `<!-- -->` explain the reasoning behind each section.

**Version:** 2.1 | **Date:** 2026-03-17

---

## Mission

<!-- One or two sentences. No technologies. -->

Automated extraction, verification, and systematization of factual claims from scientific publications on geomorphology and paleogeography. The system replaces manual literature review, not the scientific judgment.

---

## Ontology

<!-- What entities exist in the domain and how they relate. The expert reads this and says: "Yes, the world is structured this way." -->

### Core Distinctions

**Fact ≠ Claim.** A Fact is an observed measurement or phenomenon recorded in a publication. A Claim is an interpretation or conclusion drawn from facts. One fact can have multiple contradictory claims from different authors. Conflating them loses the ability to trace scientific disagreements.

**Measurement ≠ Calibration ≠ Interpretation.** Three distinct operations. A grain size measurement (0.25 mm) is not the same as its calibration against a standard, which is not the same as the interpretation ("fine sand indicates low-energy depositional environment").

**Roundness ≠ Circularity.** Two different morphometric parameters. Roundness measures smoothness of edges. Circularity measures how close the shape is to a circle. Confusing them produces incorrect sedimentological conclusions.

**Term ≠ Concept.** The same term can have different meanings across scientific schools. "Loess" in Russian and Western geomorphology refers to overlapping but non-identical categories. The system must track terms-in-context, not bare terms.

### Typologies

- Publications: monograph, article, dissertation, report, map description
- Facts: measured, observed, calculated, inferred
- Sources: primary (original publication) vs. secondary (citing another)

---

## Deontology

<!-- What is permitted and what is forbidden. Not structure of the world, but rules of working with it. -->

**Originals are immutable.** Source text, once ingested, cannot be modified. All transformations produce derived artifacts. Loss of original = loss of traceability.

**No assertion enters the system without evidence linkage.** Every claim must trace back to a specific page, paragraph, or figure in the source publication. Unlinked claims are noise.

**Never split within well/outcrop descriptions.** When chunking text for processing, geological descriptions of individual wells and outcrops are atomic units. Splitting them produces incoherent fragments that mislead analysis.

**Training samples are permanent assets.** Expert-annotated samples are expensive (hours of geologist time per sample). Loss is catastrophic and irreversible. They are never in temporary storage.

---

## Axiology

<!-- What is valuable and what is not. Priorities. -->

**Completeness over speed.** Missing a relevant publication is worse than slow processing. Deep analysis of hundreds of documents, not surface indexing of millions.

**Distillation quality over throughput.** One correctly extracted fact with proper attribution is worth more than a hundred unverified claims.

**Traceability over convenience.** Every step from source to conclusion must be reconstructable. If the user asks "where did this come from?" — the answer must be immediate and specific.

**Review speed threshold: 2 sec/grain.** If the expert review interface takes longer than 2 seconds per grain to render and interact with, the UI is broken, not the expert.

---

## Praxeology

<!-- How to act. Not description of the world, not prohibitions, but principles of action. -->

**Triage is built into the process.** Not all publications are equal. The system prioritizes by relevance before deep processing.

**Derived layers are regenerable.** Indexes, summaries, cached views — all can be rebuilt from source data. Design them for regeneration, not permanence.

**Infrastructure is temporary, knowledge is permanent.** The database engine can change. The hosting can change. The processing pipeline can change. The domain model and training samples must survive all of these.

**Simplicity over architectural perfection.** If a simpler solution works and satisfies invariants, prefer it. Architectural elegance is not a goal — correctness and maintainability are.

---

## Domain Specifics

<!-- Knowledge that doesn't fit other sections but is essential for correct implementation. -->

- Russian-language publications dominate the field. OCR quality for Russian geological texts is a critical bottleneck.
- Geological terminology has regional variants (Soviet/Russian school vs. Western nomenclature).
- Coordinate systems: publications may use historical coordinate systems. Transformation to modern systems requires metadata about the source CRS.
- Scale matters: thin section analysis (micrometers) vs. outcrop description (meters) vs. regional mapping (kilometers) — different analytical approaches at each scale.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-15 | Initial DNA from SciProof project start |
| 2.0 | 2026-02-20 | Added Roundness ≠ Circularity distinction, review speed threshold |
| 2.1 | 2026-03-17 | Philosophical framework alignment, Term ≠ Concept added |
