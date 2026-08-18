#!/bin/sh
# install-hook.sh — ставит dna_lint как pre-commit в указанный репозиторий.
#
#   sh install-hook.sh /path/to/repo
#
# Кладёт хук и линт в .git/hooks/ — отслеживаемое содержимое репозитория
# не меняется. Существующий чужой хук не затирается: он сохраняется и
# вызывается первым (цепочка).
#
# Репозитории на фреймворке pre-commit (есть .pre-commit-config.yaml)
# определяются отдельно: там .git/hooks/pre-commit генерируемый, и правка
# делается в конфиге. Установщик такой репозиторий не трогает, а печатает
# готовый фрагмент для вставки.

set -eu
REPO="${1:?укажи путь к репозиторию}"
SRC=$(cd "$(dirname "$0")" && pwd)

[ -d "$REPO/.git" ] || { echo "$REPO: не git-репозиторий — пропуск"; exit 0; }

HOOKS="$REPO/.git/hooks"
mkdir -p "$HOOKS"

if [ -f "$REPO/.pre-commit-config.yaml" ]; then
    cat <<YAML
$REPO: фреймворк pre-commit. .git/hooks/pre-commit генерируемый — не трогаю.
Вставь в .pre-commit-config.yaml (это отслеживаемый файл, изменение на твоё ревью):

  - repo: local
    hooks:
      - id: dna-lint
        name: dna_lint (структура DNA)
        entry: python skills/project-dna/harness/dna_lint.py
        language: system
        files: '(^|/)(DNA|Project_DNA|Research_DNA)\.md$'
        pass_filenames: true
YAML
    exit 0
fi

cp "$SRC/dna_lint.py" "$HOOKS/dna_lint.py"

if [ -f "$HOOKS/pre-commit" ] && ! grep -q 'pre-commit-dna' "$HOOKS/pre-commit" 2>/dev/null; then
    mv "$HOOKS/pre-commit" "$HOOKS/pre-commit.local"
    chmod +x "$HOOKS/pre-commit.local"
    cp "$SRC/pre-commit-dna.sh" "$HOOKS/pre-commit-dna"
    cat > "$HOOKS/pre-commit" <<'CHAIN'
#!/bin/sh
# Цепочка: существовавший хук, затем dna_lint.
set -e
[ -x "$(dirname "$0")/pre-commit.local" ] && "$(dirname "$0")/pre-commit.local" "$@"
exec "$(dirname "$0")/pre-commit-dna" "$@"
CHAIN
    chmod +x "$HOOKS/pre-commit" "$HOOKS/pre-commit-dna"
    echo "$REPO: установлен в цепочке (прежний хук → pre-commit.local)"
else
    cp "$SRC/pre-commit-dna.sh" "$HOOKS/pre-commit"
    chmod +x "$HOOKS/pre-commit"
    echo "$REPO: установлен"
fi

MODE=$(cd "$REPO" && git config --bool dnalint.blocking 2>/dev/null || echo false)
echo "  режим: $([ "$MODE" = true ] && echo блокировка || echo предупреждение)"
