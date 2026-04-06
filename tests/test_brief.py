from pathlib import Path

from kindle_vault_sync.brief import build_plaintext_brief
from kindle_vault_sync.config import AppConfig
from kindle_vault_sync.scanner import NoteItem, TodoItem


def test_build_plaintext_brief_contains_sections() -> None:
    config = AppConfig(
        vault_path=Path("vault"),
        vocab_file=Path("japanese/jlpt_n5_pool.md"),
        output_dir=Path("output"),
        scan_days=7,
        vocab_count=5,
        include_patterns=["**/*.md"],
        exclude_patterns=[],
        include_full_notes=True,
        preview_lines=8,
        title_prefix="Daily JLPT Brief",
        todo_title="Last 7 Days Todo",
        notes_title="Last 7 Days Notes",
        vocab_title="JLPT N5 - 5 Words",
        smtp_host="smtp.gmail.com",
        smtp_port=465,
    )

    text = build_plaintext_brief(
        config=config,
        words=["mizu", "hon"],
        todos=[TodoItem(source="daily/today.md", content="Study")],
        notes=[NoteItem(source="notes/a.md", content="line1")],
    )

    assert "Daily JLPT Brief" in text
    assert "JLPT N5 - 5 Words" in text
    assert "Last 7 Days Todo" in text
    assert "Last 7 Days Notes" in text
