
#!/usr/bin/env python3
"""Generate a naturally sorted repository tree inside README.md."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
README = ROOT / "README.md"

START_MARKER = "<!-- TREE_START -->"
END_MARKER = "<!-- TREE_END -->"

IGNORED = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
}

def natural_key(item: Path):
    """Sort numbered filenames naturally: 2.png before 10.png."""
    return [
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", item.name)
    ]

def build_tree(folder: Path, prefix: str = "") -> list[str]:
    """Build a readable tree of files and folders."""
    items = [
        item for item in folder.iterdir()
        if item.name not in IGNORED
        and item.name != "README.md"
    ]

    items.sort(key=lambda item: (item.is_file(), natural_key(item)))

    lines = []

    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        connector = "└── " if is_last else "├── "
        suffix = "/" if item.is_dir() else ""

        lines.append(f"{prefix}{connector}{item.name}{suffix}")

        if item.is_dir():
            extension = "    " if is_last else "│   "
            lines.extend(build_tree(item, prefix + extension))

    return lines

def main():
    content = README.read_text(encoding="utf-8")

    if START_MARKER not in content or END_MARKER not in content:
        raise ValueError(
            "README.md must contain TREE_START and TREE_END markers."
        )

    if content.index(START_MARKER) >= content.index(END_MARKER):
        raise ValueError("Tree markers are in the wrong order.")

    tree_lines = [ROOT.name + "/", *build_tree(ROOT)]
    tree_block = "```text\n" + "\n".join(tree_lines) + "\n```"

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )

    replacement = (
        START_MARKER + "\n" + tree_block + "\n" + END_MARKER
    )

    updated = pattern.sub(lambda _: replacement, content, count=1)

    if updated != content:
        README.write_text(updated, encoding="utf-8")
        print("README.md repository structure updated!")
    else:
        print("README.md repository structure is already up to date.")

if __name__ == "__main__":
    main()
