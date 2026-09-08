def test_import_exceptions_public():
    import cloudconvert.exceptions.exceptions as exc_mod
    assert hasattr(exc_mod, "CloudConvertException")
    assert isinstance(exc_mod.CloudConvertException("public"), Exception)

def test_inheritance_cloudconvert_exception_public():
    from cloudconvert.exceptions.exceptions import CloudConvertException
    class SubCloudConvertException(CloudConvertException):
        pass
    e = SubCloudConvertException("public error")
    assert isinstance(e, CloudConvertException)
    assert "public error" in str(e)