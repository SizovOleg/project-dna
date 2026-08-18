#!/usr/bin/env python3
"""stream-json -> плоский текст: ассистентский текст + вызовы инструментов.
Грепы ассертов должны видеть и рассуждения, и фактические действия."""
import json
import sys

def main(path: str) -> None:
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("{"):
                if line:
                    print(line)
                continue
            try:
                ev = json.loads(line)
            except Exception:
                print(line)
                continue
            msg = ev.get("message") or {}
            for b in msg.get("content") or []:
                if not isinstance(b, dict):
                    continue
                kind = b.get("type")
                if kind == "text":
                    print(b.get("text", ""))
                elif kind == "tool_use":
                    payload = json.dumps(b.get("input", {}), ensure_ascii=False)
                    print("[TOOL {}] {}".format(b.get("name"), payload[:2000]))
                elif kind == "tool_result":
                    c = b.get("content")
                    text = c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)
                    print("[RESULT] {}".format(text[:2000]))
            if ev.get("type") == "result" and ev.get("result"):
                print(ev["result"])

if __name__ == "__main__":
    main(sys.argv[1])
