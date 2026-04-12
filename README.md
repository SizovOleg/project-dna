# Project DNA

**Create, maintain, and audit root project documents with implementation-independent invariants.**

DNA (Decision Nucleic Acid) is a compact document (2-5 pages) that captures only the decisions that hold true **regardless of implementation** — no technology names, no frameworks, no models. Just "what" and "why".

## Why DNA?

When working with AI coding agents, the biggest risk is not bad code — it's code that solves the wrong problem. DNA prevents this by giving agents a set of **invariants** they must never violate, while leaving implementation decisions flexible.

```
DNA.md — invariants, for humans
  ↓
RNA / Harness — enforcement, for the agent
  ├── CLAUDE.md (contract with the agent)
  ├── Skills (codified experience)
  └── Plugins / MCP (tooling)
  ↓
Requirements → TechnicalDesign → Code
  ↑
DNA audit (feedback loop)
```

## What This Skill Does

The `project-dna` skill provides 5 operational modes:

| Mode | Trigger | What it does |
|------|---------|-------------|
| **Create DNA** | "start project", "create DNA" | Guides you through crystallizing domain knowledge into a DNA document |
| **DNA Audit** | "check compliance", "DNA audit" | Compares code against DNA invariants, reports violations and gaps |
| **Extract DNA** | "what are our invariants" | Reverse-engineers DNA from an existing codebase |
| **Mutate DNA** | "update DNA" | Safely updates DNA with versioning and impact analysis |
| **Create RNA** | "create harness" | Translates DNA invariants into stack-specific enforcement rules |

### The Four Layers

DNA is structured around four philosophical layers:

- **Ontology** — what entities exist and how they relate
- **Deontology** — what is permitted and what is forbidden
- **Axiology** — what is valuable and what is not
- **Praxeology** — how to act

## Installation

### Claude Code (plugin)

```bash
claude plugin install <username>/project-dna
```

### Claude Code (manual)

Copy the skill directory to your skills folder:

```bash
# Personal (all projects)
cp -r skills/project-dna ~/.claude/skills/

# Project-specific
cp -r skills/project-dna .claude/skills/
```

### Other AI Agents

Copy `skills/project-dna/SKILL.md` to your agent's skills directory. The skill follows the open [Agent Skills](https://agentskills.io) standard and works with any compatible agent.

## Usage

Once installed, the skill activates automatically when you:

- Start a new project: *"Let's create a DNA for this project"*
- Need an audit: *"Run a DNA audit"*
- Want to understand invariants: *"What are our invariants?"*
- Need to update: *"This decision is outdated, update the DNA"*
- Need enforcement rules: *"Create RNA for our Python/PostgreSQL stack"*

## Additional Resources

- [Full DNA/RNA Methodology (English)](references/methodology-en.md) — philosophy, anti-patterns, lifecycle, roles
- [Full DNA/RNA Methodology (Russian)](references/methodology-ru.md) — original methodology document

## License

MIT

---

# Project DNA (RU)

**Создание, поддержка и аудит корневых документов проекта с инвариантами, независимыми от реализации.**

DNA (Decision Nucleic Acid) — компактный документ (2-5 страниц), содержащий только решения, верные **независимо от реализации**. Без названий технологий, фреймворков, моделей. Только «что» и «почему».

### Установка

```bash
# Персональная (все проекты)
cp -r skills/project-dna ~/.claude/skills/

# Для конкретного проекта
cp -r skills/project-dna .claude/skills/
```

### 5 режимов работы

1. **Создание DNA** — кристаллизация доменного знания в DNA-документ
2. **DNA-аудит** — проверка кода на соответствие инвариантам
3. **Извлечение DNA** — обратное проектирование DNA из существующего кода
4. **Мутация DNA** — безопасное обновление с версионированием
5. **Создание RNA** — трансляция инвариантов в правила для конкретного стека

Подробная методология: [references/methodology-ru.md](references/methodology-ru.md)
