#!/usr/bin/env python3
"""Validate recorded reviews; does not perform OCR or visual inspection."""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

CHECKS = ["logo_glyphs", "product_name", "packaging", "typography",
          "evidence", "efficacy_visual", "composition"]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def norm(value):
    # Only layout whitespace is ignored. Case, glyphs, numbers and punctuation matter.
    return re.sub(r"\s+", "", value)

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def within(root, name):
    rel = Path(name)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("Image path must be relative and remain within --root: " + name)
    p = (root / rel).resolve()
    if not p.is_relative_to(root):
        raise ValueError("Image path escapes --root: " + name)
    if not p.is_file() or p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise ValueError("Missing or unsupported image: " + str(p))
    return p

def load_manifest(path, root):
    m = read(path)
    if not isinstance(m, dict):
        raise ValueError('Manifest must be an object.')
    if not nonempty(m.get("product_id")) or not isinstance(m.get("pages"), list) or not m["pages"]:
        raise ValueError("Manifest needs product_id and nonempty pages.")
    ids, image_paths = set(), set()
    for page in m["pages"]:
        pid = page.get("page_id")
        if not nonempty(pid) or pid in ids:
            raise ValueError("Missing/duplicate page_id.")
        ids.add(pid)
        if not nonempty(page.get("file")):
            raise ValueError(pid + ": missing file.")
        image = within(root, page["file"])
        if str(image) in image_paths:
            raise ValueError("Same image assigned to multiple pages.")
        image_paths.add(str(image))
        texts = page.get("critical_text")
        if not isinstance(texts, list) or not texts:
            raise ValueError(pid + ": critical_text must not be empty.")
        tids = set()
        for item in texts:
            tid = item.get("id")
            if not nonempty(tid) or tid in tids:
                raise ValueError(pid + ": missing/duplicate text id.")
            tids.add(tid)
            if not nonempty(item.get("expected")) or not nonempty(item.get("source")):
                raise ValueError(pid + "/" + tid + ": expected text and source required.")
    return m

def initialize(args):
    if args.record.exists():
        raise ValueError("Review already exists. Use a new record filename; do not erase earlier review.")
    root = args.root.resolve()
    m = load_manifest(args.manifest, root)
    pages = []
    for p in m["pages"]:
        pages.append({
            "page_id": p["page_id"], "file": p["file"],
            "image_sha256": sha(within(root, p["file"])),
            "reviewer": "", "reviewed_at": "",
            "critical_text": [
                {"id": t["id"], "observed": "", "review_method": "",
                 "source_verified": False, "notes": ""} for t in p["critical_text"]],
            "visual_checks": {
                k: {"status": "pending", "notes": ""} for k in CHECKS},
            "issues": []
        })
    write(args.record, {
        "schema_version": 1, "product_id": m["product_id"],
        "manifest_sha256": sha(args.manifest),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tool_scope": "Recorded-review gate only; no OCR or visual recognition.",
        "pages": pages
    })
    print("Created pending review: " + str(args.record))
    return 0

def keyed(items, key, label, errors):
    if not isinstance(items, list):
        errors.append(label + ": must be a list")
        return {}
    result = {}
    for item in items:
        if not isinstance(item, dict) or not nonempty(item.get(key)):
            errors.append(label + ": invalid item")
            continue
        if item[key] in result:
            errors.append(label + ": duplicate " + item[key])
        result[item[key]] = item
    return result

def check(args):
    root = args.root.resolve()
    m = load_manifest(args.manifest, root)
    if args.out:
        protected = {args.manifest.resolve(), args.record.resolve()}
        protected.update(within(root, p['file']) for p in m['pages'])
        if args.out.resolve() in protected or args.out.suffix.lower() != '.json':
            raise ValueError('Result output must be a separate JSON file, never a source image/manifest/review.')
    r = read(args.record)
    if not isinstance(r, dict):
        raise ValueError('Review must be an object.')
    errors = []
    if r.get("schema_version") != 1:
        errors.append("Unsupported review schema.")
    if r.get("product_id") != m["product_id"]:
        errors.append("Product mismatch.")
    if r.get("manifest_sha256") != sha(args.manifest):
        errors.append("Manifest changed after review initialization; initialize a new review.")
    reviewed = keyed(r.get("pages"), "page_id", "review pages", errors)
    expected_ids = {p["page_id"] for p in m["pages"]}
    if set(reviewed) != expected_ids:
        errors.append("Review page set does not match manifest.")
    for p in m["pages"]:
        pid = p["page_id"]
        q = reviewed.get(pid)
        if q is None:
            continue
        if q.get("file") != p["file"]:
            errors.append(pid + ": review file mismatch.")
        if q.get("image_sha256") != sha(within(root, p["file"])):
            errors.append(pid + ": image changed; old review invalid.")
        if not nonempty(q.get("reviewer")):
            errors.append(pid + ": reviewer missing.")
        try:
            stamp = datetime.fromisoformat(q.get("reviewed_at", "").replace("Z", "+00:00"))
            if stamp.tzinfo is None:
                raise ValueError()
            if stamp > datetime.now(timezone.utc):
                raise ValueError()
        except (ValueError, TypeError, AttributeError):
            errors.append(pid + ": valid past timezone-aware reviewed_at required.")
        texts = keyed(q.get("critical_text"), "id", pid + " text", errors)
        if set(texts) != {t["id"] for t in p["critical_text"]}:
            errors.append(pid + ": critical text coverage mismatch.")
        for t in p["critical_text"]:
            observed = texts.get(t["id"], {})
            where = pid + "/" + t["id"]
            value = observed.get("observed")
            if not nonempty(value) or norm(value) != norm(t["expected"]):
                errors.append(where + ": observed text mismatch or unreadable.")
            if observed.get("review_method") not in {"manual", "ocr+visual"}:
                errors.append(where + ": manual or ocr+visual review required.")
            if observed.get("review_method") == "ocr+visual" and not nonempty(observed.get("ocr_evidence")):
                errors.append(where + ": actual OCR tool/output reference required.")
            if observed.get("source_verified") is not True:
                errors.append(where + ": source not verified.")
        vc = q.get("visual_checks")
        if not isinstance(vc, dict):
            vc = {}
        if set(vc) != set(CHECKS):
            errors.append(pid + ": missing/unexpected visual check keys.")
        for name in CHECKS:
            item = vc.get(name, {})
            if not isinstance(item, dict):
                errors.append(pid + "/" + name + ": invalid visual record.")
                continue
            if item.get("status") not in {"pass", "not_applicable"} or not nonempty(item.get("notes")):
                errors.append(pid + "/" + name + ": visual review pending/failed or explanation missing.")
            if item.get('status') == 'not_applicable' and name not in {'packaging', 'efficacy_visual'}:
                errors.append(pid + '/' + name + ': mandatory visual review cannot be skipped.')
        issues = q.get("issues")
        if not isinstance(issues, list):
            errors.append(pid + ": issues must be a list.")
            continue
        for issue in issues:
            if not isinstance(issue, dict):
                errors.append(pid + ": invalid issue.")
                continue
            if issue.get("severity") not in {"critical", "major", "minor"}:
                errors.append(pid + ": issue severity missing/invalid.")
            if issue.get("status") not in {"open", "resolved"}:
                errors.append(pid + ": issue status missing/invalid.")
            if not nonempty(issue.get("description")) or not nonempty(issue.get("region")):
                errors.append(pid + ": issue needs description and region.")
            if issue.get("severity") in {"critical", "major"} and issue.get("status") != "resolved":
                errors.append(pid + ": unresolved " + issue["severity"] + " issue.")
            if issue.get("status") == "resolved" and not nonempty(issue.get("resolution")):
                errors.append(pid + ": resolved issue needs repair/recheck evidence.")
    result = {
        "record_gate_passed": not errors,
        "scope": "Review-record consistency and freshness only; not automated image/OCR validation.",
        "product_id": m["product_id"], "page_count": len(m["pages"]),
        "errors": errors
    }
    if args.out:
        write(args.out, result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ("init", "check"):
        p = sub.add_parser(command)
        p.add_argument("--manifest", type=Path, required=True)
        p.add_argument("--root", type=Path, required=True)
        p.add_argument("--record", type=Path, required=True)
        if command == "check":
            p.add_argument("--out", type=Path)
    args = parser.parse_args()
    if hasattr(args, "out") and args.out:
        protected = {args.manifest.resolve(), args.record.resolve()}
        if args.out.resolve() in protected:
            parser.error("--out must not overwrite manifest or review.")
    try:
        return initialize(args) if args.command == "init" else check(args)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("QA gate error: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
