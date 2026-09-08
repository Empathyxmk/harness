import pytest
from src.spring5webapp.spring5webapp_application import main

def test_main_method_runs_without_exception():
    # Should not raise any exceptions when run with no args
    main([])

def test_context_loads():
    # This also just calls main, which should not fail
    main([])