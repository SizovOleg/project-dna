# Enforcement: what separates a rule from an intention

[RU version](enforcement-ru.md)

A skill without external checks is a set of beliefs about what works. This layer
answers the question "how do we know the rule is being followed" — and answers it
with numbers rather than confidence.

## The ladder

A rung is determined by **how external the check is**, not by how the rule is
worded. Writing FORBIDDEN in the text does not raise the rung.

| Rung | Mechanism | What it is |
|---|---|---|
| 1 | Text in the skill | Intention |
| 2 | + placement at start and end | Intention with better odds |
| 3 | + observable trace in an artifact | Observable compliance |
| 4 | + regression test with a k/n threshold | Measured compliance |
| 5 | + an external check that fails | Specification |
| 6 | + architectural impossibility | Hard constraint |

A specification begins at rung 5. Everything below is intention with varying
quality of evidence. Two categories live off the ladder: `[heuristic]` — a rule
that has no violation indicator and never will, and `[architect discipline]` — a
rule for the human that no agent can enforce. Both are fine when labelled; the
error is not having such rules, it is counting them as specification.

Honest per-rule maps:
[project-dna](../skills/project-dna/ENFORCEMENT_MAP.md) ·
[architect-cc-workflow](../skills/architect-cc-workflow/ENFORCEMENT_MAP.md)

## Why rules about artifacts cost less than rules about process

`project-dna` has the better profile: eight rules already sit at rung 5, because
what gets checked is a static file. Files can be linted; behaviour can only be
measured. The practical consequence: **word new rules in terms of artifacts from
the start.** "Every invariant carries a violation indicator" is checkable by grep;
"the agent acts prudently" is checkable by nothing.

## Lints

| Script | Checks | Raises |
|---|---|---|
| [`dna_lint.py`](../skills/project-dna/harness/dna_lint.py) | DNA structure: technology names, length, violation indicators, negative and numeric invariants, the trailing key-invariant block | DNA rules to 5 |
| [`report_lint.py`](../skills/architect-cc-workflow/harness/report_lint.py) | Phase-end report: required sections, banned self-certification phrases, presence of confidence markers, signal counters | §11, §12, §15.2 |
| [`signal_lint.py`](../skills/architect-cc-workflow/harness/signal_lint.py) | Signal log: chronological order, no events after BLOCK, silence budget, report counters matching the log | §15.1, §15.2, §15.3 |

All three are dependency-free. Run as `python3 <script> <file>`; exit 0 is PASS,
exit 1 is FAIL.

### Pre-commit

```bash
sh skills/project-dna/harness/install-hook.sh /path/to/repo
```

The hook fires only when a DNA file is part of the commit and leaves ordinary
commits alone. It installs entirely inside `.git/hooks/`, so tracked repository
content is untouched, and an existing foreign hook is chained rather than
overwritten.

**Warning mode by default, not blocking.** This is not timidity but a conclusion
from measurement: DNA files written before violation indicators existed do not
pass the lint at all, and a blocking hook would halt work across every project at
once. Enable blocking per project once its DNA has been migrated:

```bash
git config dnalint.blocking true
```

Repositories using the `pre-commit` framework are left alone — there
`.git/hooks/pre-commit` is generated. The installer prints a ready snippet for
`.pre-commit-config.yaml` instead.

## Communicating during the work, not after it

A signal delivered in the final message is not a signal, it is an autopsy. BLOCK
earns its keep by stopping things **before** the action. In headless execution
the final text is the only channel, so §15 without a separate one degenerates:
the agent finishes the job and only then reports that there was a BLOCK.

So signals go into an append-only log as they occur:

```
2026-08-18T11:04:12Z  START      DevPrompt_07
2026-08-18T11:06:48Z  HEARTBEAT  step 2/5, six files read
2026-08-18T11:09:31Z  NOTE       users table has no email column
2026-08-18T11:09:33Z  BLOCK      ALTER TABLE required, outside mandate
```

A line is written before the action it concerns. BLOCK is the last line before
the halt. `signal_lint` verifies this by timestamp rather than on trust, and
reconciles the Phase-end report's counters against the log — a report that
retells instead of reflecting gets caught.

## Regression suite

[REGRESSION_SUITE.md](../skills/architect-cc-workflow/REGRESSION_SUITE.md) holds
the behavioural tests and the baseline. Five principles, two of which are the
ones usually forgotten:

- **Completeness by construction.** Every anti-pattern has a test; changing the
  skill without adding one counts as an unfinished change.
- **Negative tests are mandatory.** Without them the suite rewards
  over-triggering: a skill that blocks everything passes every positive test. A
  mechanism that fires too often is as broken as one that never fires.

Running the smoke set:

```bash
sh skills/architect-cc-workflow/harness/run_smoke.sh
```

**From an ordinary terminal only.** Inside a Claude Code session the CLI refuses
to start a nested session; the script detects this and says so plainly.

## The baseline is a function of (skill, model)

Change the model and the whole baseline is void and must be re-run. Amend the
skill and it is void for the rules affected. The first measurement (2026-08-18,
Sonnet) demonstrated this literally: T-A-1 came out 2/3, the §3/§15 conflict was
resolved by adding §3.6, and the recount on the amended version gave 3/3 — both
figures stayed in the table with their versions, because overwriting a
measurement loses the record of what changed and why.

## What the measurement does not show

A passing test does not prove the skill caused the behaviour. For T-H-1 a control
with no skill and an empty `CLAUDE.md` produced the same 3/3 — the base model
behaves that way on its own, and the test measures it rather than the protocol.
The discriminance of the remaining tests has not been measured.

That is no reason to drop the test: it still catches a regression if the behaviour
ever degrades. It is a reason not to credit it to the skill.

## What the agent cannot do for the owner

Violation indicators were drafted by agents across eleven existing DNA documents.
All eleven passed the lint. All eleven failed adversarial verification: 29
fabricated indicators, 19 critical content losses.

The cause is not agent quality but the nature of the task. A violation indicator
is not a restatement of the invariant — it is a domain judgement about what is
observable in this particular world. Derived from text syntactically, the result
comes out grammatically sound and plausible while being disconnected from the
domain: an unconditional prohibition acquires an exception, a prescribed
procedure gets declared a violation, a checkable state is replaced by a claim
about what the analyst knew and when.

The lint catches a missing indicator. It does not catch a meaningless one and
never will — that row sits at rung 1 permanently. Details in
`skills/project-dna/ENFORCEMENT_MAP.md`, section on the mass migration.
