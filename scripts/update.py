from pathlib import Path


def update(path: Path):
    lines = path.read_text().splitlines()
    lines.insert(0, f"url_slug: {path.stem}")
    new_yaml = "\n".join(lines) + "\n"
    path.write_text(new_yaml)


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
        update(yaml_path)
