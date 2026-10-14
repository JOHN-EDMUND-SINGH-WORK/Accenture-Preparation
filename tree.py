#!/usr/bin/env python3
"""
Generate a readable folder/file tree for this repository.

Usage:
    python tree.py
    python tree.py --output TREE.md
    python tree.py --root "C:\\path\\to\\Accenture" --output TREE.md

By default, the script scans the folder containing tree.py, prints the tree,
and saves a copy to TREE.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

DEFAULT_IGNORES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "node_modules",
    "target",
    "dist",
}


def build_tree(root: Path, ignore_names: set[str]) -> str:
    """Return a Unicode tree of root's folders and files."""
    lines = [f"{root.name}/"]

    def walk(folder: Path, prefix: str = "") -> None:
        try:
            entries = [
                item for item in folder.iterdir()
                if item.name not in ignore_names
            ]
            entries.sort(key=lambda item: (item.is_file(), item.name.lower()))
        except PermissionError:
            lines.append(f"{prefix}└── [Permission denied]")
            return

        for index, item in enumerate(entries):
            is_last = index == len(entries) - 1
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{item.name}{'/' if item.is_dir() else ''}")

            if item.is_dir():
                extension = "    " if is_last else "│   "
                walk(item, prefix + extension)

    walk(root)
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automatically generate a repository folder tree."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Repository folder to scan (defaults to the folder containing tree.py).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("TREE.md"),
        help="File to save the tree to (default: TREE.md).",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files/folders, except the default ignored folders.",
    )
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"Folder does not exist: {root}")

    ignored = set(DEFAULT_IGNORES)
    if not args.include_hidden:
        # Hidden entries are skipped unless they are explicitly useful.
        hidden_names = {
            item.name for item in root.iterdir()
            if item.name.startswith(".")
        }
        ignored.update(hidden_names)

    tree_text = build_tree(root, ignored)
    print(tree_text)

    output_path = args.output
    if not output_path.is_absolute():
        output_path = root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("```text\n" + tree_text + "\n```\n", encoding="utf-8")
    print(f"\nTree saved to: {output_path}")


if __name__ == "__main__":
    main()
