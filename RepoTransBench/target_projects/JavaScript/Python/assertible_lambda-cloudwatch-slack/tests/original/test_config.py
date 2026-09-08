import os
import importlib
import sys

SRC_PATH = "src.aws_lambda_cloudwatch_slack.config"

def reload_config():
    # Remove the module from sys modules to reload with fresh env
    if SRC_PATH in sys.modules:
        del sys.modules[SRC_PATH]
    return importlib.import_module(SRC_PATH)

def test_exports_kms_encrypted_hook_url_from_env(monkeypatch):
    monkeypatch.setenv("KMS_ENCRYPTED_HOOK_URL", "encryptedurl")
    config = reload_config()
    assert config.kmsEncryptedHookUrl == "encryptedurl"

def test_exports_unencrypted_hook_url_from_env(monkeypatch):
    monkeypatch.setenv("UNENCRYPTED_HOOK_URL", "unencryptedurl")
    config = reload_config()
    assert config.unencryptedHookUrl == "unencryptedurl"

def test_services_contain_correct_match_text():
    import src.aws_lambda_cloudwatch_slack.config as config
    assert config.services["elasticbeanstalk"]["match_text"] == "ElasticBeanstalkNotifications"
    assert config.services["codedeploy"]["match_text"] == "CodeDeploy"
    assert config.services["codepipeline"]["match_text"] == "CodePipelineNotifications"
    assert config.services["elasticache"]["match_text"] == "ElastiCache"
    assert config.services["autoscaling"]["match_text"] == "AutoScaling"
    assert isinstance(config.services["cloudwatch"], dict)