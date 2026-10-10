"""Contratti pubblici dei dataset (schema clean/mart)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
DATASETS = sorted(REPO.glob("datasets/*/dataset.yml"))


@pytest.mark.contract
def test_at_least_three_datasets() -> None:
    assert len(DATASETS) >= 3


@pytest.mark.contract
@pytest.mark.parametrize("config_path", DATASETS, ids=lambda p: p.parent.name)
def test_dataset_contract(config_path: Path) -> None:
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    assert cfg["schema_version"] == 1
    assert cfg["root"] == "../../out"

    ds = cfg["dataset"]
    assert ds["category"] == "welfare-lavoro"
    assert ds["source_id"] == "cnel_archivio"
    assert ds["name"].replace("-", "_") == config_path.parent.name.replace("-", "_")
    assert ds["tags"][0] == "welfare-lavoro"
    assert "years" in ds

    sources = cfg["raw"]["sources"]
    assert any(s.get("primary") for s in sources)
    assert all("type" in s and "args" in s for s in sources)

    clean = cfg["clean"]
    assert clean["sql"].endswith("clean.sql")
    assert (config_path.parent / clean["sql"]).exists()
    assert clean["required_columns"]
    assert clean["validate"]["not_null"]
    # primary_key obbligatoria salvo deroga documentata in notes.md
    if "primary_key" not in clean["validate"]:
        notes = config_path.parent / "notes.md"
        assert notes.exists(), "mancano primary_key e notes.md con la deroga"
        assert "eroga" in notes.read_text(encoding="utf-8").lower()

    mart = cfg["mart"]
    assert mart["tables"], "almeno un mart richiesto"
    for table in mart["tables"]:
        sql_path = config_path.parent / table["sql"]
        assert sql_path.exists(), f"manca {table['sql']}"
    assert mart["validate"]["table_rules"]


@pytest.mark.contract
def test_extract_scripts_exist_and_declare_output() -> None:
    for config_path in DATASETS:
        cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        for source in cfg["raw"]["sources"]:
            if source["type"] != "script":
                continue
            cmd = source["args"]["command"]
            assert "extract.py" in cmd
            script = config_path.parent / "extract.py"
            assert script.exists(), f"manca {script}"
            assert source["args"]["output"].endswith(".csv")
