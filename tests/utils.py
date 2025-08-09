from pathlib import Path
from yaml import load, Loader

root = Path(__file__).parent.parent


# Load schema:

schema = load((root / "schemas/deployments-schema.yaml").open(), Loader=Loader)


def _get_path_nodes(path, schema):
    yield (path, schema)
    if "properties" in schema:
        for subpath, subschema in schema["properties"].items():
            for path_node in _get_path_nodes(f"{path}/{subpath}", subschema):
                yield path_node


path_nodes = list(_get_path_nodes("", schema))
paths = [path for path, node in path_nodes]
