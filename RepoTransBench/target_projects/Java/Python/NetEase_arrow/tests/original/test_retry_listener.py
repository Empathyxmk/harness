import pytest
from unittest.mock import Mock, ANY

# Patch-out classes corresponding to Java artifacts

class TestngRetry:
    pass

class RetryListener:
    def transform(self, annotation, test_class, constructor, method):
        # Java: if annotation.getRetryAnalyzer() == null -> setRetryAnalyzer(TestngRetry.class)
        if annotation.getRetryAnalyzer() is None:
            annotation.setRetryAnalyzer(TestngRetry)
        # Else: do nothing

def test_transform_sets_retry_analyzer_when_null():
    listener = RetryListener()
    annotation = Mock()
    annotation.getRetryAnalyzer.return_value = None
    listener.transform(annotation, object, None, None)
    annotation.setRetryAnalyzer.assert_called_once_with(TestngRetry)

def test_transform_does_not_override_if_already_set():
    listener = RetryListener()
    annotation = Mock()
    fake_retry = Mock()
    annotation.getRetryAnalyzer.return_value = fake_retry
    listener.transform(annotation, object, None, None)
    # setRetryAnalyzer should NOT be called if retry analyzer already exists
    annotation.setRetryAnalyzer.assert_not_called()