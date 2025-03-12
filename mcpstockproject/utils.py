import tomllib
from pathlib import Path
import random
import yaml


def load_config(section: str | None = None) -> dict:
    config = tomllib.loads((Path(__file__).parent / "config.toml").read_text())
    if section is not None:
        return config[section]
    else:
        return config


def read_yaml_file(file_path):
    """
    Reads a YAML file from the given file path and returns its content as a Python dictionary.

    :param file_path: The path to the YAML file on the disk.
    :return: A Python dictionary interpreting the content of the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            # Use yaml.safe_load() to parse the YAML file into a Python dictionary
            parsed_dict = yaml.safe_load(file)
        return parsed_dict
    except FileNotFoundError:
        raise FileNotFoundError(f"The file at path '{file_path}' was not found.")
    except Exception as e:
        raise ValueError(f"Error reading YAML file: {e}")


def store_report(report):
    # Generate a random integer below 10
    random_number = random.randrange(10)
    print(random_number)
    path = "reports/report_" + str(random_number)
    try:
        # Open the file in write mode
        with open(path, 'w') as file:
            # Write the data to the file
            file.write(report)
        print(f"File written successfully to {path}")
    except Exception as e:
        print(f"Error writing file: {e}")
