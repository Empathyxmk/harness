from qcore.events import EventHook
from qcore.asserts import assert_eq

def test_public_eventhook_register_and_emit():
    results = []

    def handler1(x):
        results.append(x)
    def handler2(x):
        results.append(x+1)

    hook = EventHook()
    hook.register(handler1)
    hook.register(handler2)
    hook.emit(100)
    assert_eq(results, [100, 101])
    hook.unregister(handler1)
    hook.emit(200)
    assert_eq(results, [100, 101, 201])