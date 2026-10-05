"""Validate repository inputs and public packaging scope; does not review images."""
from pathlib import Path
import hashlib
import json
import re
import struct
import subprocess
import sys
from build_release import read_metadata

ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    fields, _ = read_metadata()
    require(fields["name"] == "beauty-live-handcards", "Skill directory/name mismatch")
    require(bool(fields["description"]) and len(fields["description"]) <= 1024, "Invalid description")
    require(fields["author"] and "待填写" not in fields["author"], "Author is missing")
    files = [p for p in ROOT.rglob("*") if p.is_file() and not any(part in {".git", "dist", "__pycache__"} for part in p.relative_to(ROOT).parts)]
    for path in files:
        require(not path.is_symlink(), "Symlink in distribution")
        require(path.stat().st_size < 100 * 1024 * 1024, "GitHub file exceeds size limit")
        require(path.suffix.lower() not in {".pdf", ".xlsx", ".xls", ".log", ".pyc"}, "Unexpected source/private file: " + path.name)
        require(not path.name.startswith(".env"), "Environment file in distribution")
        if path.suffix.lower() in {".md", ".py", ".json"}:
            text = path.read_text(encoding="utf-8-sig")
            require(not re.search(r"\b(?:github_pat_|ghp_)[A-Za-z0-9_]{25,}", text), "Credential-like content")
            require(not re.search(r"\b[A-Z]:[\\/]", text), "Absolute machine path: " + path.name)
        if path.suffix.lower() == ".md":
            text = path.read_text(encoding="utf-8-sig")
            for link in re.findall(r"\]\(([^)]+)\)", text):
                if "://" not in link and not link.startswith("#"):
                    require((path.parent / link.split("#")[0]).exists(), "Broken local link: " + str(path.relative_to(ROOT)) + " -> " + link)
    skill = ROOT / "skills" / fields["name"]
    for p in skill.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts:
            text = p.read_text(encoding="utf-8")
            require(not any(x in text for x in ("香莱可人", "漾皑秀", "XYJCR", "YOUNG XCELL", "current-project.md", "yang-aixiu")), "Product-specific facts in installable skill")
    manifest = json.loads((ROOT / "examples" / "manifest.json").read_text(encoding="utf-8"))
    named = set()
    for case in manifest["sets"]:
        require(case["image_count"] == len(case["images"]), "Case count mismatch")
        for image in case["images"]:
            path = ROOT / "examples" / case["id"] / image["file"]
            require(path.is_file(), "Missing case image")
            data = path.read_bytes()
            require(hashlib.sha256(data).hexdigest() == image["sha256"], "Image hash differs")
            require(len(data) == image["bytes"], "Image size differs")
            require(data[:8] == b"\x89PNG\r\n\x1a\n", "PNG signature differs")
            width, height = struct.unpack(">II", data[16:24])
            require([width, height] == [image["width"], image["height"]], "PNG dimensions differ")
            named.add(path.resolve())
    actual = set(p.resolve() for p in (ROOT / "examples").rglob("*.png"))
    require(actual == named, "Unlisted/missing showcase image")
    require(manifest["image_total"] == len(named), "Image total differs")
    subprocess.run([sys.executable, str(skill / "scripts" / "qa_gate.py"), "--help"], capture_output=True, check=True)
    print(json.dumps({"metadata": "passed", "local_links": "passed", "public_file_scope": "passed",
                      "case_sets": len(manifest["sets"]), "image_hashes_checked": len(named),
                      "qa_gate_help": "passed", "visual_review": "not performed by this validator"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError) as error:
        print("Validation failed: " + str(error), file=sys.stderr)
        sys.exit(1)

