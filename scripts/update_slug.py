from pathlib import Path
import re


def update_slug(path: Path):
    # Preserving YAML formatting is annoying,
    # so we'll just do string replacement.
    # Not ideal!
    deployment_yaml = path.read_text()
    match = re.search(r"^url_slug: (.*)", deployment_yaml)

    old_slug = match.group(1)
    new_slug = path.stem
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
