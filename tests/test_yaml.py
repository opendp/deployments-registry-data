import re
from pathlib import Path
import pytest
from jsonschema import validate, Draft7Validator
from jsonschema.exceptions import ValidationError
from yaml import load, Loader


root = Path(__file__).parent.parent

yaml_paths = list(root.glob("deployments/*.yaml")) + list(
    Path(__file__).parent.glob("deployments/*.yaml")
)

bad_yaml_paths = list(Path(__file__).parent.glob("bad_deployments/*.yaml"))

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_name(yaml_path):
    assert re.fullmatch(r"[a-z][a-z0-9_]+\.yaml", yaml_path.name)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_schema(yaml_path):
    instance = load(yaml_path.open(), Loader=Loader)
    validate(instance, schema, format_checker=Draft7Validator.FORMAT_CHECKER)


@pytest.mark.parametrize("bad_yaml_path", bad_yaml_paths, ids=lambda path: path.name)
def test_bad_yaml_schema(bad_yaml_path):
    bad_instance = load(bad_yaml_path.open(), Loader=Loader)
    try:
        validate(bad_instance, schema, format_checker=Draft7Validator.FORMAT_CHECKER)
    except ValidationError as e:
        clean_message = re.sub(r"\W+", " ", e.message).strip().replace(" ", "_").lower()
        assert f"{clean_message}.yaml" == bad_yaml_path.name
        return
    # Should not reach here!
    pytest.fail()
