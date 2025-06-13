import re
from pathlib import Path
import pytest
from jsonschema import validate
from yaml import load, Loader


root = Path(__file__).parent.parent

yaml_paths = list(root.glob("cases/*.yaml"))

schema = load((root / "schemas/cases-schema.yaml").open(), Loader=Loader)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_name(yaml_path):
    assert re.fullmatch(r"[a-z][a-z0-9_]+\.yaml", yaml_path.name)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_schema(yaml_path):
    instance = load(yaml_path.open(), Loader=Loader)
    validate(instance, schema)
