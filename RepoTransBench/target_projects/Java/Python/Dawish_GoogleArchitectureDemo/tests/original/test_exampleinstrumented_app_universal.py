class AppContext:
    def get_package_name(self):
        return "google.architecture"

def test_use_app_context():
    app_context = AppContext()
    assert app_context.get_package_name() == "google.architecture"