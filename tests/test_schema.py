from pathlib import Path
import pytest
from yaml import load, Loader

root = Path(__file__).parent.parent


# Load schema:

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)


def get_path_nodes(path, schema):
    yield (path, schema)
    if "properties" in schema:
        for subpath, subschema in schema["properties"].items():
            for path_node in get_path_nodes(f"{path}/{subpath}", subschema):
                yield path_node


path_nodes = list(get_path_nodes("", schema))
paths = [path for path, node in path_nodes]


# Load template:

template = load((root / "tests/good_deployments/template.yaml").open(), Loader=Loader)


def get_path_templates(path, template):
    yield (path, template)
    if isinstance(template, dict):
        for subpath, subtemplate in template.items():
            for path_template in get_path_templates(f"{path}/{subpath}", subtemplate):
                yield path_template


path_templates = list(get_path_templates("", template))


# Tests:


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_nodes_have_descriptions(path, node):
    if path in [
        "/deployment",
        "/deployment/dp_flavor",
        "/deployment/privacy_loss",
        "/deployment/privacy_loss/privacy_parameters/epsilon",
        "/deployment/privacy_loss/privacy_parameters/rho",
        "/deployment/privacy_loss/privacy_parameters/delta",
        "/deployment/model",
        "/deployment/model/model_name_description",
        "/deployment/accounting",
        "/deployment/implementation",
        "/deployment/additional_information",
    ]:
        pytest.skip("TODO: More descriptions would be nice to have")
    assert "description" in node


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_nodes_have_tiers(path, node):
    if "properties" in node:
        return  # Tier is only applied to leaf nodes.
    if not path.startswith("/deployment/"):
        return  # Tier is not needed at the top level.
    if path.startswith("/deployment/privacy_loss/privacy_parameters/"):
        return  # Tier not needed on individual parameters.
    if path in [
        "/deployment/dp_flavor/input_metric",
        "/deployment/dp_flavor/bound_on_input_distance",
        "/deployment/dp_flavor/output_measure",
        "/deployment/dp_flavor/bound_on_output_distance",
        "/deployment/model/model_name_description",
        "/deployment/model/is_many_release_description",
    ]:
        pytest.skip("TODO: More tiers would be nice to have")
    assert "tier" in node


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_objects_have_additional_properties_false(path, node):
    if not "properties" in node:
        return  # Only applicable to objects
    assert not node["additionalProperties"]


def test_template_is_complete():
    template_paths = [path for path, node in path_templates]
    assert template_paths == paths
