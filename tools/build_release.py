"""Build host-specific skill packages and the authorized product gallery."""
from pathlib import Path
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "beauty-live-handcards"


def read_metadata():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    _, front, body = text.split("---", 2)
    fields = {}
    for key in ("name", "description", "author", "version", "display_name"):
        match = re.search(r"^\s*" + key + r":\s*(.+)$", front, re.M)
        if not match:
            raise ValueError("Missing metadata: " + key)
        value = match.group(1).strip()
        fields[key] = json.loads(value) if value.startswith('"') else value
    if not re.fullmatch(r"\d+\.\d+\.\d+", fields["version"]):
        raise ValueError("Expected semantic version")
    return fields, body


def entries(directory, prefix=""):
    for path in sorted(directory.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            if path.is_symlink():
                raise ValueError("Symlink excluded: " + str(path))
            yield prefix + path.relative_to(directory).as_posix(), path.read_bytes()


def archive(path, files):
    files = list(files)
    expected = dict(files)
    if len(expected) != len(files):
        raise ValueError("Duplicate archive entries")
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for name, content in files:
            info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, content)
    with zipfile.ZipFile(path) as z:
        if z.testzip() is not None or set(z.namelist()) != set(expected):
            raise ValueError("Archive verification failed")
        for name in z.namelist():
            if z.read(name) != expected[name]:
                raise ValueError("Archive content differs: " + name)


def main():
    fields, body = read_metadata()
    version = fields["version"]
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    generic = dist / ("beauty-live-handcards-agent-" + version + ".zip")
    workbuddy = dist / ("beauty-live-handcards-workbuddy-" + version + ".zip")
    examples = dist / ("beauty-live-handcards-product-examples-" + version + ".zip")
    archive(generic, entries(SKILL, "beauty-live-handcards/"))
    workbuddy_fields = {
        "name": fields["name"], "display_name": fields["display_name"],
        "display_name_en": "Beauty Live Handcards",
        "description": fields["description"],
        "description_zh": "根据真实产品素材制作美妆直播手卡、功效套图和组合卡，兼顾推广表达与中文图像质检。",
        "description_en": "Create beauty livestream product cards and image sets from verified product materials, with promotional copy and visual quality checks.",
        "category": "design", "version": version, "author": fields["author"]
    }
    front = "---\n" + "\n".join(k + ": " + json.dumps(v, ensure_ascii=False) for k, v in workbuddy_fields.items()) + "\n---\n"
    workbuddy_main = (front + body).encode("utf-8")
    archive(workbuddy, ((name, workbuddy_main if name == "SKILL.md" else content) for name, content in entries(SKILL)))
    archive(examples, entries(ROOT / "examples", "examples/"))
    hashes = "\n".join(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name for p in (generic, workbuddy, examples)) + "\n"
    (dist / "SHA256SUMS").write_text(hashes, encoding="utf-8")
    print(hashes, end="")


if __name__ == "__main__":
    main()

