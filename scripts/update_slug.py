from pathlib import Path
import re
from yaml import load, Loader


def clean(messy):
    return re.sub(r"\W+", "_", messy.lower())


def make_slug(data):
    product = data["deployment"]["product"]
    return "_".join(
        [
            clean(product["name"]),
            clean("-".join(product["data_curators"])),
            clean(product["publication_date"].split("-")[0]),
        ]
    ).replace("_", "-")


def update_slug(path: Path):
    # Preserving YAML formatting is annoying,
    # so we'll just do string replacement.
    # Not ideal!
    deployment_yaml = path.read_text()
    match = re.search(r"^url_slug: (.*)", deployment_yaml)

    deployment = load(deployment_yaml, Loader=Loader)

    old_slug = match.group(1)
    new_slug = make_slug(deployment)
    deployment_yaml = re.sub(
        r"^url_slug: (.*)", f"url_slug: {new_slug}", deployment_yaml
    )

    path.write_text(deployment_yaml)
    return (old_slug, new_slug)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml_paths",
        nargs="+",
        type=Path,
    )
    args = parser.parse_args()
    for yaml_path in args.yaml_paths:
        update_slug(yaml_path)
