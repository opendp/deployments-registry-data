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
        "/deployment/basic",
        "/deployment/dp_variant",
        "/deployment/privacy_loss",
        "/deployment/privacy_loss/privacy_parameters/epsilon",
        "/deployment/privacy_loss/privacy_parameters/rho",
        "/deployment/privacy_loss/privacy_parameters/delta",
        "/deployment/deployment_model",
        "/deployment/deployment_model/model_name_description",
        "/deployment/accounting",
        "/deployment/implementation",
        "/deployment/administrative",
        "/deployment/administrative/sources",
        "/deployment/administrative/notes",
        "/deployment/administrative/evidence_sources",
    ]:
        assert "description" not in node.keys()
        pytest.skip("TODO: More description would be nice to have")
    if path.endswith("_source"):
        pytest.skip("description_long not needed for every _source field")
    assert "description" in node.keys(), f"{path} missing description"


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_node_has_description_long(path, node):
    skip_list = [
        "",
        "/url_slug",
        "/status",
        "/registry_authors",
        "/deployment",
        "/deployment/basic",
        "/deployment/basic/name",
        "/deployment/basic/description",
        "/deployment/basic/intended_use",
        "/deployment/basic/data_product_region",
        "/deployment/basic/data_product_sector",
        "/deployment/dp_variant",
        "/deployment/dp_variant/data_domain",
        "/deployment/dp_variant/unprotected_quantities",
        "/deployment/privacy_loss/privacy_unit_description",
        "/deployment/privacy_loss/privacy_parameters/epsilon",
        "/deployment/privacy_loss/privacy_parameters/delta",
        "/deployment/privacy_loss/privacy_parameters/rho",
        "/deployment/privacy_loss/privacy_parameters_description",
        "/deployment/deployment_model",
        "/deployment/deployment_model/model_name_description",
        "/deployment/deployment_model/actors",
        "/deployment/deployment_model/release_type_description",
        "/deployment/deployment_model/data_source_type_description",
        "/deployment/deployment_model/access_type_description",
        "/deployment/administrative",
        "/deployment/administrative/notes",
        "/deployment/administrative/registry_authors",
    ]
    if path in skip_list:
        assert "description_long" not in node.keys()
        pytest.skip("TODO: More description_long would be nice to have")
    if path.endswith("_source"):
        pytest.skip("description_long not needed for every _source field")
    assert "description_long" in node.keys(), f"{path} missing description_long"


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_node_has_tier(path, node):
    if "properties" in node:
        return  # Tier is only applied to leaf nodes.
    if not path.startswith("/deployment/"):
        return  # Tier is not needed at the top level.
    if path.startswith("/deployment/privacy_loss/privacy_parameters/"):
        return  # Tier not needed on individual parameters.
    if path in [
        "/deployment/deployment_model/model_name_description",
        "/deployment/deployment_model/release_type_description",
        "/deployment/administrative/registry_authors",
    ]:
        assert "tier" not in node.keys()
        pytest.skip("TODO: More tiers would be nice to have")
    if path.endswith("_source"):
        pytest.skip("tier not needed for every _source field")
    assert "tier" in node.keys(), f"{path} missing tier"


@pytest.mark.parametrize(("path", "node"), path_nodes, ids=paths)
def test_object_has_additional_properties_false(path, node):
    if not "properties" in node:
        return  # Only applicable to objects
    assert not node["additionalProperties"]


def test_template_is_complete():
    template_paths = [
        # Unlike other objects in the schema, the keys of evidences_sources
        # are user-supplied rather than being fixed, so there are keys in the template,
        # but not in the schema.
        path
        for path, node in path_templates
        if "evidence_sources/" not in path
    ]
    assert template_paths == paths
