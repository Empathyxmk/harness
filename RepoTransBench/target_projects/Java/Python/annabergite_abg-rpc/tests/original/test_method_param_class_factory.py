def create_class(method):
    return {"method": method.__name__}

class UserService:
    def method1(self): pass
    def method2(self, a): pass

def test_method_param_class_factory():
    for method in [UserService.method1, UserService.method2]:
        result = create_class(method)
        assert isinstance(result, dict)
        assert "method" in result