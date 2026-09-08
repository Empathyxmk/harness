import jmespath
from jmespath.functions import Functions

class CustomFunctions(Functions):
    @jmespath.functions.signature({'types': ['number']})
    def _func_pubadd(self, x):
        return x + 42

def test_custom_function_pubadd_public():
    functions = CustomFunctions()
    # This is the legacy, correct way of injecting functions for jmespath
    options = jmespath.Options(custom_functions=functions)
    res = jmespath.search("pubadd(@)", 58, options=options)
    assert res == 100

def test_custom_function_pubarraydouble_public():
    class MyFuncs(Functions):
        @jmespath.functions.signature({'types': ['array']})
        def _func_arraydouble(self, x):
            return [i * 2 for i in x]
    myfuncs = MyFuncs()
    arr = [7, 6, 5]
    options = jmespath.Options(custom_functions=myfuncs)
    out = jmespath.search("arraydouble(@)", arr, options=options)
    assert out == [14, 12, 10]