#!/usr/bin/env python3
"""suite_lint.py — проверка §16.1 «полнота по построению».

Каждый анти-паттерн скилла обязан иметь хотя бы один тест в suite; каждый тест
обязан ссылаться на существующий анти-паттерн или на раздел скилла. Проверка
скоупится разделом «Common anti-patterns recorded» — вне его те же заголовки
`### A.` встречаются в шаблоне verification report и в подсчёт не идут.

Дополнительно: тесты, у которых нет строки в baseline, перечисляются отдельно —
по §16.3 добавление анти-паттерна триггерит full-прогон.

Использование: python3 suite_lint.py SKILL.md REGRESSION_SUITE.md
Exit 0 — PASS, exit 1 — FAIL.
"""
import io
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AP_SECTION = "## Common anti-patterns recorded"


def anti_patterns(skill: str) -> list[str]:
    try:
        i = skill.index(AP_SECTION)
    except ValueError:
        return []
    j = skill.index("\n## ", i + len(AP_SECTION))
    return sorted(set(re.findall(r"^### ([A-Z])\.", skill[i:j], re.M)))


def tests(suite: str) -> dict[str, str]:
    out = {}
    for m in re.finditer(r"^\*\*(T-[A-Z0-9-]+)\*\*\s*·\s*(?:паттерн\s*)?([A-Z§0-9.]+)", suite, re.M):
        out[m.group(1)] = m.group(2)
    return out


def baseline_ids(suite: str) -> set[str]:
    return set(re.findall(r"^\|\s*\*?\*?(T-[A-Z0-9-]+)", suite, re.M))


def main(skill_path: str, suite_path: str) -> int:
    skill = io.open(skill_path, encoding="utf-8").read()
    suite = io.open(suite_path, encoding="utf-8").read()

    ap = anti_patterns(skill)
    ts = tests(suite)
    base = baseline_ids(suite)

    if not ap:
        print(f"FAIL: раздел «{AP_SECTION}» не найден — нечего проверять")
        return 1

    covered = {v[0] for v in ts.values() if v and v[0].isalpha()}
    print(f"анти-паттернов: {len(ap)} | тестов: {len(ts)} | строк baseline: {len(base)}")

    fails, warns = [], []

    missing = [a for a in ap if a not in covered]
    if missing:
        fails.append(
            "анти-паттерны без теста (§16.1, изменение считается незавершённым): "
            + ", ".join(missing)
        )

    orphan = sorted({v[0] for v in ts.values() if v and v[0].isalpha()} - set(ap))
    if orphan:
        warns.append("тесты ссылаются на несуществующий анти-паттерн: " + ", ".join(orphan))

    unmeasured = sorted(t for t in ts if t not in base)
    if unmeasured:
        warns.append(
            f"тестов без строки в baseline: {len(unmeasured)} ({', '.join(unmeasured)}) — "
            "по §16.3 добавление анти-паттерна триггерит full-прогон"
        )

    for w in warns:
        print(f"WARN: {w}")
    if fails:
        for f_ in fails:
            print(f"FAIL: {f_}")
        print(f"\nИтог: FAIL ({len(fails)} нарушений, {len(warns)} предупреждений)")
        return 1
    print(f"\nИтог: PASS ({len(warns)} предупреждений)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
