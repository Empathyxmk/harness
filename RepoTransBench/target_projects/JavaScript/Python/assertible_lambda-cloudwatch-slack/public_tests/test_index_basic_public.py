from src.aws_lambda_cloudwatch_slack import index

def test_public_index_exports_and_util():
    assert isinstance(index, object) or hasattr(index, "__dict__")
    assert hasattr(index, "handleElasticBeanstalk") and callable(index.handleElasticBeanstalk)
    assert hasattr(index, "handleCodeDeploy") and callable(index.handleCodeDeploy)
    assert hasattr(index, "postMessage") and callable(index.postMessage)