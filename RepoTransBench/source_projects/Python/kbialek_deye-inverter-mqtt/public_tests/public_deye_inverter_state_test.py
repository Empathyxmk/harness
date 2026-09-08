import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from deye_inverter_state import DeyeInverterState
from deye_events import DeyeEventList, DeyeLoggerStatusEvent, DeyeObservationEvent, Observation
from deye_sensor import AbstractSensor, SensorRegisterRanges

class PublicFakeSensor(AbstractSensor):
    def __init__(self, name: str, value: float, is_readiness_check=False):
        super().__init__(name, groups=["float"], print_format="{:0.2f}")
        self.value = value
        self.__is_readiness_check = is_readiness_check

    def read_value(self, registers):
        return self.value

    @property
    def is_readiness_check(self):
        return self.__is_readiness_check

class TestInverterStatePublic(unittest.TestCase):
    def test_no_last_observation(self):
        config_mock = MagicMock()
        config_mock.logger_config.protocol = "rs485"
        modbus = MagicMock()
        reg_ranges = SensorRegisterRanges([], [], 0)
        inverter_state = DeyeInverterState(config_mock, config_mock.logger_config, reg_ranges, modbus, [], [])
        inverter_state._DeyeInverterState__config.event_expiry = 500
        observation_1 = DeyeObservationEvent(Observation(PublicFakeSensor("Voltage", 3.3), datetime.now(), 44.2))
        observation_2 = DeyeObservationEvent(Observation(PublicFakeSensor("Power", 2.2), datetime.now(), 19.2))
        status_event_online = DeyeLoggerStatusEvent(online=True)
        events_new = DeyeEventList([status_event_online, observation_1, observation_2])
        self.assertTrue(inverter_state._DeyeInverterState__is_device_observation_changed(events_new))

    def test_is_device_offline(self):
        config_mock = MagicMock()
        config_mock.logger_config.protocol = "rs485"
        modbus = MagicMock()
        reg_ranges = SensorRegisterRanges([], [], 0)
        inverter_state = DeyeInverterState(config_mock, config_mock.logger_config, reg_ranges, modbus, [], [])
        inverter_state._DeyeInverterState__config.event_expiry = 500
        observation_1 = DeyeObservationEvent(Observation(PublicFakeSensor("Voltage", 3.3), datetime.now(), 44.2))
        observation_2 = DeyeObservationEvent(Observation(PublicFakeSensor("Power", 2.2), datetime.now(), 19.2))
        status_event_online = DeyeLoggerStatusEvent(online=True)
        status_event_offline = DeyeLoggerStatusEvent(online=False)
        inverter_state._DeyeInverterState__last_observations = DeyeEventList(
            [status_event_online, observation_1, observation_2]
        )
        events_new = DeyeEventList([status_event_offline])
        self.assertFalse(inverter_state._DeyeInverterState__is_device_observation_changed(events_new))

    @patch("time.time")
    def test_is_events_unchanged(self, time):
        config_mock = MagicMock()
        config_mock.logger_config.protocol = "rs485"
        modbus = MagicMock()
        reg_ranges = SensorRegisterRanges([], [], 0)
        inverter_state = DeyeInverterState(config_mock, config_mock.logger_config, reg_ranges, modbus, [], [])
        inverter_state._DeyeInverterState__config.event_expiry = 500
        observation_1 = DeyeObservationEvent(Observation(PublicFakeSensor("Voltage", 3.3), datetime.now(), 44.2))
        observation_2 = DeyeObservationEvent(Observation(PublicFakeSensor("Power", 2.2), datetime.now(), 19.2))
        status_event_online = DeyeLoggerStatusEvent(online=True)
        inverter_state._DeyeInverterState__last_observations = DeyeEventList(
            [status_event_online, observation_1, observation_2]
        )

        initial_time = 1640000000
        time.return_value = initial_time

        inverter_state._DeyeInverterState__last_observations = DeyeEventList([status_event_online, observation_1, observation_2])
        events_new = DeyeEventList([status_event_online, observation_1, observation_2])
        inverter_state._DeyeInverterState__event_updated = initial_time - 480  # 8 minutes ago
        self.assertFalse(inverter_state._DeyeInverterState__is_device_observation_changed(events_new))

    @patch("time.time")
    def test_is_events_unchanged_expired(self, time):
        config_mock = MagicMock()
        config_mock.logger_config.protocol = "rs485"
        modbus = MagicMock()
        reg_ranges = SensorRegisterRanges([], [], 0)
        inverter_state = DeyeInverterState(config_mock, config_mock.logger_config, reg_ranges, modbus, [], [])
        inverter_state._DeyeInverterState__config.event_expiry = 500
        observation_1 = DeyeObservationEvent(Observation(PublicFakeSensor("Voltage", 3.3), datetime.now(), 44.2))
        observation_2 = DeyeObservationEvent(Observation(PublicFakeSensor("Power", 2.2), datetime.now(), 19.2))
        status_event_online = DeyeLoggerStatusEvent(online=True)
        inverter_state._DeyeInverterState__last_observations = DeyeEventList(
            [status_event_online, observation_1, observation_2]
        )

        initial_time = 1640000000
        time.return_value = initial_time

        inverter_state._DeyeInverterState__last_observations = DeyeEventList([status_event_online, observation_1, observation_2])
        events_new = DeyeEventList([status_event_online, observation_1, observation_2])
        inverter_state._DeyeInverterState__event_updated = initial_time - 501  # expired
        self.assertTrue(inverter_state._DeyeInverterState__is_device_observation_changed(events_new))


if __name__ == "__main__":
    unittest.main()