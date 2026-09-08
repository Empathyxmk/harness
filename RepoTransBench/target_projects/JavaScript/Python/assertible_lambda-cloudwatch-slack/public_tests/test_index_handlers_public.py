import pytest
import copy
import json

from src.aws_lambda_cloudwatch_slack import index


def make_elastic_beanstalk_event_public(message, subject="EbEnv Subject"):
    return {
        "Records": [{
            "Sns": {
                "Message": message,
                "Subject": subject,
                "Timestamp": "2022-08-15T12:34:56Z"
            }
        }]
    }


def make_codedeploy_event_public(msg, subject="CD Deployment"):
    return {
        "Records": [{
            "Sns": {
                "Message": msg if isinstance(msg, str) else json.dumps(msg),
                "Subject": subject,
                "Timestamp": "2023-02-21T15:24:10Z"
            }
        }]
    }


class TestIndexHandlersPublic:
    demo_message = {
        "deploymentGroupName": "AnotherGroup",
        "applicationName": "SampleApp",
        "status": "FAILED"
    }

    # Elastic Beanstalk
    def test_handle_elasticbeanstalk_good_color_alternative_message(self):
        event = make_elastic_beanstalk_event_public('Deployment completed successfully')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'good'
        assert 'Deployment' in result['attachments'][0]['fields'][1]['value']

    def test_handle_elasticbeanstalk_danger_for_RED_alert_message(self):
        event = make_elastic_beanstalk_event_public('ALERT: Environment status changed to RED state.')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'danger'

    def test_handle_elasticbeanstalk_danger_for_severity_indicated(self):
        event = make_elastic_beanstalk_event_public('CRITICAL severity warning detected.')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'danger'

    def test_handle_elasticbeanstalk_warning_for_yellow_notification(self):
        event = make_elastic_beanstalk_event_public('Warning: YELLOW health level reported.')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'warning'

    def test_handle_elasticbeanstalk_warning_when_info_present(self):
        event = make_elastic_beanstalk_event_public('Info: Environment running smoothly.')
        result = index.handleElasticBeanstalk(event, {})
        assert result['attachments'][0]['color'] == 'warning'

    def test_handle_elasticbeanstalk_uses_hardcoded_subject_when_sns_subject_removed(self):
        event = make_elastic_beanstalk_event_public('Recovery notice', None)
        event = copy.deepcopy(event)
        del event['Records'][0]['Sns']['Subject']
        result = index.handleElasticBeanstalk(event, {})
        assert "AWS Elastic Beanstalk Notification" in result['text']

    # CodeDeploy
    def test_handle_codedeploy_json_failed_status_public(self):
        event = make_codedeploy_event_public(dict(self.demo_message, status="FAILED"))
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['color'] == 'danger'
        assert result['attachments'][0]['fields'][1]['title'] == 'Deployment Group'

    def test_handle_codedeploy_json_succeeded_good_in_public_data(self):
        event = make_codedeploy_event_public(dict(self.demo_message, status="SUCCEEDED"))
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['color'] == 'good'

    def test_handle_codedeploy_json_in_progress_warning(self):
        event = make_codedeploy_event_public(dict(self.demo_message, status="IN_PROGRESS"))
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['color'] == 'warning'

    def test_handle_codedeploy_fallback_to_string_message_on_parse_error_public(self):
        event = make_codedeploy_event_public("deployment event string")
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['fields'][1]['title'] == 'Message'

    def test_handle_codedeploy_json_without_deploymentgroupname_public(self):
        event = make_codedeploy_event_public({"status": "SUCCEEDED"})
        result = index.handleCodeDeploy(event, {})
        assert result['attachments'][0]['fields'][1]['title'] == 'Deployment Group'

    def test_handle_codedeploy_works_when_sns_subject_missing_public(self):
        event = make_codedeploy_event_public(dict(self.demo_message))
        event = copy.deepcopy(event)
        del event['Records'][0]['Sns']['Subject']
        result = index.handleCodeDeploy(event, {})
        assert "AWS CodeDeploy Notification" in result['text']

    def test_handle_codedeploy_works_with_missing_sns_and_falls_back_public(self):
        event = {"Records": [{"Sns": {}}]}
        result = index.handleCodeDeploy(event, {})
        assert isinstance(result, dict)
        assert len(result['attachments'][0]['fields']) > 0

    def test_handle_codedeploy_handles_no_records_public_fallback(self):
        event = {}
        result = index.handleCodeDeploy(event, {})
        assert isinstance(result, dict)