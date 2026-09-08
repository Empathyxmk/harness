import cloudconvert.environment_vars as env

def test_env_vars_names():
    assert env.CLOUDCONVERT_API_KEY == "API_KEY"
    assert env.CLOUDCONVERT_SANDBOX == "true"

def test_env_module_strings():
    # The docstring should be present on the module
    assert "Environment Variables" in env.__doc__