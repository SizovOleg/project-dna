#!/usr/bin/env python3
"""dna_lint.py — механическая проверка DNA.md.

Поднимает на ступень 5 структурные правила project-dna:
  - нет названий технологий (стоп-слова);
  - компактность (2-5 страниц ~ до 2600 слов);
  - каждый инвариант раздела 3 имеет «Признак нарушения:»;
  - раздел 6 (негативные инварианты) существует и непуст;
  - раздел 7 (числовые инварианты) существует (пустота — warning);
  - раздел 4.2 содержит формат разрешённых дилемм;
  - блок «Ключевые инварианты» присутствует в конце файла;
  - ASSUMPTIONS.md существует рядом (иначе warning).

Содержательное КАЧЕСТВО признака нарушения линт не проверяет и не может —
это ступень 1, закрывается аудитом (Режим 2, блок 🩺).

Использование: python3 dna_lint.py path/to/DNA.md
Exit 0 — PASS, exit 1 — FAIL.
"""
import os
import re
import sys

# Windows-консоль по умолчанию в кодировке ANSI (cp1251 и т.п.):
# вывод со стрелками и типографикой падает UnicodeEncodeError,
# а exit=1 от краха неотличим от exit=1 от нарушения.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TECH_STOPWORDS = [
    "python", "javascript", "typescript", "java", "golang", "rust",
    "postgres", "postgresql", "mysql", "sqlite", "mongodb", "redis",
    "docker", "kubernetes", "nginx", "fastapi", "flask", "django",
    "react", "vue", "angular", "node.js", "nodejs",
    "langchain", "llamaindex", "ollama", "vllm",
    "gpt-", "claude", "gemini", "deepseek", "qwen", "llama",
    "aws", "azure", "gcp", "bedrock", "vertex",
    "pandas", "numpy", "pytorch", "tensorflow",
    "n8n", "airflow", "kafka",
]

WORD_LIMIT = 2600  # ~5 страниц

# DNA пишется на языке доменного эксперта — линт не должен требовать русского.
MARKER_VIOLATION = ("признак нарушения", "violation indicator")
# Плейсхолдер содержит слова маркера, но признаком не является:
# незаполненное поле не должно засчитываться как заполненное.
PLACEHOLDER = ("требует владельца", "requires owner", "[todo", "tbd", "уточнить")
MARKER_DILEMMA = ("когда нельзя одновременно", "when we cannot both", "когда нельзя одновременнo")


def section(text: str, num: int) -> str | None:
    m = re.search(
        rf"^##\s*{num}\.\s.*?$(.*?)(?=^##\s*\d+\.|\Z)", text, re.M | re.S
    )
    return m.group(1) if m else None


def main(path: str) -> int:
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        print(f"FAIL: не удалось прочитать {path}: {e}")
        return 1

    fails, warns = [], []
    lower = text.lower()

    # 1. Технологии (длинные слова первыми, чтобы «postgresql» съел «postgres»)
    flagged_spans: list[tuple[int, int]] = []
    for word in sorted(TECH_STOPWORDS, key=len, reverse=True):
        for m in re.finditer(re.escape(word), lower):
            if any(m.start() < e and m.end() > s for s, e in flagged_spans):
                continue  # подстрока уже флагнутого слова
            line_no = lower[: m.start()].count("\n") + 1
            line = text.splitlines()[line_no - 1].strip()
            if line.startswith(">") or "пример" in line.lower():
                continue  # цитаты/примеры не считаем
            flagged_spans.append((m.start(), m.end()))
            fails.append(f"строка {line_no}: технология «{word}» — DNA не содержит реализации")
            break  # одного вхождения на слово достаточно

    # 2. Компактность
    words = len(re.findall(r"\S+", text))
    if words > WORD_LIMIT:
        fails.append(f"объём {words} слов > {WORD_LIMIT} (~5 стр). DNA всегда компактный")
    else:
        print(f"объём: {words} слов (лимит {WORD_LIMIT})")

    # 3. Признак нарушения в каждом инварианте раздела 3
    sec3 = section(text, 3)
    if sec3 is None:
        fails.append("раздел 3 (Ограничения) не найден")
    else:
        subs = re.split(r"^###\s+", sec3, flags=re.M)[1:]
        if not subs:
            warns.append("раздел 3 без подразделов ### — нечего проверять на признаки")
        for sub in subs:
            title = sub.splitlines()[0].strip()
            low = sub.lower()
            if not any(k in low for k in MARKER_VIOLATION):
                fails.append(f"инвариант «{title}»: нет «Признак нарушения:» — лозунг, не инвариант")
            else:
                # строка(и) с маркером — проверяем, что там не заглушка
                marked = [
                    ln for ln in sub.splitlines()
                    if any(k in ln.lower() for k in MARKER_VIOLATION)
                ]
                if marked and all(
                    any(ph in ln.lower() for ph in PLACEHOLDER) for ln in marked
                ):
                    fails.append(
                        f"инвариант «{title}»: признак не заполнен (заглушка) — "
                        "ждёт владельца, засчитывать нельзя"
                    )

    # 4. Негативные инварианты
    sec6 = section(text, 6)
    if sec6 is None:
        fails.append("раздел 6 (Негативные инварианты) отсутствует — нет защиты от accretion")
    elif len(re.sub(r"[#\s\[\]().]", "", sec6)) < 60:
        fails.append("раздел 6 существует, но пуст — заполнить или честно удалить")

    # 5. Числовые инварианты
    sec7 = section(text, 7)
    if sec7 is None:
        warns.append("раздел 7 (Числовые инварианты) отсутствует — ок только для не-data проектов")
    elif not re.search(r"\d", sec7):
        warns.append("раздел 7 без единого числа/диапазона")

    # 6. Аксиология как дилеммы
    sec4 = section(text, 4)
    if sec4 and not any(k in sec4.lower() for k in MARKER_DILEMMA):
        warns.append("раздел 4: нет формата «Когда нельзя одновременно A и B → …» — перечень вместо правила выбора")

    # 7. Ключевые инварианты в конце
    tail = text[-2500:]
    if not re.search(r"ключевые\s+инварианты|key\s+invariants", tail, re.I):
        fails.append("нет блока «Ключевые инварианты» в конце — правило только в середине игнорируется агентом")

    # 8. ASSUMPTIONS.md рядом
    neighbor = os.path.join(os.path.dirname(os.path.abspath(path)), "ASSUMPTIONS.md")
    if not os.path.exists(neighbor):
        warns.append("рядом нет ASSUMPTIONS.md — гипотезам некуда деваться, осядут в DNA")

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
