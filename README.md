# deployments-registry-data

This repo provides backing data for the privacy deployments registry.
It is intended to be included as git submodule in the front-end repo.

## Adding new deployment records

New records should be submitted as PRs,
in most cases just a single YAML file updated or modified.
Descriptions and caveats about a new record are best in the YAML itself,
rather than in comments on the PR:
Information in the YAML will benefit all downstream users, and not just the reviewer.

We don't have any hard conventions on file names.
Abbreviating the title of a publication is one approach.
Avoid encoding metadata (year, authors) in the filename so there is less risk of things getting out of sync, but do include enough information to avoid confusion.

PRs are tested automatically.
If you need to add a new enumerated value, an update to the schema will also be required,
and should be justified.
To run tests locally, follow the developer instructions below.

## Getting started as a developer

```bash
# Set up a venv:
python -m venv .venv
source .venv/bin/activate

# Install dependencies:
pip install -r requirements.txt

# Precommit hook:
pre-commit install

# Run tests:
pytest
```

## Reviewing PRs

The tests will make sure the record is valid, so focus on things the computer doesn't do.
Is the description readable?
If this is a new contributor, spot check the original source for accuracy.
If a new enumeration value is proposed, consider getting more opinions before approving.

## FAQ

### Are there plans to support RDF or connect to `schema.org`?

Not currently. The plain YAML/JSON representation of the data is sufficient for our needs.
That said, we keep the principles of the [`schema.org` naming conventions](https://schema.org/docs/styleguide.html) in mind,
and distinguish nested types in the schema, instead of just having a flat list of fields.
We do use underscores in names for readability.