---
name: architect-cc-workflow
description: "Universal workflow protocol для пары architect (Claude.ai) + Claude Code в DNA/RNA проектах. Используй ВСЕГДА при: формулировании commands к Claude Code, написании DevPrompt'ов, ревью workflow между sessions, обнаружении систематических ошибок architect-side, планировании phase transitions. Триггеры: «напиши команду Claude Code», «напиши DevPrompt», «как мне дать задачу», «почему architect ошибается», «как валидировать решение», «что architect решает что Claude Code», «верификация спеков», «verification protocol», «error budget», «assumptions section», «boundaries Claude Code architect». Скилл кодифицирует уроки из Phase 1-2 sat-revisit-tool: ~10% architect error rate из-за LLM structural limits, защиты через verification + probe-first + assumption declaration + state refresh + hard iteration limits. НЕ для DNA creation (project-dna) или PRD writing (prd-coauthoring) или scientific methodology (research-with-ai)."
license: MIT
---

# Architect/Claude Code Workflow Protocol

Универсальный протокол взаимодействия между architect (Claude.ai в роли архитектора) и Claude Code (Claude в роли разработчика) для проектов, использующих DNA/RNA framework.

## Зачем нужен этот скилл

Architect (LLM) делает структурные ошибки при ~10% rate из-за:

1. **No persistent state** — каждое сообщение fresh context window, repo state reconstruct из памяти + prior conversation
2. **Pattern matching from training** — confidently generates plausible-but-wrong assertions from training precedents
3. **Confabulation risk** — claim знание литературы/кода без actual verification

Эти ошибки systematic, не accidental. Они **не исчезнут** через "будь внимательнее" — нужны structural defenses.

Скилл кодифицирует workflow protocol который catches errors **до execution**, минимизирует wasted sessions, четко разделяет responsibility между architect и Claude Code.

## Связанные скиллы (читай первыми если применимо)

- **`project-dna`** — создание DNA документа. **Этот workflow protocol активируется ПОСЛЕ создания DNA**, для execution phase. Project-dna — про "что" и "почему", architect-cc-workflow — про "как взаимодействовать при реализации".
- **`pipeline-development`** — техническая реализация pipeline сервисов. **Cross-reference**: architect-cc-workflow специфицирует workflow rules, pipeline-development специфицирует technical patterns. Используй вместе при разработке кода.
- **`research-with-ai`** — научная методология. Orthogonal — research-with-ai про epistemic discipline (что считать истиной), architect-cc-workflow про execution discipline (как достигать решений).

## Основные принципы

### 1. Decision boundaries (кто что решает)

**Architect (Claude.ai) decides — scientific/strategic:**
- Acceptance criteria thresholds + numeric values для научного claim
- Pre-registered protocol revisions (signed off by architect)
- Phase scope и task priorities
- Stop/pivot/proceed decisions при unexpected results
- GPT review verdict triage (substantive vs re-litigated)
- Publication-relevant claims

**Claude Code decides — implementation:**
- Module structure + boundaries (informed by existing codebase)
- LOC estimates calibrated против analogous existing modules
- Type signatures + pattern selection (informed by existing code)
- Edge case identification + handling vs deferral
- Test coverage strategy (target architect-set, cases CC-identified)
- Function/class naming conventions (consistent с existing codebase)
- Helper function placement decisions

**Antipattern:** architect specifies LOC estimates, type signatures, exact function names. Claude Code видит реальный код, делает это лучше.

**Antipattern:** Claude Code defers acceptance threshold к architect "knows better". Threshold — научное решение, architect owns. Implementation pattern — engineering, Claude Code owns.

### 2. Architect command format

Architect commands должны быть **goal-oriented**, не implementation-prescriptive:

```
Цель: [scientific objective]

Acceptance criteria: [thresholds, measurable]

Constraints (hard):
- [DNA invariants]
- [Pre-registered protocol]
- [scope boundaries]

Constraints (soft):
- [preferences, can override с rationale]

Assumptions (verify перед execute):
1. [infrastructure or capability assumed to exist]
2. [precondition assumed to hold]
3. [data/state assumed available]

Decision points для escalation:
- [conditions when к stop and ask]

Не specify:
- exact module boundaries (CC decides)
- exact LOC budget (CC estimates)
- specific function names (CC chooses)
- detailed test cases (CC identifies)
```

**Test:** если architect command может быть выполнен без opening repo — она too prescriptive (reverses к implementation territory).

### 3. Verification protocol (Claude Code → architect)

Перед executing любую architect-issued decision/spec/instruction, Claude Code обязан verify:

**3.1. Numeric constants verification**
- Check project knowledge / repo docs для cited source с page/section
- Если no project source: web search для literature confirmation
- Flag: ✅ verified / ⚠️ contradicts / ❓ unverifiable

**3.2. Architectural assumption verification**
- Check assumption против prior phase deliverables
- Check assumption against existing code patterns
- Flag potential conflicts с prior architecture

**3.3. Implementation feasibility check**
- LOC estimates: compare к analogous existing modules
- Dependencies: verify available или need addition
- Side effects: identify downstream consumers affected

**3.4. Improvement suggestions**
- Если architect's approach has known anti-patterns, suggest alternatives
- Если stronger pattern exists в codebase, reference it

**3.5. Return verification report BEFORE execution**

Format:
```
## Verification report — [command name]

### A. Numeric constants
| Value | Source | Status |
|---|---|---|
...

### B. Architectural assumptions
1. [assumption] — ✅/⚠️/❓ + rationale
...

### C. Implementation feasibility
| Task | Estimated LOC | Comparable | Realistic? |
...

### D. Suggested adjustments
1. [suggestion + rationale]

### Open questions for architect
1. [question requiring architect decision]

### Awaiting architect confirmation
```

Если architect command содержит no constants/assumptions to verify (routine: "run tests", "commit current state") → execute directly.

**4. Routine vs verifiable commands**

Verify | Don't verify
---|---
DevPrompt specs | "git status"
Plans (multi-step) | "run pytest"
Acceptance criteria | "commit current state"
Numeric constraints | "push к origin"
Architectural decisions | "show last commit message"
Pre-registered protocol | Trivial single-line edits

### 4. Architect explicit assumptions section

Каждый architect-issued command/spec должен содержать **"Assumptions (verify перед execute):"** section.

Format:
```
Assumptions:
1) [infrastructure or capability assumed to exist]
2) [precondition assumed to hold]
3) [data/state assumed available]
```

Если architect command не содержит assumptions section — Claude Code requests это перед execute.

Если any assumption verifies as false → STOP, escalate, не guess.

**Common antipattern caught:** architect issues "run benchmark" assuming runner exists; reality — runner needs к be built. Verification catches.

### 5. Periodic state refresh

Каждые 5 Claude Code sessions (или по architect request), Claude Code dumps:
- `git log --oneline -30`
- `find core/ tests/ -name "*.py" -type f | head -50`
- List of key types/classes (grep for `class ` / `dataclass`)
- Current dependencies summary

Output saved к `docs/state_refresh_YYYYMMDD.md`. Architect reads перед next major decision.

Counter увеличивается в `docs/Decisions.md` — track session count since last refresh.

**Зачем:** architect mental model decays. Refresh — cheap (~5 min Claude Code time) vs cost of architect errors based on stale state.

### 6. Error budget acknowledgment

Architect errors expected at ~10% rate из-за LLM structural limits. **Это accepted operational mode, не failure mode.**

Когда Claude Code identifies architect assumption gap — **НЕ defer к "architect knows better".** Escalate immediately per protocol. Claude Code — peer reviewer, не subordinate.

**Communication norm:** Claude Code не должен apologize за catching architect errors. Architect не должен быть defensive. Errors expected, defenses designed для catch.

### 7. Hard limits на GPT review iterations

Maximum 3 GPT review iterations per task. После 3rd:

- ALLOW (no HIGH/CRITICAL anywhere) → unblock, proceed
- ALLOW_WITH_FIXES (only MEDIUM/LOW residuals) → unblock, proceed
- BLOCK с only re-litigated findings (already addressed) → architect override, proceed
- BLOCK с new HIGH/CRITICAL → STOP, pivot к infrastructure-only closure
- ALLOW_WITH_FIXES с HIGH listed (severity downgrade) → treat as BLOCK
- BLOCK с only MEDIUM/LOW (no HIGH/CRITICAL) → unconventional, treat as ALLOW_WITH_FIXES
- Mixed severity ambiguous → conservative (highest severity wins)

**Зачем:** GPT review iterations имеют diminishing returns. Каждый round может introduce новые findings от prior fixes. Hard limit forces closure decision.

### 8. Probe-first protocol

Каждый new acceptance criterion / external dependency / data source требует **probe stage (DevPrompt_NN.0)** перед main implementation plan.

Probe deliverable: empirical evidence (concrete URL/SHA-256/output paste, не speculation). Probe report committed как research artefact. Architect uses probe results к finalize main plan.

Probe time-boxed (3-5 hours typical). Если probe surfaces blocker → STOP, escalate, не workaround.

**Зачем:** architect numerical constraints без empirical pre-flight verification — most common error source. Probe catches до plan finalization.

### 9. Pre-registration immutability

Pre-registered acceptance criteria committed к git BEFORE benchmark/experiment execution. Mid-run modifications forbidden (data dredging risk).

Revisions allowed но require:
1. Formal Decisions.md entry с rationale
2. Original criteria preserved в git history (immutable)
3. Revised criteria new commit
4. Architect explicit sign-off

### 10. Implementation autonomy

Перед major implementation work — Claude Code **proposes design** (modules, types, key functions). Architect approves **direction**, не details. Implementation proceeds autonomously after direction approval.

Tradeoff escalations при substantive decisions (architect call needed) — Claude Code stops, asks. Не guess.

## Когда применять

### При формулировании commands к Claude Code

Architect's checklist перед finalizing command:

- [ ] Goal явно сформулирован (что хотим достичь)
- [ ] Acceptance criteria measurable (что считать успехом)
- [ ] Hard constraints listed (DNA, pre-registered, scope)
- [ ] Soft constraints listed (preferences, можно override)
- [ ] Assumptions section explicit (что предполагаю существующим)
- [ ] Decision points для escalation specified
- [ ] Implementation details **NOT** prescribed (CC decides)

Если checklist failed — переписать command перед issuing.

### При написании DevPrompt'ов

DevPrompt обязан содержать:

- Numeric constraints с **citations к literature/probe** (не paraphrase from memory)
- Type isolation explicit (Protocol/Generic, не Union widening cross-phase)
- Runtime invariants (не metadata-only validation)
- Aggregations report group counts + estimand
- LOC estimates calibrated против analogous existing modules

См. memory rule #7 для checklist.

### При обнаружении систематических errors

Если architect делает 3+ ошибки подряд того же типа — записать **anti-pattern в Decisions.md** + memory.

Pattern recognition важнее tactical fix. Anti-pattern recorded → future commands самопроверяются.

### При phase transitions

Перед entering Phase N+1:

1. Phase N retrospective document — lessons learned записать
2. State refresh commit перед DevPrompt_NN.0 probe
3. Memory rules updated с new patterns observed

## Common anti-patterns recorded

### A. Numerical constraints без empirical verification
**Симптом:** architect specifies "X hours" / "Y meters" / "Z LOC" из памяти, оказывается wrong.
**Защита:** каждая numeric constant требует direct citation OR empirical probe.
**Пример (sat-revisit-tool):** "6h calibration per Mao 2023" — на самом деле Mao 2023 не specifies 6h floor. Wasted Session 4 на 2h cal benchmark с 1.1% convergence.

### B. Type widening (Union) instead of isolation (Protocol/Generic)
**Симптом:** new phase types added через `OldType | NewType` Union, contaminating prior phase code.
**Защита:** Protocol pattern или Generic с phase boundaries explicit.
**Пример:** Phase 2 GRACE-FO config added через `SentinelMission | GRACEFOMission` widening. GPT review flagged как Phase 1 type contamination.

### C. "Locked module" claim без downstream consumer audit
**Симптом:** architect declares module locked, но downstream consumers нуждаются breaking changes.
**Защита:** перед "locked" declaration — explicitly enumerate downstream consumers и verify changes compatible.
**Пример:** DevPrompt_07 declared `numerical.py` locked while DevPrompt_07 simultaneously required `forces.py` updates breaking `numerical.py` calls.

### D. Aggregation без n_groups + estimand reporting
**Симптом:** statistical aggregation reports single number без cluster/group counts.
**Защита:** каждое aggregation reports both n_observations AND n_groups (clusters), explicit estimand documentation.
**Пример:** cluster bootstrap не reported n_clusters, только n_arcs — overstates statistical power.

### E. Commands assuming infrastructure existence
**Симптом:** architect issues "run X" assuming runner exists; реальность — нужно build first.
**Защита:** каждая command — explicit assumptions section listing infrastructure prerequisites.
**Пример:** Session 6.1 launch command assumed VLEO production runner existed. Реальность — Phase 1 runner был для S-3A POE, Phase 2 нужен SP3-driven adapter (~250-400 LOC build).

### F. LOC estimates from training data
**Симптом:** architect estimates "~150 LOC" для new module, реальность 250-400.
**Защита:** Claude Code calibrates estimate против analogous existing module (read git ls-files + count LOC of comparable).

## Communication norms

### Architect side

- Не writing implementation details (что-то менее specific чем "module Foo handles Bar concern")
- Not apologizing для catching own errors via verification protocol — protocol working as designed
- Document errors recorded в Decisions.md для anti-pattern accumulation
- Honest acknowledgment когда no clear answer ("I'm guessing here, нужна probe")

### Claude Code side

- Verification reports brief (no extensive prose unless flagged issues)
- Implementation autonomy после direction approval (don't ask permission for naming)
- Escalate при substantive decisions, не tactical
- Не "architect knows better" deference — peer review stance

## Reusable template

CLAUDE_TEMPLATE.md содержит §16 (workflow protocol) ready к copy в новые проекты. Adapt §1-15 project-specific sections, keep §16 intact.

## Memory rules относящиеся

Memory items #11 (universal architect/CC workflow) и #12 (LLM error budget defenses) — cross-project rules применимые автоматически.

## Применение в существующих проектах

**Новый проект:**
1. Create DNA via project-dna skill
2. Create CLAUDE.md from CLAUDE_TEMPLATE.md (§16 protocol)
3. First DevPrompt_00.0 probe stage перед main implementation
4. Architect commands в goal-oriented format с assumptions section
5. Claude Code verification protocol active

**Existing project (retrofit):**
1. Audit existing CLAUDE.md — добавить §16 sections если missing
2. Записать observed anti-patterns в Decisions.md
3. Active immediately — applies к next architect command

## Когда НЕ применять

- **Solo coding** (без architect/CC pair) — overkill protocol
- **Throwaway prototypes** (не projects) — friction > benefit
- **Routine maintenance** (single-line fixes, dependency bumps) — не нужны verification protocols
- **Project-dna creation phase** — workflow protocol активируется AFTER DNA creation, не во время
- **Crisis fixes** (production down, hot fix) — speed > protocol для emergency context, document после

## Эволюция этого скилла

При observation новых anti-patterns в проектах — update этот skill:
1. Add anti-pattern в section "Common anti-patterns recorded"
2. Update memory rules если universal applicability
3. Update CLAUDE_TEMPLATE.md если pattern needs CLAUDE.md enforcement

Skill кодифицирует accumulated experience — растет с каждым проектом.
