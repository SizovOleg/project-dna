#!/usr/bin/env python3
"""report_lint.py — механическая проверка Phase-end report.

Поднимает на ступень 5 (внешняя проверка, которая падает):
  §11 частично — запрещённые фразы самосертификации;
  §12 частично — наличие confidence markers (корректность непроверяема в принципе);
  §15.2 — присутствие счётчиков signal budget;
  структуру отчёта из «При phase transitions».

Использование: python3 report_lint.py PHASE_N_REPORT.md
Exit 0 — PASS (warnings допустимы), exit 1 — FAIL.
"""
import re
import sys

# Windows-консоль по умолчанию в кодировке ANSI (cp1251 и т.п.):
# вывод со стрелками и типографикой падает UnicodeEncodeError,
# а exit=1 от краха неотличим от exit=1 от нарушения.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REQUIRED_SECTIONS = [
    "Сделано",
    "Не сделано",
    "Tool-budget",
    "Signal budget",
    "Открытые вопросы",
    "Что НЕ проверено",
    "Решения без согласования",
]

# §11: формулировки, игнорируемые как статистическое продолжение.
# В отчёте их быть не должно — отчёт перечисляет факты и маркеры,
# вердикт о завершении выносит архитектор.
FORBIDDEN = [
    r"\btask\s+complete\b",
    r"\ball\s+done\b",
    r"\bproduction[\s-]+ready\b",
    r"\bвсё\s+готово\b",
    r"\bполностью\s+готово\b",
    r"\bготово\s+к\s+прод\w*\b",
    r"\bвсе\s+тесты\s+прошли\b",
    r"\ball\s+tests\s+pass(ed)?\b",
    r"\bimplementation\s+finished\b",
    r"\beverything\s+works\b",
]

MARKER = r"\[(VERIFIED|TESTED|INSPECTED|ASSUMED|GUESSED)\]"
BUDGET = r"BLOCK\s*:\s*\d+.*NOTE\s*:\s*\d+"


def main(path: str) -> int:
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"FAIL: не удалось прочитать {path}: {e}")
        return 1

    fails, warns = [], []

    for sec in REQUIRED_SECTIONS:
        if not re.search(r"^#{2,4}\s*" + re.escape(sec), text, re.M | re.I):
            fails.append(f"отсутствует секция «{sec}»")

    for pat in FORBIDDEN:
        for m in re.finditer(pat, text, re.I):
            line = text[: m.start()].count("\n") + 1
            fails.append(f"строка {line}: фраза самосертификации «{m.group(0)}» (§11)")

    markers = re.findall(MARKER, text)
    if not markers:
        fails.append("ни одного confidence marker (§12) во всём отчёте")
    else:
        counts = {}
        for mk in markers:
            counts[mk] = counts.get(mk, 0) + 1
        print("markers:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())))
        low = counts.get("ASSUMED", 0) + counts.get("GUESSED", 0)
        if low:
            warns.append(
                f"{low} утверждений [ASSUMED]/[GUESSED] — архитектор решает, "
                "какие поднять до [VERIFIED] (§12)"
            )

    if not re.search(BUDGET, text, re.S):
        fails.append("нет счётчиков «BLOCK: N … NOTE: M» (§15.2)")

    # Эвристика: строки с числами в секции «Сделано» без маркера — warning.
    m = re.search(
        r"^#{2,4}\s*Сделано(.*?)(?=^#{2,4}\s|\Z)", text, re.M | re.S | re.I
    )
    if m:
        for i, line in enumerate(m.group(1).splitlines(), 1):
            if re.search(r"\d", line) and line.strip().startswith("-"):
                if not re.search(MARKER, line):
                    warns.append(f"«Сделано», пункт с числом без маркера: {line.strip()[:60]}")

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
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
