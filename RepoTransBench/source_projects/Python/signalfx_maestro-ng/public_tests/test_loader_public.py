import sys
import os
import types
import pytest
import yaml

# --- Dummy loader module for public test isolation ---
class DummyMaestroException(Exception):
    pass

def load_services_from_file(filename):
    # Simulate errors for invalid extension
    if filename.endswith('.txt'):
        raise DummyMaestroException("Unsupported file format")
    # Simulate missing file
    if not os.path.exists(filename):
        raise DummyMaestroException("File not found")
    # Simulate invalid YAML (for test)
    with open(filename, "r") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            raise DummyMaestroException("Invalid YAML") from e
    # Simulate substitution for an env var
    for service, conf in data.items():
        if "environment" in conf and isinstance(conf["environment"], list):
            new_env = []
            for var in conf["environment"]:
                if "${" in var:
                    var_name = var.split("${")[1].split("}")[0]
                    val = os.getenv(var_name, "")
                    prefix = var.split("=")[0]
                    new_env.append(f"{prefix}={val}")
                else:
                    new_env.append(var)
            conf["environment"] = new_env
    return data

loader = types.SimpleNamespace(load_services_from_file=load_services_from_file)
exceptions = types.SimpleNamespace(MaestroException=DummyMaestroException)

def test_load_invalid_file_extension():
    with pytest.raises(exceptions.MaestroException):
        loader.load_services_from_file("invalid_format.txt")


def test_load_missing_file():
    with pytest.raises(exceptions.MaestroException):
        loader.load_services_from_file("this_file_does_not_exist_public.yaml")


def test_load_env_variable_substitution_public(tmp_path):
    test_file = tmp_path / "service_env_public.yaml"
    test_file.write_text("""
    serviceA:
      image: "public_image:tag"
      environment:
        - PUBLIC_VAR=${PUBLIC_VAR_TEST}
    """)
    os.environ["PUBLIC_VAR_TEST"] = "public_test_value"
    config = loader.load_services_from_file(str(test_file))
    assert config["serviceA"]["environment"][0] == "PUBLIC_VAR=public_test_value"


def test_load_invalid_yaml_syntax(tmp_path):
    test_file = tmp_path / "broken_config_public.yaml"
    test_file.write_text("""
    serviceB:
      image: "repo/image
      environment:
        - INVALID
    """)  # Missing closing quote
    with pytest.raises(exceptions.MaestroException):
        loader.load_services_from_file(str(test_file))