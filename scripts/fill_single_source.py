#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
import fileinput
from yaml import load, Loader


def process(line: str, key: str):
    link = f"[citation](#{key})"
    # Multi-line with separate _details
    if m := re.match(r"(\s+)description:", line):
        print(f"{m.group(1)}data_curators_details: '{link}'")

    # Single line, free text:
    if m := re.match(
        r"(\s+)(description|intended_use|data_product_region|model_name_details|release_type_details|data_source_type_details|data_domain):[^|]*$",
        line,
    ):
        print(f"{line.rstrip()} {link}")
    # not free text:
    elif m := re.match(
        r"(\s+)(data_product_type|data_product_sector|publication_date|variant_name|access_type):.*",
        line,
    ):
        print(line, end="")
        print(f"{m.group(1)}{m.group(2)}_details: '{link}'")
    elif m := re.match(r"\s+#\s+\w+:.*", line):
        # drop comments
        pass
    else:
        print(line, end="")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--yaml_paths",
        nargs="+",
        type=Path,
    )
    args = parser.parse_args()

    for yaml_path in args.yaml_paths:
        deployment = load(yaml_path.open(), Loader=Loader)
        sources = deployment["deployment"]["administrative"]["evidence_sources"]
        source_keys = list(sources.keys())
        if len(source_keys) > 1:
            print(f"Multiple keys: process {yaml_path} by hand")
            continue

        if "data_curators_details" in yaml_path.read_text():
            print(f"Already processed {yaml_path}")
            continue

        print(f"Processing {yaml_path}")
        key = source_keys[0]
        with fileinput.input(files=yaml_path, encoding="utf-8", inplace=True) as f:
            for line in f:
                process(line, key)
