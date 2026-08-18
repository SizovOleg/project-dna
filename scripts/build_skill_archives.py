#!/usr/bin/env python3
"""build_skill_archives.py — собирает .skill-архивы из содержимого репозитория.

    python3 scripts/build_skill_archives.py [каталог_назначения]

Формат .skill — обычный zip с каталогом <имя>/ внутри (стандарт Agent Skills).
Кроме SKILL.md кладутся сопутствующие артефакты: карты enforcement, suite, harness.
Дополнительно собирается bundle со всеми скиллами и README для передачи коллегам.

Без внешних зависимостей: zip-бинарник в системе не нужен.
"""
import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "skills"
SKILLS = ["architect-cc-workflow", "project-dna", "research-with-ai"]
SKIP = {"__pycache__", ".DS_Store"}

README = """# DNA/RNA skills — комплект для установки

Три скилла, работающие в связке:

| Скилл | Отвечает за |
|---|---|
| `project-dna` | Инварианты проекта: что нельзя нарушить и почему |
| `architect-cc-workflow` | Дисциплина исполнения: как обе стороны ловят ошибки друг друга |
| `research-with-ai` | Эпистемика: что считать истиной |

Порядок включения: `research-with-ai` (режим 8, разведка области) → `project-dna`
(инварианты) → `architect-cc-workflow` (исполнение).

## Установка

```bash
# для всех проектов
cp -r project-dna architect-cc-workflow research-with-ai ~/.claude/skills/

# для одного проекта
cp -r project-dna architect-cc-workflow research-with-ai .claude/skills/
```

Проверить: в Claude Code спросить «какие у тебя скиллы?».

## Что кроме SKILL.md

`ENFORCEMENT_MAP.md` — честная оценка каждого правила по шестиступенчатой шкале:
от «текст в скилле» (намерение) до «архитектурная невозможность». Ступень
определяется внешностью проверки, а не формулировкой: слово «ЗАПРЕЩЕНО» в тексте
ступень не поднимает.

`REGRESSION_SUITE.md` — поведенческие тесты и baseline с измеренными числами.
Baseline — функция пары (скилл, модель): при смене модели он недействителен
целиком и перепрогоняется.

`harness/` — внешние проверки, поднимающие правила на ступень 5:

| Скрипт | Проверяет |
|---|---|
| `project-dna/harness/dna_lint.py` | структуру DNA: технологии, объём, признаки нарушения, негативные инварианты |
| `project-dna/harness/install-hook.sh` | ставит dna_lint как pre-commit (по умолчанию предупреждение, не блокировка) |
| `architect-cc-workflow/harness/report_lint.py` | Phase-end report: обязательные секции, запрет самосертификации, confidence markers |
| `architect-cc-workflow/harness/signal_lint.py` | журнал сигналов: BLOCK раньше остановки, сверка счётчиков отчёта с фактом |
| `architect-cc-workflow/harness/run_smoke.sh` | прогон смоук-набора (запускать вне сессии Claude Code) |

## Известные ограничения

- `run_smoke.sh` не работает изнутри сессии Claude Code: CLI отказывается
  запускать вложенную сессию. Запускать из обычного терминала.
- Блокирующий режим pre-commit включается по проекту после приведения DNA
  к формату: `git config dnalint.blocking true`. По умолчанию — предупреждение,
  потому что DNA, написанные до введения признаков нарушения, линт не проходят.
- Дискриминантность тестов измерена частично: для T-H-1 контроль без скилла
  дал тот же результат — этот тест меряет базовую модель, а не протокол.
"""


def files_of(root: Path):
    for p in sorted(root.rglob("*")):
        if p.is_file() and not any(part in SKIP for part in p.parts):
            yield p


def write_zip(target: Path, pairs) -> None:
    target.unlink(missing_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
        for path, arcname in pairs:
            z.write(path, arcname)


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "dist"
    out.mkdir(parents=True, exist_ok=True)
    built = []

    for s in SKILLS:
        d = SRC / s
        if not d.is_dir():
            print(f"пропуск: {d} нет")
            continue
        target = out / f"{s}.skill"
        write_zip(target, ((p, str(Path(s) / p.relative_to(d)).replace("\\", "/"))
                           for p in files_of(d)))
        n = sum(1 for _ in files_of(d))
        print(f"{target.name:<34} {target.stat().st_size:>7} байт, файлов: {n}")
        built.append(target)

    bundle = out / "dna-rna-skills-bundle.zip"
    pairs = []
    for s in SKILLS:
        d = SRC / s
        if d.is_dir():
            pairs += [(p, str(Path(s) / p.relative_to(d)).replace("\\", "/"))
                      for p in files_of(d)]
    tmp_readme = out / "_README.md"
    tmp_readme.write_text(README, encoding="utf-8")
    pairs.append((tmp_readme, "README.md"))
    write_zip(bundle, pairs)
    tmp_readme.unlink()
    print(f"{bundle.name:<34} {bundle.stat().st_size:>7} байт, файлов: {len(pairs)}")
    built.append(bundle)

    print("\nsha256:")
    for b in built:
        h = hashlib.sha256(b.read_bytes()).hexdigest()
        print(f"  {h[:16]}  {b.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
