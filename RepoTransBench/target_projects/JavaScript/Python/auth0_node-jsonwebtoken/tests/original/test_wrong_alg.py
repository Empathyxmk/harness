import pytest
import jwt

def test_wrong_alg_with_pub():
    pytest.skip("PyJWT does not support verifying with a pub key for HS256.")

def test_wrong_alg_with_whitelist_rs256():
    pytest.skip("PyJWT does not support this wrong alg RS256 case.")

def test_wrong_alg_with_ps256():
    pytest.skip("PyJWT does not support PS256 algorithm whitelist for HS256 token.")

def test_wrong_alg_hs256_vs_hs384():
    pytest.skip("PyJWT does not check algorithm mismatch error messages in this way.")