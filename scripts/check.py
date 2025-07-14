from pathlib import Path
from sys import exit
from yaml import load, Loader, dump, scan
import re
from jsonschema import validate, Draft7Validator
from spellchecker import SpellChecker
import requests


root = Path(__file__).parent.parent

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)

spell = SpellChecker()
spell.word_frequency.load_words((root / "dictionary.txt").read_text().splitlines())

known_bad_urls = (root / "known_bad_urls.txt").read_text().splitlines()


def check_name(yaml_path: Path):
    if not re.fullmatch(r"[a-z0-9_]+\.yaml", yaml_path.name):
        return "File names should be lowercase letters, numbers, and underscores."


def check_schema(yaml_path):
    instance = load(yaml_path.open(), Loader=Loader)
    validator = Draft7Validator(schema, format_checker=Draft7Validator.FORMAT_CHECKER)
    return [error.message for error in validator.iter_errors(instance)]


def get_all_values_paths(node, path=""):
    """
    >>> list(get_all_values_paths({'a': 1, 'b': {'c': [2, 3]}}))
    [('/a', 1), ('/b/c/0', 2), ('/b/c/1', 3)]
    """
    # Revisit this if we add any lists to the schema.
    for key, value in node.items():
        new_path = f"{path}/{key}"
        if isinstance(value, dict):
            yield from get_all_values_paths(value, new_path)
        elif isinstance(value, list):
            yield from get_all_values_paths(dict(enumerate(value)), new_path)
        else:
            yield (new_path, value)


def check_spelling(yaml_path):
    deployment = load(yaml_path.open(), Loader=Loader)
    pairs = get_all_values_paths(deployment)
    errors = []
    for path, text in pairs:
        if not isinstance(text, str):
            continue
        text = re.sub(r"https?://\S+", "", text)
        words = re.findall(r"\w+", text)
        for word in words:
            lc_word = word.lower()
            if word != lc_word:
                continue  # TODO: Tighten spell check.
            if not re.fullmatch(r"[a-z]+", word):
                continue  # TODO: Non-ascii characters in converted data seem like mistakes.
            correction = spell.correction(lc_word)
            if lc_word != spell.correction(lc_word):
                errors.append(f'{path}: "{word}" -> "{correction}"?')
    return errors


def check_urls(yaml_path):
    deployment = load(yaml_path.open(), Loader=Loader)
    pairs = get_all_values_paths(deployment)
    errors = []
    for path, text in pairs:
        if not isinstance(text, str):
            continue
        urls = re.findall(r"https?://\S+", text)
        for url in urls:
            if url in known_bad_urls:
                continue
            request = requests.get(url)
            if request.status_code != 200:
                errors.append(f"HTTP {request.status_code} for {url}")
    return errors


def check_quoting(yaml_path):
    errors = []
    for token in scan(yaml_path.open(), Loader=Loader):
        if hasattr(token, "style"):
            style = token.style
            if style is None or style in ["|", '"', "'"]:
                continue
            errors.append(
                f'instead of "{style}", use "|" to preserve whitespace in "{token.value}"'
            )
    return errors


def infer_tier(deployment):
    # TODO
    return 1, []


def check_tier(yaml_path):
    errors = []
    deployment = load(yaml_path.open(), Loader=Loader)
    expected_tier = deployment["tier"]
    inferred_tier, missing_fields = infer_tier(deployment)
    if expected_tier < inferred_tier:
        assert not missing_fields
        errors.append(
            f"tier could be increased from {expected_tier} to {inferred_tier}"
        )
    if expected_tier > inferred_tier:
        errors.append(
            f"record is actually only tier {inferred_tier}; "
            f'for tier {expected_tier} fill in {", ".join(missing_fields)}'
        )
    return errors


def check(yaml_path: Path):
    detail_checks = [
        function for name, function in globals().items() if name.startswith("check_")
    ]
    errors = {}
    for detail_check in detail_checks:
        name = detail_check.__name__.replace("_", " ")
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
        assert isinstance(error, list)
        if error:
            errors[yaml_path.name] = error
    if errors:
        print(dump(errors))
        exit(1)
    print("No errors!")
