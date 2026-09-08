import unittest
from unittest.mock import patch
from datetime import datetime, timedelta

from src.deye_multi_inverter_data_aggregator import DeyeMultiInverterDataAggregator
from src.deye_observation import Observation

class DummySensor:
    pass

class DummyObs(Observation):
    def __init__(self, sensor, dt, value):
        super().__init__(sensor, dt, value)

class DummyEvent:
    def __init__(self, name, value):
        self.observation = DummyObs(name, datetime.now(), value)

class DummyDeyeEventList(list):
    pass

class DummyAggregatedSensors:
    aggregated_ac_active_power_sensor = DummySensor()
    aggregated_day_energy_sensor = DummySensor()

class TestDeyeMultiInverterDataAggregatorPublic(unittest.TestCase):

    def setUp(self):
        self.aggregator = DeyeMultiInverterDataAggregator()

    def test_process_and_aggregate_public(self):
        el = DummyDeyeEventList([DummyEvent("ac/power", 432.1), DummyEvent("day/energy", 23.45)])
        with patch("src.deye_multi_inverter_data_aggregator.deye_sensors_aggregated", DummyAggregatedSensors), \
             patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            self.aggregator.process(el)
            aggs = self.aggregator.aggregate()
            self.assertEqual(len(aggs), 2)
            # Check that the aggregate values are correct
            self.assertIsInstance(aggs[0], Observation)
            self.assertIsInstance(aggs[1], Observation)
            vals = sorted([agg.value for agg in aggs])
            self.assertCountEqual(vals, [432.1, 23.45])

    def test_reset_state_public(self):
        el = DummyDeyeEventList([DummyEvent("ac/power", 55.0), DummyEvent("day/energy", 12.6)])
        with patch("src.deye_multi_inverter_data_aggregator.deye_sensors_aggregated", DummyAggregatedSensors), \
             patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            self.aggregator.process(el)
            # Simulate date change to trigger reset
            self.aggregator._DeyeMultiInverterDataAggregator__last_aggregation_ts = (
                datetime.now() - timedelta(days=1)
            )
            aggs = self.aggregator.aggregate()
            self.assertTrue(any(isinstance(agg, Observation) for agg in aggs))

    def test_no_event_type_public(self):
        el = DummyDeyeEventList([DummyEvent("test", 1), DummyEvent("test2", 2)])
        with patch("src.deye_multi_inverter_data_aggregator.deye_sensors_aggregated", DummyAggregatedSensors), \
             patch("src.deye_multi_inverter_data_aggregator.DeyeObservationEvent", DummyEvent):
            # Should not fail when events are not real DeyeObservationEvents
            self.aggregator.process(el)
            aggs = self.aggregator.aggregate()
            self.assertEqual(len(aggs), 2)


if __name__ == "__main__":
    unittest.main()