import unittest
from src.deye_active_power_regulation import ActivePowerRegulationStateMachine, ActivePowerRegulationState


class TestActivePowerRegulationStateMachinePublic(unittest.TestCase):

    def test_initial_state(self):
        m = ActivePowerRegulationStateMachine()
        self.assertEqual(m.state, ActivePowerRegulationState.IDLE)

    def test_set_target_active_power_switches_state(self):
        m = ActivePowerRegulationStateMachine()
        m.set_target_active_power(524.5)
        self.assertEqual(m.target_active_power, 524.5)
        self.assertEqual(m.state, ActivePowerRegulationState.SETPOINT_CHANGED)

    def test_state_goes_to_applied(self):
        m = ActivePowerRegulationStateMachine()
        m.set_target_active_power(802.1)
        m.apply_setpoint()
        self.assertEqual(m.state, ActivePowerRegulationState.APPLIED)
        self.assertEqual(m.target_active_power, 802.1)

    def test_reset_reverts_to_idle(self):
        m = ActivePowerRegulationStateMachine()
        m.set_target_active_power(301.0)
        m.reset()
        self.assertEqual(m.state, ActivePowerRegulationState.IDLE)
        self.assertIsNone(m.target_active_power)


if __name__ == "__main__":
    unittest.main()