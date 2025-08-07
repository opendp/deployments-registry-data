# from pathlib import Path
# import pytest
from yaml import load, Loader
from jsonschema import Draft7Validator


from utils import root, path_nodes, paths

ui_hints = load((root / "ui-hints/deployments-hints.yaml").open(), Loader=Loader)
ui_hints_schema = load((root / "schemas/hints-schema.yaml").open(), Loader=Loader)


def test_hints_schema():
    validator = Draft7Validator(
        ui_hints_schema, format_checker=Draft7Validator.FORMAT_CHECKER
    )
    assert not [
        f'{".".join(error.path)}: {error.message}'
        for error in validator.iter_errors(ui_hints)
    ]


def test_short_fields_exist():
    assert set(ui_hints["short_fields"]) < set(paths)


def test_extra_columns_exist():
    assert set(ui_hints["extra_columns"].values()) < set(paths)
