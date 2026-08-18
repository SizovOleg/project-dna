# RNA: SciProof — Python/PostgreSQL/Claude Code

> Companion to [example-dna.md](example-dna.md). Shows how DNA invariants translate into stack-specific enforcement. **Every rule below derives from a violation indicator** — that's what makes the translation mechanical rather than interpretive.

**Stack:** Python 3.12, PostgreSQL 16, Claude Code, GitHub Actions
**DNA Version:** 3.0 | **RNA Version:** 2.0 | **Date:** 2026-08-18

---

## How this file is derived

The violation indicator in DNA *is* the check specification. An invariant without one is untranslatable into RNA — which is why the skill demands it at DNA creation time.

```
DNA invariant
  └─ Violation indicator  ──►  RNA check (stack-specific)
                               ├─ Test
                               ├─ CI rule
                               └─ CLAUDE.md rule
```

---

## Ontology Enforcement

### Fact ≠ Claim — DNA §2.2

**Violation indicator:** One table or record holds both facts and claims.

```
RULE: Models `Fact` and `Claim` are separate classes, separate tables.

TEST: test_fact_claim_separation()
  - Assert `facts` and `claims` tables both exist
  - Assert `claims.fact_id` FK references `facts.id`
  - Assert no column in either table holds the other's payload

CI: Schema migration lint — reject any migration merging the two tables.

CLAUDE.md: "Never combine facts and claims into a single model or
    table, even for 'simplification'."
```

### Roundness ≠ Circularity — DNA §2.2

**Violation indicator:** One column holds values of both parameters, or one is computed from the other.

```
RULE: Separate columns, separate computation pipelines.

TEST: test_morphometric_separation()
  - Assert both columns exist in grain_measurements
  - Assert distinct computation functions
  - Assert neither value is derivable from the other
    (property test: vary one, assert the other is unchanged)

CLAUDE.md: "Roundness and Circularity are strictly different
    morphometric parameters. Never alias, merge, or derive one
    from the other."
```

---

## Deontology Enforcement

### Originals immutable — DNA §3.1

**Violation indicator:** An UPDATE or DELETE path to the originals store exists and is reachable from application code.

```sql
CREATE OR REPLACE FUNCTION prevent_original_mutation()
RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'Originals are immutable (DNA §3.1)';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER originals_immutable
BEFORE UPDATE OR DELETE ON originals
FOR EACH ROW EXECUTE FUNCTION prevent_original_mutation();
```

```
TEST: test_originals_immutability()
  - Insert original → success
  - Attempt UPDATE → expect exception
  - Attempt DELETE → expect exception

CI: SQL lint — flag any raw UPDATE/DELETE targeting originals.
```

### Measurement ≠ Interpretation — DNA §3.2

**Violation indicator:** A single record or column holds both measured and interpreted values.

```
RULE: `measurements` and `interpretations` are separate tables.
      Interpretation rows carry `derived_from_measurement_id`.

TEST: test_measurement_interpretation_split()
  - Assert separate tables
  - Assert every interpretation row has a non-null source measurement
  - Assert no measurement column accepts free-text interpretation

CI: Column-name lint — reject columns matching /interpret|conclusion/
    on the measurements table.
```

### Evidence linkage — DNA §3.3

**Violation indicator:** An output artifact contains a record with a non-empty value and an empty provenance field.

```sql
ALTER TABLE claims
ADD CONSTRAINT claims_source_ref_required
CHECK (source_ref IS NOT NULL AND source_ref != '');
```

```
TEST: test_evidence_linkage()
  - SELECT count(*) FROM claims WHERE source_ref IS NULL → 0
  - Attempt INSERT without source_ref → expect constraint violation
  - Export a sample artifact, assert no row has value-without-provenance

CI: Weekly — SELECT count(*) FROM claims WHERE source_ref IS NULL;
    assert = 0.
```

### Atomic unit descriptions — DNA §3.4

**Violation indicator:** A chunk begins mid-description — first line lacks a unit header and the preceding chunk ends without a terminator.

```python
BOUNDARY_MARKERS = [r'Скв\.', r'Обн\.', r'Разрез']

def chunk_text(text: str, markers: list[str] = BOUNDARY_MARKERS) -> list[str]:
    """Разбивает текст только по границам геологических единиц."""
    ...
```

```
TEST: test_atomic_chunking()
  - Every chunk starts at document start or at a boundary marker
  - Round-trip: "".join(chunks) == original_text
  - Regression case: 1974 report with nested well descriptions

CLAUDE.md: "Geological descriptions of wells (Скв.) and outcrops
    (Обн.) are atomic units. Never split within them."
```

### Training samples permanent — DNA §3.5

**Violation indicator:** Training data path resolves under a temp directory, lacks backup, or is deletable without confirmation.

```python
TRAINING_DATA_PATH = Path("data/training/")  # version-controlled

assert not TRAINING_DATA_PATH.is_relative_to(Path(tempfile.gettempdir()))
```

```
TEST: test_training_data_persistence()
  - Assert path is under version control
  - Assert backup mechanism configured
  - Assert deletion requires explicit --confirm flag

CI: Pre-commit hook — reject commits modifying data/training/
    without an explicit flag.
```

---

## Axiology Enforcement — resolved dilemmas

Each dilemma from DNA §4.2 becomes a rule of choice the agent can actually apply.

### Completeness over speed

```
RULE: Generous timeouts; no premature truncation.

CONFIG: PROCESSING_TIMEOUT = 60  # seconds, not 5

TEST: test_completeness_priority()
  - Assert PROCESSING_TIMEOUT >= 30
  - Grep for LIMIT clauses lacking an adjacent justification comment

CI: Query lint — LIMIT without comment = warning.

CLAUDE.md: "Never add LIMIT without a comment explaining why
    truncation is acceptable here. Completeness beats speed."
```

### Responsiveness in review UI

```
TEST: test_review_performance()
  - Load grain review page, measure render time
  - Assert < 2000ms at 95th percentile

CI: Performance regression test on every PR touching the review UI.
```

---

## Negative Invariants — DNA §6

These become **prohibitions**, not checks. Where possible they're lint rules; where not, they're CLAUDE.md rules with rationale, so the agent knows a proposal to add them requires DNA mutation.

```
FORBIDDEN: ORM abstraction over the query layer (DNA §6.3)
  LINT: reject imports of sqlalchemy.orm, django.db.models
  CLAUDE.md: "Queries encode domain logic that must stay readable
      to a reviewing geologist. Raw SQL with named queries only.
      Proposing an ORM requires DNA mutation (Mode 4)."

FORBIDDEN: Silent schema migration on startup (DNA §6.3)
  LINT: reject migration calls from application entrypoints
  CLAUDE.md: "Schema changes are reviewed events. Never auto-migrate
      on boot."

FORBIDDEN: Automatic interpretation of results (DNA §6.1)
  CLAUDE.md: "The system extracts and organizes; it does not conclude.
      Do not add features that generate interpretations, summaries of
      meaning, or 'likely conclusions' alongside extracted facts."

FORBIDDEN: Cross-publication synthesis (DNA §6.1)
  CLAUDE.md: "Never merge claims from different authors into a
      consensus view. Disagreement is signal."
```

---

## ANCHORS.md — generated from DNA §7

> Not a source of truth for code — a **tripwire for self-checking**. The agent compares its output against these before reporting. A breach produces `[FAILED ANCHOR]` in the report, never silent continuation. See `architect-cc-workflow` §14.1.

### Structural invariants (asserted in code)

```
grain_size_um ∈ (0, 2000]
roundness ∈ [0, 1]
circularity ∈ [0, 1]
roundness and circularity are independent — neither derived from the other
publication_year ∈ [1850, current_year]
depth values within one well description increase monotonically
a measurement has exactly one source_ref
```

### Reference canaries (checked when the object is processed)

```
Publication #0001 (Sidorov 1974) — 47 facts, 112 claims, 3 wells
Grain sample TS-0042 — roundness 0.61, circularity 0.83
Well "Скв. 15-бис" — 23 depth intervals, 4.2–187.6 m
```

If a canary drifts, the pipeline is broken — not the data.

---

## CLAUDE.md rules (aggregated)

```markdown
# CLAUDE.md — DNA-derived rules

## Invariants — never violate (DNA §3, §6)
- Facts and Claims: separate entities, tables, models
- Measurement and Interpretation: separate storage
- Roundness ≠ Circularity — never alias or derive
- Originals immutable — no UPDATE, no DELETE
- Every claim has source_ref — no unlinked assertions
- Never split text within well/outcrop descriptions
- Training data is permanent — never in temp storage

## Never build (DNA §6)
- Automatic interpretation of results
- Cross-publication consensus synthesis
- ORM over the query layer
- Auto-migration on startup

## Priorities (DNA §4.2 — resolved dilemmas)
- Completeness over speed: generous timeouts, no LIMIT without comment
- Accuracy over volume: attribution correctness first
- Provenance over model simplicity
- Review UI responsiveness: < 2 sec per item

## Numeric self-check
Before reporting any numeric result, verify against ANCHORS.md.
A breach reports as [FAILED ANCHOR] — never silently ignored.
All arithmetic through code execution, never through reasoning.
```
