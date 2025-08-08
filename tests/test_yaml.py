from check import check

from pathlib import Path
import pytest
import re


root = Path(__file__).parent.parent


@pytest.mark.parametrize(
    "yaml_path", root.glob("deployments/*.yaml"), ids=lambda path: path.name
)
def test_real_yaml(yaml_path):
    errors = check(yaml_path, skip=["check_urls"])
    assert not errors


@pytest.mark.parametrize(
    "yaml_path", root.glob("tests/good_deployments/*.yaml"), ids=lambda path: path.name
)
def test_good_yaml(yaml_path):
    errors = check(yaml_path)
    assert not errors


@pytest.mark.parametrize(
    "bad_yaml_path",
    root.glob("tests/bad_deployments/*.yaml"),
    ids=lambda path: path.name,
)
def test_bad_yaml(bad_yaml_path):
    errors = check(bad_yaml_path)
    assert errors, "Expected errors"
    clean_error = re.sub(r"\W+", " ", str(errors)).strip().replace(" ", "_").lower()
    assert clean_error == bad_yaml_path.stem, errors
