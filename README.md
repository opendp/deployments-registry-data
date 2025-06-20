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

## Relationship to other metadata standards

The Privacy Deployments Registry can be partially mapped to [Dublin Core](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/).

| Registry | DC |
|---|---|
| | contributor |
| | coverage |
| data_curator | creator |
| publication_date | date |
| data_product_description | description |
| | format |
| | identifier |
| | language |
| | publisher |
| | relation |
| | rights |
| | source |
| dp_flavor.data_domain | subject |
| short_name | title |
| | type |
