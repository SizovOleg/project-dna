#!/bin/sh
# pre-commit-dna — механическая проверка DNA перед коммитом (project-dna, ступень 5).
#
# Срабатывает ТОЛЬКО если в коммит попал DNA-файл. Обычные коммиты не трогает.
#
# Режимы:
#   предупреждение (по умолчанию) — печатает отчёт, коммит проходит
#   блокировка                    — git config dnalint.blocking true
#
# Блокировка по умолчанию выключена намеренно: DNA, написанные до введения
# «признаков нарушения», не проходят линт целиком. Включать по проекту —
# после того, как его DNA приведён к формату.

set -u

HOOK_DIR=$(cd "$(dirname "$0")" && pwd)
LINT="$HOOK_DIR/dna_lint.py"

[ -f "$LINT" ] || { echo "pre-commit-dna: dna_lint.py не найден, проверка пропущена" >&2; exit 0; }

PY=""
for c in python3 python py; do
    command -v "$c" >/dev/null 2>&1 && { PY="$c"; break; }
done
[ -n "$PY" ] || { echo "pre-commit-dna: python не найден, проверка пропущена" >&2; exit 0; }

# DNA-файлы в индексе (без удалённых)
FILES=$(git diff --cached --name-only --diff-filter=ACMR \
        | grep -Ei '(^|/)(dna|project_dna|research_dna|[a-z0-9_-]+_dna)\.md$' || true)
[ -n "$FILES" ] || exit 0

BLOCKING=$(git config --bool dnalint.blocking 2>/dev/null || echo false)
RC=0

echo "─── dna_lint ─────────────────────────────────────────"
for f in $FILES; do
    [ -f "$f" ] || continue
    echo "· $f"
    "$PY" "$LINT" "$f" 2>&1 | sed 's/^/  /'
    [ "${PIPESTATUS:-0}" = "0" ] || true
    "$PY" "$LINT" "$f" >/dev/null 2>&1 || RC=1
done
echo "──────────────────────────────────────────────────────"

if [ "$RC" != "0" ]; then
    if [ "$BLOCKING" = "true" ]; then
        echo "Коммит остановлен: DNA не проходит линт." >&2
        echo "Обойти разово: git commit --no-verify" >&2
        exit 1
    fi
    echo "Режим предупреждения — коммит проходит."
    echo "Включить блокировку в этом проекте: git config dnalint.blocking true"
fi
exit 0
