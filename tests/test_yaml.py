from check import check_local, checks
from update_slug import update_slug

import pytest
import re
from collections import Counter
from yaml import load, Loader

from utils import root


def test_unique_slugs():
    slugs = Counter(
        load(path.read_text(), Loader=Loader)["url_slug"]
        for path in root.glob("deployments/*.yaml")
    )
    duplicates = [slug for slug, count in slugs.items() if count > 1]
    assert not duplicates


@pytest.mark.parametrize(
    "yaml_path", root.glob("deployments/*.yaml"), ids=lambda path: path.name
)
def test_updated_slugs(yaml_path):
    (old, new) = update_slug(yaml_path)
    assert old == new, "url_slug was out of sync: updated now"


@pytest.mark.parametrize(
    "yaml_path", root.glob("deployments/*.yaml"), ids=lambda path: path.name
)
def test_real_yaml(yaml_path):
    errors = check_local(yaml_path, only=checks - {"check_urls"})
    assert not errors


@pytest.mark.parametrize(
    "yaml_path", root.glob("tests/good_deployments/*.yaml"), ids=lambda path: path.name
)
def test_good_yaml(yaml_path):
    errors = check_local(yaml_path)
    assert not errors


@pytest.mark.parametrize(
    "bad_yaml_path",
    root.glob("tests/bad_deployments/*.yaml"),
    ids=lambda path: path.name,
)
def test_bad_yaml(bad_yaml_path):
    errors = check_local(bad_yaml_path)
    assert errors, "Expected errors, but there aren't any"
    errors_stem = errors_to_stem(errors)
    assert errors_stem == bad_yaml_path.stem, errors


def errors_to_stem(errors):
    short_paths = re.sub(r"\S+\.", ".", str(errors))
    return re.sub(r"\W+", " ", short_paths).strip().replace(" ", "_").lower()
