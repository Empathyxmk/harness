import pytest
import copy

# Assume src.aws_lambda_cloudwatch_slack.index exists and has the expected handlers.
from src.aws_lambda_cloudwatch_slack import index

def make_elastic_beanstalk_event(message, subject='TestBeBe Subject'):
    return {
        "Records": [{
            "Sns": {
                "Message": message,
                "Subject": subject,
                "Timestamp": "2021-01-01T00:00:00Z"
            }
        }]
    }

def make_codedeploy_event(msg, subject='TestCD Subject'):
    import json
    return {
        "Records": [{
            "Sns": {
                "Message": msg if isinstance(msg, str) else json.dumps(msg),
                "Subject": subject,
                "Timestamp": "2021-01-01T00:00:00Z"
            }
        }]
    }


class TestIndexHandlers:
    # Elastic Beanstalk
    def test_handle_elasticbeanstalk_good_color_standard_message(self):
        event = make_elastic_beanstalk_event('Application update finished')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'good'
        assert 'Application' in result['attachments'][0]['fields'][1]['value']

    def test_handle_elasticbeanstalk_danger_for_RED(self):
        event = make_elastic_beanstalk_event('Environment health has transitioned to RED.')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'danger'

    def test_handle_elasticbeanstalk_danger_for_Severe(self):
        event = make_elastic_beanstalk_event('Environment health has transitioned to Severe')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'danger'

    def test_handle_elasticbeanstalk_warning_for_yellow(self):
        event = make_elastic_beanstalk_event('Environment health has transitioned to YELLOW')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'warning'

    def test_handle_elasticbeanstalk_warning_for_info(self):
        event = make_elastic_beanstalk_event('Environment health has transitioned to Info')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'warning'

    def test_handle_elasticbeanstalk_default_subject(self):
        event = make_elastic_beanstalk_event('OK again', None)
        event = copy.deepcopy(event)
        del event['Records'][0]['Sns']['Subject']
        result = index.handleElasticBeanstalk(event, {})
        assert "AWS Elastic Beanstalk Notification" in result['text']

    # CodeDeploy
    minimal_message = {
        "deploymentGroupName": "SomeGroup",
        "applicationName": "AppA",
        "status": "FAILED"
    }

    def test_handle_codedeploy_json_failed_status(self):
        event = make_codedeploy_event(dict(self.minimal_message, status="FAILED"))
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['color'] == 'danger'
        assert result['attachments'][0]['fields'][1]['title'] == 'Deployment Group'

    def test_handle_codedeploy_json_succeeded_good(self):
        event = make_codedeploy_event(dict(self.minimal_message, status="SUCCEEDED"))
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['color'] == 'good'

    def test_handle_codedeploy_json_neutral_warning(self):
        event = make_codedeploy_event(dict(self.minimal_message, status="STOPPED"))
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['color'] == 'warning'

    def test_handle_codedeploy_fallback_string_message(self):
        event = make_codedeploy_event("just a string")
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['fields'][1]['title'] == 'Message'

    def test_handle_codedeploy_json_missing_deploymentgroup(self):
        event = make_codedeploy_event({"status": "FAILED"})
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['fields'][1]['title'] == 'Deployment Group'

    def test_handle_codedeploy_missing_sns_subject(self):
        event = make_codedeploy_event(dict(self.minimal_message))
        event = copy.deepcopy(event)
        del event['Records'][0]['Sns']['Subject']
        result = index.handleCodeDeploy(event, {})
        assert "AWS CodeDeploy Notification" in result['text']

    def test_handle_codedeploy_missing_sns_and_fallback(self):
        event = {"Records": [{"Sns": {}}]}
        result = index.handleCodeDeploy(event, {})
        assert isinstance(result, dict)
        assert len(result['attachments'][0]['fields']) > 0

    def test_handle_codedeploy_no_records_fallback(self):
        event = {}
        result = index.handleCodeDeploy(event, {})
        assert isinstance(result, dict)