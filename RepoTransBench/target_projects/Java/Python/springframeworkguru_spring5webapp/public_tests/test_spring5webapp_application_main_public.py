import pytest
from src.spring5webapp.spring5webapp_application import main

def test_main_method_runs_without_exception_with_args():
    # Should not raise any exceptions when run with an argument
    main(["publicTestArg"])