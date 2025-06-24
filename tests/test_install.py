from jsonschema import validate, Draft7Validator
from jsonschema.exceptions import ValidationError
import pytest


def validate_date(date):
    validate(
        instance=date,
        schema={"type": "string", "format": "date"},
        format_checker=Draft7Validator.FORMAT_CHECKER,
    )


@pytest.mark.parametrize("no_date", ["abc", "2000", "2000-01"])
def test_format_check_fails(no_date):
    # The jsonschema docs warn:
    # > If a dependency is not installed when using a checker that requires it,
    # > validation will succeed without throwing an error, as also specified by the specification.
    # https://python-jsonschema.readthedocs.io/en/latest/validate/#validating-formats
    #
    # If this test fails, it may mean that not all dependencies are installed.
    with pytest.raises(ValidationError):
        validate_date(no_date)


@pytest.mark.parametrize("date", ["2000-01-01"])
def test_format_check_passes(date):
    validate_date(date)
