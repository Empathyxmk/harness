import pytest
import io
from pre_commit_hooks import check_merge_conflict

@pytest.mark.parametrize(
    "content, expected_exit",
    [
        (b"This is a regular file\nJust text\n", 0),  # no conflict markers, should pass
        (b"random text\nwith some lines\n", 0),
        (b"No conflicts here\n", 0),
        (
            b"abc\n<<<<<<< BRANCH_ONE\nedit one\n=======\nedit two\n>>>>>>> BRANCH_TWO\nxyz\n",
            1,  # conflict markers present, should fail
        ),
        (
            b"Some text\n<<<<<<< HEAD\nversion X\n=======\nversion Y\n>>>>>>> master\nMore text\n",
            1,
        ),
    ],
)
def test_public_conflict_markers(tmp_path, content, expected_exit):
    f = tmp_path / "some_file.txt"
    f.write_bytes(content)
    # pass assume_in_merge flag so GIT dir is not checked
    args = [str(f), "--assume-in-merge"]
    result = check_merge_conflict.main(args)
    assert result == expected_exit