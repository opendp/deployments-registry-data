import re
from pathlib import Path
import pytest
from jsonschema import validate, Draft7Validator
from yaml import load, Loader
from spellchecker import SpellChecker


root = Path(__file__).parent.parent

yaml_paths = list(root.glob("deployments/*.yaml")) + list(
    Path(__file__).parent.glob("deployments/*.yaml")
)

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)

spell = SpellChecker()
spell.word_frequency.load_words((root / "dictionary.txt").read_text().splitlines())


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_name(yaml_path):
    assert re.fullmatch(r"[a-z][a-z0-9_]+\.yaml", yaml_path.name)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_schema(yaml_path):
    instance = load(yaml_path.open(), Loader=Loader)
    validate(instance, schema, format_checker=Draft7Validator.FORMAT_CHECKER)


def get_all_values_paths(node, path=""):
    # Revisit this if we add any lists to the schema.
    for key, value in node.items():
        new_path = f"{path}/{key}"
        if isinstance(value, dict):
            yield from get_all_values_paths(value, new_path)
        else:
            yield (new_path, value)


@pytest.mark.parametrize("yaml_path", yaml_paths, ids=lambda path: path.name)
def test_yaml_spelling(yaml_path):
    deployment = load(yaml_path.open(), Loader=Loader)
    pairs = get_all_values_paths(deployment)
    errors = []
    for path, text in pairs:
        if not isinstance(text, str):
            continue
        words = re.findall(r"\w+", text)
        for word in words:
            lc_word = word.lower()
            correction = spell.correction(lc_word)
            if lc_word != spell.correction(lc_word):
                errors.append(f'{path}: "{word}" -> "{correction}"?')
    assert not errors, "\n".join(errors)
