import pytest

# Test only the build and run framework; skip Kaldi/ivector code due to missing dependencies.
def test_basicframework_sanitycheck():
    # Equivalent to SUCCEED() in gtest, i.e., always passes
    assert True