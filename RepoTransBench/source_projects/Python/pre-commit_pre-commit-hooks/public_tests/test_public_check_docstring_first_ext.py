import textwrap
from pre_commit_hooks import check_docstring_first

def test_public_with_module_docstring_and_func(tmp_path):
    # module docstring at top
    file = tmp_path / "documented.py"
    file.write_text(
        textwrap.dedent(
            '''\
            """A top-level docstring."""

            def foo():
                """Function docstring."""
                return True
            '''
        )
    )
    assert check_docstring_first.main([str(file)]) == 0

def test_public_docstring_after_import(tmp_path):
    # import comes first, then docstring: this is wrong
    file = tmp_path / "import_first.py"
    file.write_text(
        textwrap.dedent(
            '''\
            import os

            """Wrong place for docstring."""
            def bar():
                pass
            '''
        )
    )
    assert check_docstring_first.main([str(file)]) == 1

def test_public_no_docstring(tmp_path):
    file = tmp_path / "empty.py"
    file.write_text(
        textwrap.dedent(
            '''\
            def hi():
                return "no docstring"
            '''
        )
    )
    assert check_docstring_first.main([str(file)]) == 1