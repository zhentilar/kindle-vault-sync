from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class AppConfig:
    vault_path: Path
    vocab_file: Path
    output_dir: Path
    scan_days: int
    vocab_count: int
    include_patterns: list[str]
    exclude_patterns: list[str]
    include_full_notes: bool
    preview_lines: int
    title_prefix: str
    todo_title: str
    notes_title: str
    vocab_title: str
    smtp_host: str
    smtp_port: int


class ConfigError(ValueError):
    pass


def _require_type(data: dict[str, Any], key: str, expected: type, default: Any) -> Any:
    value = data.get(key, default)
    if not isinstance(value, expected):
        raise ConfigError(f"Invalid '{key}': expected {expected.__name__}")
    return value


def _require_int_in_range(data: dict[str, Any], key: str, default: int, min_value: int, max_value: int) -> int:
    value = data.get(key, default)
    try:
        value_int = int(value)
    except (TypeError, ValueError) as exc:
        raise ConfigError(f"Invalid '{key}': expected integer") from exc

    if value_int < min_value or value_int > max_value:
        raise ConfigError(f"Invalid '{key}': must be between {min_value} and {max_value}")
    return value_int


def _load_json(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in config file: {config_path}") from exc

    if not isinstance(data, dict):
        raise ConfigError("Config root must be a JSON object")
    return data


def load_config(config_path: Path) -> AppConfig:
    data = _load_json(config_path)
    base = config_path.parent

    scan_days = _require_int_in_range(data, "scan_days", 7, 1, 365)
    vocab_count = _require_int_in_range(data, "vocab_count", 5, 1, 200)
    preview_lines = _require_int_in_range(data, "preview_lines", 8, 1, 200)
    smtp_port = _require_int_in_range(data, "smtp_port", 465, 1, 65535)

    include_patterns = _require_type(data, "include_patterns", list, ["**/*.md"])
    exclude_patterns = _require_type(data, "exclude_patterns", list, [])
    include_full_notes = _require_type(data, "include_full_notes", bool, True)

    if not all(isinstance(item, str) and item for item in include_patterns):
        raise ConfigError("Invalid 'include_patterns': all items must be non-empty strings")

    if not all(isinstance(item, str) and item for item in exclude_patterns):
        raise ConfigError("Invalid 'exclude_patterns': all items must be non-empty strings")

    vault_path = (base / str(data.get("vault_path", "vault"))).resolve()
    if not vault_path.exists() or not vault_path.is_dir():
        raise ConfigError(f"Invalid 'vault_path': directory not found -> {vault_path}")

    return AppConfig(
        vault_path=vault_path,
        vocab_file=Path(str(data.get("vocab_file", "japanese/jlpt_n5_pool.md"))),
        output_dir=(base / str(data.get("output_dir", "output"))).resolve(),
        scan_days=scan_days,
        vocab_count=vocab_count,
        include_patterns=include_patterns,
        exclude_patterns=exclude_patterns,
        include_full_notes=include_full_notes,
        preview_lines=preview_lines,
        title_prefix=str(data.get("title_prefix", "Daily JLPT Brief")),
        todo_title=str(data.get("todo_title", "Last 7 Days Todo")),
        notes_title=str(data.get("notes_title", "Last 7 Days Notes")),
        vocab_title=str(data.get("vocab_title", "JLPT N5 - 5 Words")),
        smtp_host=str(data.get("smtp_host", "smtp.gmail.com")),
        smtp_port=smtp_port,
    )


def get_mail_credentials() -> tuple[str, str, str]:
    try:
        kindle_email = os.environ["KVS_KINDLE_EMAIL"]
        sender_email = os.environ["KVS_SENDER_EMAIL"]
        app_password = os.environ["KVS_APP_PASSWORD"]
    except KeyError as exc:
        missing = exc.args[0]
        raise ConfigError(f"Missing environment variable: {missing}") from exc

    if "@" not in kindle_email:
        raise ConfigError("Invalid KVS_KINDLE_EMAIL: expected an email address")
    if "@" not in sender_email:
        raise ConfigError("Invalid KVS_SENDER_EMAIL: expected an email address")
    if not app_password.strip():
        raise ConfigError("Invalid KVS_APP_PASSWORD: value is empty")

    return kindle_email, sender_email, app_password
