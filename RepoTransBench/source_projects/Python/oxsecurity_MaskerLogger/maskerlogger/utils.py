import os

def get_config_file_path(filename="gitleaks.toml"):
    cfgdir = os.path.join(os.path.dirname(__file__), "config")
    return os.path.join(cfgdir, filename)