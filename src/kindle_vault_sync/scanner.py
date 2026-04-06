from __future__ import annotations

import random
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


@dataclass
class NoteItem:
    source: str
    content: str


@dataclass
class TodoItem:
    source: str
    content: str


def _is_excluded(rel_path: str, exclude_patterns: list[str]) -> bool:
    path = Path(rel_path)
    for pattern in exclude_patterns:
        if path.match(pattern):
            return True
    return False


def collect_markdown_files(
    vault_path: Path,
    include_patterns: list[str],
    exclude_patterns: list[str],
    scan_days: int,
) -> list[Path]:
    now = datetime.now()
    cutoff = now - timedelta(days=scan_days)

    files: list[Path] = []
    for pattern in include_patterns:
        for file_path in vault_path.glob(pattern):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() != ".md":
                continue

            rel = str(file_path.relative_to(vault_path))
            if _is_excluded(rel, exclude_patterns):
                continue

            modified = datetime.fromtimestamp(file_path.stat().st_mtime)
            if modified < cutoff:
                continue

            files.append(file_path)

    deduped = sorted(set(files))
    return deduped


def load_vocab_words(vault_path: Path, vocab_file: Path, vocab_count: int) -> list[str]:
    full_path = (vault_path / vocab_file).resolve()
    if not full_path.exists():
        return []

    lines = [
        line.strip("- ").strip()
        for line in full_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not lines:
        return []

    count = min(vocab_count, len(lines))
    return random.sample(lines, count)


def extract_todos_and_notes(
    vault_path: Path,
    files: list[Path],
    include_full_notes: bool,
    preview_lines: int,
) -> tuple[list[TodoItem], list[NoteItem]]:
    todos: list[TodoItem] = []
    notes: list[NoteItem] = []

    for file_path in files:
        text = file_path.read_text(encoding="utf-8")
        rel = str(file_path.relative_to(vault_path))

        for todo in re.findall(r"- \[ \] (.+)", text):
            todos.append(TodoItem(source=rel, content=todo.strip()))

        clean_text = text.strip()
        if not clean_text:
            continue

        if include_full_notes:
            notes.append(NoteItem(source=rel, content=clean_text))
            continue

        selected: list[str] = []
        for line in clean_text.splitlines():
            line = line.strip()
            if not line:
                continue
            selected.append(line)
            if len(selected) >= preview_lines:
                break

        if selected:
            notes.append(NoteItem(source=rel, content="\n".join(selected)))

    unique_todos: list[TodoItem] = []
    seen: set[tuple[str, str]] = set()
    for todo in todos:
        key = (todo.source, todo.content)
        if key in seen:
            continue
        seen.add(key)
        unique_todos.append(todo)

    return unique_todos, notes
