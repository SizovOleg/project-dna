# RNA: SciProof — Python/PostgreSQL/Claude Code

> This is a real-world example showing how DNA invariants translate into stack-specific enforcement rules. Each rule references the DNA invariant it implements.

**Stack:** Python 3.12, PostgreSQL 16, Claude Code, GitHub Actions CI
**DNA Version:** 2.1 | **RNA Version:** 1.3 | **Date:** 2026-03-17

---

## Ontology Enforcement

### Fact ≠ Claim (DNA: Ontology / Core Distinctions)

```
RULE: Models `Fact` and `Claim` are separate Python classes 
      and separate PostgreSQL tables.
      
TEST: test_fact_claim_separation()
  - Assert `facts` table exists
  - Assert `claims` table exists  
  - Assert `claims.fact_id` FK to `facts.id`
  - Assert no columns mixing fact data with claim data

CI: Schema migration lint — reject any migration that 
    merges facts and claims tables.
    
CLAUDE.md: "Never combine facts and claims into a single 
    model or table, even for 'simplification'."
```

### Roundness ≠ Circularity (DNA: Ontology / Core Distinctions)

```
RULE: `roundness` and `circularity` are separate columns 
      with separate computation pipelines.

TEST: test_morphometric_separation()
  - Assert both columns exist in grain_measurements
  - Assert different computation functions
  - Assert values are not derived from each other

CLAUDE.md: "Roundness and Circularity are strictly different 
    morphometric parameters. Never alias, merge, or derive 
    one from the other."
```

---

## Deontology Enforcement

### Originals Immutable (DNA: Deontology)

```
RULE: Table `originals` has no UPDATE/DELETE triggers. 
      Application layer rejects mutations.

SQL:
  CREATE OR REPLACE FUNCTION prevent_original_mutation()
  RETURNS TRIGGER AS $$
  BEGIN
    RAISE EXCEPTION 'Originals are immutable (DNA invariant)';
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER originals_immutable
  BEFORE UPDATE OR DELETE ON originals
  FOR EACH ROW EXECUTE FUNCTION prevent_original_mutation();

TEST: test_originals_immutability()
  - Insert original → success
  - Attempt UPDATE → expect exception
  - Attempt DELETE → expect exception

CI: SQL lint — flag any raw UPDATE/DELETE on originals table.
```

### Evidence Linkage (DNA: Deontology)

```
RULE: `source_ref` column is NOT NULL in all claim-bearing tables.

SQL: 
  ALTER TABLE claims 
  ADD CONSTRAINT claims_source_ref_required 
  CHECK (source_ref IS NOT NULL AND source_ref != '');

TEST: test_evidence_linkage()
  - SELECT count(*) FROM claims WHERE source_ref IS NULL = 0
  - Attempt INSERT without source_ref → expect constraint violation

CI: Weekly check — 
  SELECT count(*) FROM claims WHERE source_ref IS NULL;
  Assert = 0.
```

### Atomic Well Descriptions (DNA: Deontology)

```
RULE: Text chunking respects geological unit boundaries.
      Boundary markers: "Скв." (well), "Обн." (outcrop).

CODE:
  BOUNDARY_MARKERS = [r'Скв\.', r'Обн\.', r'Разрез']
  
  def chunk_text(text, markers=BOUNDARY_MARKERS):
      # Split only at boundaries, never within descriptions
      ...

TEST: test_atomic_chunking()
  - No chunk starts mid-description (regex check)
  - Every chunk either starts at document beginning 
    or at a boundary marker
  - Round-trip: join(chunks) == original_text

CLAUDE.md: "When implementing text splitting, geological 
    descriptions of wells (Скв.) and outcrops (Обн.) are 
    atomic units. Never split within them."
```

### Training Samples (DNA: Deontology)

```
RULE: Training samples stored with redundancy. 
      Never in /tmp or ephemeral storage.

CODE:
  TRAINING_DATA_PATH = Path("data/training/")  # Version-controlled
  
  assert not str(TRAINING_DATA_PATH).startswith("/tmp")
  assert not str(TRAINING_DATA_PATH).startswith("/var/tmp")

TEST: test_training_data_persistence()
  - Assert training data path is under version control
  - Assert backup mechanism exists
  - Assert deletion requires explicit confirmation

CI: Pre-commit hook — reject commits that modify 
    data/training/ without explicit flag.
```

---

## Axiology Enforcement

### Completeness > Speed (DNA: Axiology)

```
RULE: Processing timeouts are generous. No premature truncation.

CONFIG:
  PROCESSING_TIMEOUT = 60  # seconds, not 5
  MAX_RETRIES = 3
  
  # No LIMIT without justification
  # Every SQL query with LIMIT must have a comment explaining why

TEST: test_completeness_priority()
  - Assert PROCESSING_TIMEOUT >= 30
  - Grep codebase for LIMIT clauses without comments → flag

CI: Query lint — LIMIT without comment = warning.

CLAUDE.md: "Never add LIMIT to queries without an explicit 
    comment explaining why truncation is acceptable. 
    Completeness is more important than speed."
```

### Review Speed (DNA: Axiology)

```
RULE: Expert review UI renders in < 2 seconds per grain.

TEST: test_review_performance()
  - Load grain review page
  - Measure render time
  - Assert < 2000ms for 95th percentile

CI: Performance regression test on each PR.
```

---

## Praxeology Enforcement

### Derived Layers Regenerable (DNA: Praxeology)

```
RULE: All derived data has a regeneration script.

CODE:
  # Every derived table/index/cache has:
  # 1. A clear source dependency
  # 2. A regeneration command
  # 3. A staleness check

  DERIVED_LAYERS = {
      "fact_index": {
          "source": "facts",
          "regenerate": "python manage.py rebuild_fact_index",
          "staleness_check": "SELECT max(updated_at) FROM facts > index_built_at"
      },
      ...
  }

TEST: test_regenerability()
  - For each derived layer: delete → regenerate → compare → match

CLAUDE.md: "Every derived artifact (index, cache, summary) 
    must have a documented regeneration path. If you create 
    a derived layer, add it to DERIVED_LAYERS registry."
```

### Simplicity (DNA: Praxeology)

```
CLAUDE.md: "If a simpler solution satisfies the DNA invariants, 
    prefer it. Do not add architectural complexity unless an 
    invariant requires it. Ask: 'Which DNA invariant requires 
    this complexity?' If none — simplify."
```

---

## CLAUDE.md Rules (aggregated)

```markdown
# CLAUDE.md — DNA-derived rules

## Invariants (from DNA — never violate)
- Facts and Claims are separate entities, separate tables, separate models
- Roundness ≠ Circularity — never alias or merge
- Originals are immutable — no UPDATE, no DELETE
- Every claim has source_ref — no unlinked assertions
- Never split text within well/outcrop descriptions
- Training data is a permanent asset — never in temp storage

## Priorities (from DNA Axiology)
- Completeness over speed — generous timeouts, no premature truncation
- No LIMIT without justification comment
- Review UI < 2 sec per grain

## Principles (from DNA Praxeology)
- Every derived layer must be regenerable
- Simplicity over complexity — justify with DNA invariant
- Infrastructure is temporary, knowledge is permanent
```
