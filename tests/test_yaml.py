import re
from pathlib import Path
import pytest
from jsonschema import validate, Draft7Validator
from yaml import load, Loader


root = Path(__file__).parent.parent

yaml_paths = list(root.glob("deployments/*.yaml")) + list(
    Path(__file__).parent.glob("deployments/*.yaml")
)

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_name(yaml_path):
    assert re.fullmatch(r"[a-z][a-z0-9_]+\.yaml", yaml_path.name)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_schema(yaml_path):
    instance = load(yaml_path.open(), Loader=Loader)
    validate(instance, schema, format_checker=Draft7Validator.FORMAT_CHECKER)
