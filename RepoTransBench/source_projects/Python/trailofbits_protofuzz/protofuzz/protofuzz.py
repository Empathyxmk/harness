"""
protofuzz.py: Core fuzzing engine
"""

def message_strategy(msg_cls, value_generators):
    def generator():
        inst = msg_cls()
        for fname, gen_func in value_generators.items():
            setattr(inst, fname, next(gen_func(None)))
        yield inst
    return generator

def fuzz(strategy, cb, max_tests=128):
    gen = strategy()
    for i, msg in enumerate(gen):
        cb(msg)
        if i+1 >= max_tests:
            break