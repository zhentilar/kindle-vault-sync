from __future__ import annotations

from datetime import datetime
from html import escape

from .config import AppConfig
from .scanner import NoteItem, TodoItem


def build_plaintext_brief(
    config: AppConfig,
    words: list[str],
    todos: list[TodoItem],
    notes: list[NoteItem],
) -> str:
    today = datetime.now().strftime("%Y-%m-%d")

    vocab_section = "\n".join(f"{i + 1}. {word}" for i, word in enumerate(words))
    if not vocab_section:
        vocab_section = "(No vocab words found)"

    todo_section = "\n".join(f"- [{todo.source}] {todo.content}" for todo in todos)
    if not todo_section:
        todo_section = "(No todos found in range)"

    notes_section = "\n\n".join(f"[{note.source}]\n{note.content}" for note in notes)
    if not notes_section:
        notes_section = "(No notes found in range)"

    return (
        f"{config.title_prefix} - {today}\n\n"
        f"{config.vocab_title}\n"
        f"{vocab_section}\n\n"
        f"{config.todo_title}\n"
        f"{todo_section}\n\n"
        f"{config.notes_title}\n"
        f"{notes_section}"
    )


def to_html_document(plain_text: str) -> str:
    return f"<html><body><pre>{escape(plain_text)}</pre></body></html>"
