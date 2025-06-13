# deployments-registry-data
Backing data for the privacy deployments registry

## FAQ

### Are there plans to support RDF or connect to `schema.org`?

Not currently. The plain YAML/JSON representation of the data is sufficient for our needs.
That said, we keep the principles of the [`schema.org` naming conventions](https://schema.org/docs/styleguide.html) in mind,
and distinguish nested types in the schema, instead of just having a flat list of fields.
We do use underscores in names for readability.