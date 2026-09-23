#!/usr/bin/env python3
import argparse
import re
from pathlib import Path
import fileinput


def process(line: str):
    if m := re.match(r"(\s+)description:", line):
        print(f"{m.group(1)}data_curators_details: [citation]()")
    print(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--yaml_path",
        nargs="+",
        type=Path,
    )
    args = parser.parse_args()

    with fileinput.input(files=args.yaml_path, encoding="utf-8", inplace=True) as f:
        for line in f:
            process(line)
