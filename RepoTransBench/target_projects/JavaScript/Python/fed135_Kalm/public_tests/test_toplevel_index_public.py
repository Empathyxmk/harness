def test_toplevel_exports_equal_src_public():
    import src
    import src.index as real_export
    assert dir(real_export) == dir(src)
    # Compare public-facing dicts (minus builtins)
    real_export_dict = real_export.__dict__.copy()
    src_dict = src.__dict__.copy()
    for d in [real_export_dict, src_dict]:
        d.pop('__builtins__', None)
        d.pop('__loader__', None)
        d.pop('__package__', None)
        d.pop('__spec__', None)
        d.pop('__cached__', None)
        d.pop('__file__', None)
    assert real_export_dict == src_dict