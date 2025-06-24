from pathlib import Path
from sys import exit
from yaml import load, Loader, dump
import re
from jsonschema import validate, Draft7Validator
from jsonschema.exceptions import ValidationError
from spellchecker import SpellChecker


root = Path(__file__).parent

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)

spell = SpellChecker()
spell.word_frequency.load_words((root / "dictionary.txt").read_text().splitlines())


def check_name(yaml_path: Path):
    if not re.fullmatch(r"[a-z][a-z0-9_]+\.yaml", yaml_path.name):
        return "File names should be lowercase letters, numbers, and underscores."


def check_schema(yaml_path):
    instance = load(yaml_path.open(), Loader=Loader)
    validator = Draft7Validator(schema, format_checker=Draft7Validator.FORMAT_CHECKER)
    return [error.message for error in validator.iter_errors(instance)]


def check(yaml_path: Path):
    detail_checks = [
        function for name, function in globals().items() if name.startswith("check_")
    ]
    errors = {}
    for detail_check in detail_checks:
        name = detail_check.__name__
        print(f"\t{name}...")
        error = detail_check(yaml_path)
        if error:
            errors[name] = error
    return errors


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml_paths",
        nargs="*",
        help="If empty, checks all deployments.",
        type=Path,
    )
    args = parser.parse_args()
    yaml_paths = args.yaml_paths
    if not yaml_paths:
        yaml_paths = Path(__file__).parent.glob("deployments/*.yaml")
    errors = {}
    for yaml_path in yaml_paths:
        print(f"Validating {yaml_path.name}...")
        error = check(yaml_path)
        if error:
            errors[yaml_path.name] = error
    if errors:
        print(dump(errors))
        exit(1)
    print("No errors!")
