import pytest

class FallBackMethodController:
    def department_service_fall_back(self, name):
        # Simulate the fallback response
        if name is None:
            name = ""
        return f"Department Service is taking longer than Expected. Please try again later. Name: {name}"

def test_department_service_fallback():
    controller = FallBackMethodController()
    result = controller.department_service_fall_back("test")
    assert "Department Service is taking longer" in result
    assert "test" in result

def test_department_service_fallback_null_param():
    controller = FallBackMethodController()
    result = controller.department_service_fall_back(None)
    assert "Department Service is taking longer" in result