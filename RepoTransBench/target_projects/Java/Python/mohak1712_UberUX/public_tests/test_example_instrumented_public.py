class AppContext:
    def get_package_name(self):
        return "mohak.uberux"

def test_use_app_context_public():
    app_context = AppContext()
    assert "uberux" in app_context.get_package_name()