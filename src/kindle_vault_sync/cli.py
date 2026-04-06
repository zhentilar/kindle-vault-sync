from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

from .brief import build_plaintext_brief, to_html_document
from .config import ConfigError, get_mail_credentials, load_config
from .scanner import collect_markdown_files, extract_todos_and_notes, load_vocab_words
from .sender import send_attachment


def build_digest(config_path: Path) -> tuple[str, Path, str]:
    config = load_config(config_path)

    files = collect_markdown_files(
        vault_path=config.vault_path,
        include_patterns=config.include_patterns,
        exclude_patterns=config.exclude_patterns,
        scan_days=config.scan_days,
    )

    words = load_vocab_words(
        vault_path=config.vault_path,
        vocab_file=config.vocab_file,
        vocab_count=config.vocab_count,
    )

    todos, notes = extract_todos_and_notes(
        vault_path=config.vault_path,
        files=files,
        include_full_notes=config.include_full_notes,
        preview_lines=config.preview_lines,
    )

    plain = build_plaintext_brief(config=config, words=words, todos=todos, notes=notes)
    html = to_html_document(plain)

    config.output_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_file = config.output_dir / f"JLPT-{today}.html"
    out_file.write_text(html, encoding="utf-8")

    return plain, out_file, today


def main() -> None:
    parser = argparse.ArgumentParser(description="Build and send a vault digest to Kindle")
    parser.add_argument("command", choices=["preview", "send"], help="preview: print digest, send: email digest")
    parser.add_argument("--config", default="config.json", help="Path to config json file")

    args = parser.parse_args()
    config_path = Path(args.config).resolve()

    try:
        plain_text, out_file, today = build_digest(config_path)
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        raise SystemExit(2)

    if args.command == "preview":
        print(plain_text)
        print(f"\nSaved HTML: {out_file}")
        return

    try:
        config = load_config(config_path)
        kindle_email, sender_email, app_password = get_mail_credentials()
        send_attachment(
            smtp_host=config.smtp_host,
            smtp_port=config.smtp_port,
            sender_email=sender_email,
            sender_password=app_password,
            target_email=kindle_email,
            subject=f"JLPT {today}",
            attachment_path=out_file,
        )
    except ConfigError as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        raise SystemExit(2)
    except Exception as exc:
        print(f"Send error: {exc}", file=sys.stderr)
        raise SystemExit(1)

    print(f"Sent: {today} -> {kindle_email}")


if __name__ == "__main__":
    main()
