from pathlib import Path
import re
from yaml import load, Loader, dump


def convert(old_path: Path):
    old_case = load(old_path.open(), Loader=Loader)
    new_deployment = {
        "status": "Converted",
        "registry_authors": ["Shlomi Hod"],
        "deployment": {
            "name": old_case["title"],
            "data_curator": old_case["organization"],
            "intended_use": old_case["application"],
            "data_product_type": "Summary statistics",
            "data_product_region": old_case["region"],
            "data_product_description": old_case["description"],
            "publication_date": f'{old_case["year"] or "1999"}-01-01',
            "additional_information_urls": [old_case["url"]],
            "dp_flavor": "TODO",
            # {
            #     'name': 'TODO', # Infer from parameters?
            #     'data_domain': 'TODO',
            #     'unprotected_quantities': 'TODO',
            # },
            "privacy_loss": {
                "privacy_unit": old_case[
                    "scope"
                ],  # TODO: Not sure I understand the semantics here.
                "privacy_unit_description": "TODO",
                "privacy_parameters": {
                    k: float(v)
                    for (k, v) in {
                        "epsilon": old_case["epsilon"],
                        "rho": old_case["rho"],
                        "delta": old_case["delta"],
                    }.items()
                    if v is not None
                },
            },
            "model": {
                "model_type": old_case["model"],
                "model_type_description": "TODO",
                "release_type": "One-shot",
                "release_type_description": old_case[
                    "dynamic"
                ],  # Descriptions need to be fleshed out.
                "interactivity": "Non-interactive",
            },
            "additional_dp_information": "TODO",
            # {
            #     'post_processing': 'TODO',
            #     'composition': 'TODO',
            # },
            "implementation": {
                "pre_processing_eda_hyperparameter_tuning": "",
                "mechanisms": old_case["mechanism"],
                "justification": "",
            },
        },
    }
    new_yaml_lines = dump(
        new_deployment, sort_keys=False, allow_unicode=True
    ).splitlines()
    for i, line in enumerate(new_yaml_lines):
        if "TODO" in line:
            new_yaml_lines[i] = re.sub(r"^(\s+)", r"\1# ", line)
        if "''" in line:
            new_yaml_lines[i] = f"{line} # TODO: Fill in correct value"
        # Required enumerated values: convert.py just picked one value.
        if any(
            x in line
            for x in ["Summary statistics", "One-shot", "Non-interactive", "1999"]
        ):
            new_yaml_lines[i] = f"{line} # TODO: Is this correct?"

    new_path = Path(__file__).parent.parent / "deployments" / old_path.name
    new_path.write_text("\n".join(new_yaml_lines))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yaml_paths",
        nargs="+",
        help='Try "registry-draft/registry/cases/*.yaml"',
        type=Path,
    )
    args = parser.parse_args()
    for yaml_path in args.yaml_paths:
        convert(yaml_path)
