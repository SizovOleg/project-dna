#!/usr/bin/env python3
"""signal_lint.py — проверка журнала сигналов (§15.3).

Поднимает §15.1 и §15.2 с наблюдаемого соблюдения на внешнюю проверку:
  - журнал существует и разбирается;
  - BLOCK — последняя строка (после него работа не продолжалась);
  - бюджет тишины не превышен (HEARTBEAT при длинных паузах);
  - счётчики Phase-end report совпадают с журналом.

Использование:
  python3 signal_lint.py SIGNALS.md [PHASE_N_REPORT.md]
Exit 0 — PASS, exit 1 — FAIL.
"""
import datetime as dt
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

KINDS = ("START", "HEARTBEAT", "NOTE", "BLOCK", "END")
LINE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}Z?)\s+"
    r"(?P<kind>[A-Z]+)\s*(?P<text>.*)$"
)
SILENCE_LIMIT_MIN = 15   # бюджет тишины по умолчанию


def parse_ts(raw: str) -> dt.datetime:
    return dt.datetime.strptime(raw.replace("T", " ").rstrip("Z"), "%Y-%m-%d %H:%M:%S")


def main(log_path: str, report_path: str | None) -> int:
    try:
        raw = open(log_path, encoding="utf-8").read()
    except OSError as e:
        print(f"FAIL: журнал не читается: {e}")
        return 1

    fails, warns, events = [], [], []
    for n, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = LINE.match(line)
        if not m:
            warns.append(f"строка {n} не разобрана: {line[:60]}")
            continue
        kind = m.group("kind")
        if kind not in KINDS:
            warns.append(f"строка {n}: неизвестный тип «{kind}»")
        try:
            events.append((parse_ts(m.group("ts")), kind, m.group("text"), n))
        except ValueError:
            fails.append(f"строка {n}: некорректная метка времени")

    if not events:
        print("FAIL: в журнале нет ни одного разобранного события")
        return 1

    # порядок по времени
    for a, b in zip(events, events[1:]):
        if b[0] < a[0]:
            fails.append(f"строка {b[3]}: метка времени раньше предыдущей — журнал не append-only")

    # BLOCK обязан быть последним содержательным событием
    for i, (_, kind, text, n) in enumerate(events):
        if kind == "BLOCK":
            after = [e for e in events[i + 1:] if e[1] not in ("END",)]
            if after:
                fails.append(
                    f"строка {n}: после BLOCK работа продолжалась "
                    f"({len(after)} событий, первое — строка {after[0][3]}). "
                    "BLOCK обязан останавливать (§15)"
                )
            break

    # бюджет тишины
    for a, b in zip(events, events[1:]):
        gap = (b[0] - a[0]).total_seconds() / 60
        if gap > SILENCE_LIMIT_MIN and b[1] != "HEARTBEAT":
            warns.append(
                f"строка {b[3]}: пауза {gap:.0f} мин без HEARTBEAT "
                f"(бюджет {SILENCE_LIMIT_MIN} мин, §15.1)"
            )

    counts = {k: sum(1 for e in events if e[1] == k) for k in KINDS}
    print("журнал: " + ", ".join(f"{k}={v}" for k, v in counts.items() if v))

    if counts["BLOCK"] > 1:
        warns.append(f"BLOCK встречается {counts['BLOCK']} раз — после первого работа не продолжается")
    if counts["NOTE"] > 5:
        warns.append(f"NOTE={counts['NOTE']} превышает ориентир 3–5 (§15.2): недоспецифицирован DevPrompt")

    # сверка со счётчиками отчёта
    if report_path:
        try:
            rep = open(report_path, encoding="utf-8").read()
        except OSError as e:
            fails.append(f"отчёт не читается: {e}")
        else:
            m = re.search(r"BLOCK\s*:\s*(\d+).*?NOTE\s*:\s*(\d+)", rep, re.S)
            if not m:
                fails.append("в отчёте нет счётчиков «BLOCK: N … NOTE: M» (§15.2)")
            else:
                rb, rn = int(m.group(1)), int(m.group(2))
                if rb != counts["BLOCK"] or rn != counts["NOTE"]:
                    fails.append(
                        f"счётчики отчёта (BLOCK={rb}, NOTE={rn}) расходятся с журналом "
                        f"(BLOCK={counts['BLOCK']}, NOTE={counts['NOTE']}) — "
                        "отчёт пересказывает, а не отражает факт"
                    )
                else:
                    print(f"счётчики отчёта совпадают с журналом: BLOCK={rb}, NOTE={rn}")

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
    if len(sys.argv) not in (2, 3):
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) == 3 else None))
