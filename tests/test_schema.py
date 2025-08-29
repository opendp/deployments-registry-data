from pathlib import Path
import pytest
from yaml import load, Loader

from utils import root, path_nodes, paths


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
def test_node_has_description(path, node):
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
        assert "description" not in node
        pytest.skip("TODO: More description would be nice to have")
    assert "description" in node


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_node_has_description_long(path, node):
    if path in [
        "",
        "/url_slug",
        "/status",
        "/registry_authors",
        "/deployment",
        "/deployment/name",
        "/deployment/description",
        "/deployment/intended_use",
        "/deployment/data_product_region",
        "/deployment/data_product_sector",
        "/deployment/dp_flavor",
        "/deployment/dp_flavor/data_domain",
        "/deployment/dp_flavor/unprotected_quantities",
        "/deployment/privacy_loss/privacy_unit_description",
        "/deployment/privacy_loss/privacy_parameters/epsilon",
        "/deployment/privacy_loss/privacy_parameters/delta",
        "/deployment/privacy_loss/privacy_parameters/rho",
        "/deployment/privacy_loss/privacy_parameters_description",
        "/deployment/model",
        "/deployment/model/model_name_description",
        "/deployment/model/actors",
        "/deployment/model/release_type_description",
        "/deployment/model/data_source_type_description",
        "/deployment/model/access_type_description",
    ]:
        assert "description_long" not in node
        pytest.skip("TODO: More description_long would be nice to have")
    assert "description_long" in node


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_node_has_tier(path, node):
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
        "/deployment/model/release_type_description",
    ]:
        assert "tier" not in node
        pytest.skip("TODO: More tiers would be nice to have")
    assert "tier" in node


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_object_has_additional_properties_false(path, node):
    if not "properties" in node:
        return  # Only applicable to objects
    assert not node["additionalProperties"]


def test_template_is_complete():
    template_paths = [path for path, node in path_templates]
    assert template_paths == paths
