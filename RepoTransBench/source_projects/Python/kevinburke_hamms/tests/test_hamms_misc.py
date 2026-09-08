def test_import_hamms_main():
    # Import should not error now that __main__ module exists
    import hamms.__main__

def test_main_function(capsys):
    from hamms.__main__ import main
    main()
    captured = capsys.readouterr()
    assert "hamms main executed" in captured.out