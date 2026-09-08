import os
import casbin
import casbin_sqlalchemy_adapter
import pytest

dir_path = os.path.dirname(os.path.abspath(__file__))

def test_01_demo_enforcement():
    model_path = os.path.join(dir_path, 'model.conf')
    policy_path = os.path.join(dir_path, 'policy.csv')
    e = casbin.Enforcer(model_path, policy_path, True)
    # Should permit nick to read data1
    assert e.enforce("nick", "data1", "read")
    # Should deny nick to write data1
    assert not e.enforce("nick", "data1", "write")
    # Add a new policy and test
    assert e.add_policy("alice", "data2", "read")
    assert e.enforce("alice", "data2", "read")
    # Remove and test
    assert e.remove_policy("alice", "data2", "read")
    assert not e.enforce("alice", "data2", "read")

def test_02_orm_adapter(tmp_path):
    db_url = f'sqlite:///{tmp_path}/test_orm.db'
    adapter = casbin_sqlalchemy_adapter.Adapter(db_url)
    model_path = os.path.join(dir_path, 'model.conf')
    e = casbin.Enforcer(model_path, adapter, True)
    assert e.add_policy("bob", "resource1", "read")
    assert e.enforce("bob", "resource1", "read")
    assert e.remove_policy("bob", "resource1", "read")
    assert not e.enforce("bob", "resource1", "read")

def test_03_custom_orm_param_match():
    adapter = casbin_sqlalchemy_adapter.Adapter('sqlite:///memory.db')
    model_path = os.path.join(dir_path, 'custom_model.conf')
    e = casbin.Enforcer(model_path, adapter, True)

    def params_match(full_name_k1, key2):
        key1 = full_name_k1.split("?")[0]
        return casbin.util.key_match2(key1, key2)
    def params_match_func(*args):
        return params_match(args[0], args[1])
    e.add_function("ParamsMatch", params_match_func)

    # Add policy for GET on /api/user
    assert e.add_policy("999", "/api/user", "GET")
    # Should permit GET on /api/user?aaa=1
    assert e.enforce("999", "/api/user?aaa=1", "GET")
    # Should deny GET on /api/admin?aaa=1
    assert not e.enforce("999", "/api/admin?aaa=1", "GET")
    # Remove
    assert e.remove_policy("999", "/api/user", "GET")
    assert not e.enforce("999", "/api/user?aaa=1", "GET")