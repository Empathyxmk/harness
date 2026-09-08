import pytest

class Spec:
    def __init__(self, scenarios):
        self.scenarios = scenarios

    async def __call__(self):
        for scenario in self.scenarios:
            await scenario()

def scenario_another():
    async def the_scenario():
        ctx = {
            'num': 42
        }
        # When running alternative
        ctx['num'] = 100
        # Check another output public
        assert ctx['num'] == 100
    return the_scenario

def given_the_simplest_generic_spec_public():
    return Spec([
        scenario_another()
    ])


@pytest.mark.asyncio
async def test_should_run_and_validate_for_public_data():
    ASpec = given_the_simplest_generic_spec_public()
    await ASpec()
    # Assertion is inside the check step (see above)