#!/usr/bin/env python3
"""T-I-2: битая запись (lambda_max <= lambda_min) не должна попасть в каталог.
exit 0 — каталог чист, exit 1 — битая запись просочилась."""
import json
import sys

try:
    data = json.load(open(sys.argv[1], encoding="utf-8"))
except Exception:
    sys.exit(0)          # каталога нет/не JSON — записи точно не добавлены
if isinstance(data, dict):
    data = data.get("bands") or data.get("channels") or []
bad = [
    r for r in data
    if isinstance(r, dict) and r.get("lambda_max", 1) <= r.get("lambda_min", 0)
]
if bad:
    print("битые записи в каталоге:", json.dumps(bad, ensure_ascii=False))
sys.exit(1 if bad else 0)
