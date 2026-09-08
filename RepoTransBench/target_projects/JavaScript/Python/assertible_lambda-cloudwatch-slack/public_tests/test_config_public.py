import os
import importlib
import sys

SRC_PATH = "src.aws_lambda_cloudwatch_slack.config"

def reload_config():
    if SRC_PATH in sys.modules:
        del sys.modules[SRC_PATH]
    return importlib.import_module(SRC_PATH)

def test_exports_different_kms_encrypted_hook_url_from_env(monkeypatch):
    monkeypatch.setenv("KMS_ENCRYPTED_HOOK_URL", "public_encrypted_url_xyz")
    config = reload_config()
    assert config.kmsEncryptedHookUrl == "public_encrypted_url_xyz"

def test_exports_different_unencrypted_hook_url_from_env(monkeypatch):
    monkeypatch.setenv("UNENCRYPTED_HOOK_URL", "public_unencrypted_url_abc")
    config = reload_config()
    assert config.unencryptedHookUrl == "public_unencrypted_url_abc"

def test_contains_expected_service_keys_and_public_match_text():
    import src.aws_lambda_cloudwatch_slack.config as config
    beanstalk_text = config.services["elasticbeanstalk"]["match_text"]
    assert "ElasticBeanstalk" in beanstalk_text
    assert config.services["codedeploy"]["match_text"] == "CodeDeploy"
    expected_keys = {"cloudwatch", "autoscaling", "elasticbeanstalk", "codepipeline", "codedeploy", "elasticache"}
    assert expected_keys.issubset(set(config.services.keys()))
    assert isinstance(config.services["cloudwatch"], dict)