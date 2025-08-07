# from pathlib import Path
# import pytest
from yaml import load, Loader
from jsonschema import Draft7Validator
import pytest

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


def walk_dict(to_walk, path=""):
    if isinstance(to_walk, dict):
        for key in to_walk.keys():
            for leaf in walk_dict(to_walk[key], path=f"{path}/{key}"):
                yield leaf
    else:
        yield path


def out_of_order(short, long):
    """
    >>> zoo = ['ant', 'mouse', 'dog', 'horse', 'elephant', 'whale']
    >>> out_of_order(['ant', 'whale'], zoo)
    []
    >>> out_of_order(['mouse', 'elephant', 'horse', 'whale', 'ant', 'dog'], zoo)
    ['horse < elephant', 'ant < whale']
    """
    to_return = []
    old_i = -1
    old = None
    for new in short:
        new_i = long.index(new)
        if new_i <= old_i:
            to_return.append(f"{new} < {old}")
        old = new
        old_i = new_i
    return to_return


@pytest.mark.parametrize(
    "yaml_path", root.glob("deployments/*.yaml"), ids=lambda path: path.name
)
def test_fields_in_order(yaml_path):
    # UI code will be simpler if it can rely on deployment YAML
    # always being in the prescribed order.
    deployment = load(yaml_path.open(), Loader=Loader)
    deployment_paths = list(walk_dict(deployment))
    misordered = out_of_order(deployment_paths, paths)
    assert (
        not misordered
    ), "Paths on the left should come before those on the right in the YAML."
