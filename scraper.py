import json
import sys
import urllib.request
from pathlib import Path

BASE = "https://zeustv274.live"
OUT = Path("data")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

TARGETS = {
    "matches.json": "/api/v1/match-center",
    "channels.json": "/api/v1/channels",
}


def get(path):
    req = urllib.request.Request(BASE + path, headers={
        "User-Agent": UA,
        "Accept": "application/json",
        "Referer": BASE + "/",
    })
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    OUT.mkdir(exist_ok=True)
    ok = 0
    for filename, path in TARGETS.items():
        try:
            data = get(path)
        except Exception as e:
            print(f"[hata] {filename}: {e}")
            continue
        (OUT / filename).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[ok] {filename}")
        ok += 1
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
