from pathlib import Path
from sys import exit


def validate(path: Path):
    pass


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml_paths",
        nargs="*",
        help="If empty, validates all deployments.",
        type=Path,
    )
    args = parser.parse_args()
    paths = args.yaml_paths
    if not paths:
        paths = Path(__file__).parent.glob("deployments/*.yaml")
    errors = []
    for path in paths:
        print(f"Validating {path.name}...")
        error = validate(path)
        if error:
            errors.append(error)
    if errors:
        print(errors)
        exit(1)
    print("No errors!")
