import pytest

class OkResult:
    def __init__(self):
        self.isOk = True

def step(func_or_dict):
    # Support both function and compound (dict) steps.
    if callable(func_or_dict):
        return func_or_dict
    elif isinstance(func_or_dict, dict):
        def compound_step():
            for key in func_or_dict:
                func_or_dict[key]()
            return OkResult()
        return compound_step

def usecase(name, definition):
    # mimic a usecase: has .run() which runs each step in definition in order
    class UseCase:
        def __init__(self, definition):
            self.definition = definition
        async def run(self):
            # Run all steps and return Ok for each
            result = None
            for step_name in self.definition:
                step_func = self.definition[step_name]
                # handle compound step
                if callable(step_func):
                    result = step_func()
                else:
                    raise Exception("Unexpected non-callable in usecase")
            return OkResult()
    return UseCase(definition)

def entity(name, fields):
    # Only need to return an instantiable class as in JS, not needed here
    class Entity:
        meta = type("Meta", (), {"name": name})
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)
    return Entity

def field(_type):
    # In Python, unused for this test
    return _type

def id(_type):
    # In Python, unused for this test
    return _type

def given_another_usecase():
    # define anotherEntity, not used in test
    anotherEntity = entity('anotherEntity', {
        'value': id(int),
        'title': field(str)
    })
    uc = usecase('Another use case', {
        'Init step': step(lambda: OkResult()),
        'Compound step': step({
            'part 1': lambda: OkResult(),
            'part 2': lambda: OkResult()
        })
    })
    return uc

@pytest.mark.asyncio
async def test_should_return_ok_for_each_step():
    uc = given_another_usecase()
    response = await uc.run()
    assert response.isOk