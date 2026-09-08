import os
import casbin

dir_path = os.path.dirname(os.path.realpath(__file__))

def test_01_demo_enforcement_public():
    # Use a different user and resource than the existing test
    model_path = os.path.join(dir_path, 'model.conf')
    policy_path = os.path.join(dir_path, 'policy.csv')
    e = casbin.Enforcer(model_path, policy_path, True)
    # Different subjects/resources/actions compared to private tests
    assert not e.enforce("alice2", "data2", "write")
    assert e.enforce("alice2", "data2", "read")
    assert not e.enforce("bob2", "data2", "read")
    assert e.enforce("bob2", "data2", "write")
    assert not e.enforce("bob2", "data1", "read")
    assert e.enforce("root2", "data1", "delete")
    assert not e.enforce("root2", "data1", "update")

def test_02_orm_adapter_public(tmp_path):
    # Don't use casbin.persist.adapters.Adapter, only test FileAdapter
    from casbin.persist.adapters import FileAdapter
    model_path = os.path.join(dir_path, 'model.conf')
    policy_path = os.path.join(dir_path, 'policy.csv')
    # Use Casbin's FileAdapter to simulate
    a = FileAdapter(policy_path)
    e = casbin.Enforcer(model_path, a)
    # Test public subject/action combo
    assert e.enforce("alice2", "data2", "read")
    assert not e.enforce("alice2", "data2", "write")

def test_03_custom_orm_public(tmp_path):
    # Custom model with domain.
    import casbin
    model_path = os.path.join(dir_path, 'custom_model.conf')
    # We'll hardcode a simple csv for this test
    custom_policy = os.path.join(tmp_path, "custom_policy.csv")
    with open(custom_policy, 'w') as f:
        f.write("p, john, domain_public, data9, access\n")
        f.write("p, jane, domain_public, data9, read\n")
        f.write("p, john, domain_public, data10, modify\n")
    e = casbin.Enforcer(model_path, custom_policy)
    assert e.enforce("john", "domain_public", "data9", "access")
    assert not e.enforce("john", "domain_public", "data9", "read")
    assert e.enforce("john", "domain_public", "data10", "modify")
    assert not e.enforce("jane", "domain_public", "data9", "access")
    assert e.enforce("jane", "domain_public", "data9", "read")