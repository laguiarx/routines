#!/usr/bin/env python3
"""Lista advisories críticos e pacotes maliciosos populares no OSV desde uma data.

Uso: python3 osv_recent.py DESDE [--min-downloads N]
Exemplo: python3 osv_recent.py 2026-10-26

Fontes: exportação do OSV (inclui GHSA, RustSec e MAL do OpenSSF) e API de downloads do npm.
Só usa a biblioteca padrão.
"""
import argparse
import json
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ECOSYSTEMS = ["npm", "crates.io"]
EXPORT = "https://osv-vulnerabilities.storage.googleapis.com/{}/modified_id.csv"
RECORD = "https://api.osv.dev/v1/vulns/{}"
NPM_DOWNLOADS = "https://api.npmjs.org/downloads/point/last-week/{}"


def get(url, as_json=True):
    with urllib.request.urlopen(url, timeout=30) as r:
        data = r.read().decode()
    return json.loads(data) if as_json else data


def recent_ids(ecosystem, since):
    # A exportação vem ordenada do mais recente para o mais antigo.
    ids = []
    for line in get(EXPORT.format(ecosystem), as_json=False).splitlines():
        modified, _, vid = line.partition(",")
        if modified[:10] < since:
            break
        ids.append(vid)
    return ids


def fetch(vid):
    try:
        return get(RECORD.format(vid))
    except Exception as e:
        return {"id": vid, "_error": str(e)}


def weekly_downloads(pkg):
    try:
        return get(NPM_DOWNLOADS.format(urllib.parse.quote(pkg, safe="@"))).get("downloads", 0)
    except Exception:
        return 0


def summarize(rec):
    affected = rec.get("affected", [])
    fixed = sorted({
        ev["fixed"]
        for a in affected for r in a.get("ranges", []) for ev in r.get("events", []) if "fixed" in ev
    })
    return {
        "id": rec["id"],
        "aliases": rec.get("aliases", []),
        "packages": sorted({a["package"]["name"] for a in affected if "package" in a}),
        "published": rec.get("published", "")[:10],
        "modified": rec.get("modified", "")[:10],
        "severity": rec.get("database_specific", {}).get("severity"),
        "cvss": [s["score"] for s in rec.get("severity", [])],
        "fixed": fixed,
        "summary": rec.get("summary", ""),
        "url": f"https://osv.dev/vulnerability/{rec['id']}",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("since", help="AAAA-MM-DD")
    p.add_argument("--min-downloads", type=int, default=50_000)
    args = p.parse_args()

    out = {"since": args.since, "critical": [], "unrated_with_cvss": [], "malicious_popular": [], "errors": []}
    with ThreadPoolExecutor(max_workers=16) as pool:
        for eco in ECOSYSTEMS:
            try:
                ids = recent_ids(eco, args.since)
            except Exception as e:
                out["errors"].append(f"{eco}: exportação falhou: {e}")
                continue
            for rec in pool.map(fetch, ids):
                if "_error" in rec:
                    out["errors"].append(f"{rec['id']}: {rec['_error']}")
                    continue
                s = summarize(rec)
                s["ecosystem"] = eco
                if rec["id"].startswith("MAL-"):
                    s["downloads_last_week"] = max((weekly_downloads(pk) for pk in s["packages"]), default=0) if eco == "npm" else None
                    if s["downloads_last_week"] and s["downloads_last_week"] >= args.min_downloads:
                        out["malicious_popular"].append(s)
                elif (s["severity"] or "").upper() == "CRITICAL":
                    out["critical"].append(s)
                elif not s["severity"] and s["cvss"]:
                    out["unrated_with_cvss"].append(s)

    json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
