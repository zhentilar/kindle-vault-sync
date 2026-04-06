import json
from pathlib import Path

import pytest

from kindle_vault_sync.config import ConfigError, load_config


def test_invalid_scan_days_raises(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    vault.mkdir()

    cfg = {
        "vault_path": "vault",
        "scan_days": 0,
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(cfg), encoding="utf-8")

    with pytest.raises(ConfigError):
        load_config(config_path)


def test_missing_vault_path_raises(tmp_path: Path) -> None:
    cfg = {
        "vault_path": "missing-vault",
    }
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps(cfg), encoding="utf-8")

    with pytest.raises(ConfigError):
        load_config(config_path)
